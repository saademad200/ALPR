"""
This module contains the `MainWindow` class, which is the main window of the application.

The `MainWindow` class inherits from `QMainWindow` and contains various widgets and layouts
that make up the user interface of the application. It also contains methods for handling
user input and updating the interface in response to changes in the application state.

Example usage:

    from PyQt5.QtWidgets import QApplication
    from main_window import MainWindow

    app = QApplication([])
    window = main_window()
    window.show()
    app.exec_()
"""
import csv
import datetime
import magic
import cv2
import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QStyle, QFileDialog, QMainWindow
from constants import DEFAULT_IMG_PATH, DATA_PATH
from model.model import ALPR
from user_interface.video_thread import VideoThread
from user_interface.utils import convert_cv_qt, play_video, check_duplicate
from user_interface.initialize_tabs import InitializeTabs
from user_interface.styles import SELECT_BTN_STYLE, UNSELECT_BTN_STYLE


class MainWindow(QMainWindow):
    """
    A class representing the main window of the Ronicom application.

    Attributes
    ----------
    thread : VideoThread or None
        The video processing thread object or None if there is no active thread.
    file : str or None
        The path to the selected video file or None if no file is selected.
    file_type : str or None
        The type of the selected file or None if no file is selected.
    central_widget : QWidget
        The central widget of the main window.
    ocr : ALPR
        The Automatic License Plate Recognition object used for recognizing license plates in
        images and videos.

    Methods
    -------
    __init__()
        Initializes the MainWindow object.
    initialize_ui()
        Initializes the UI of the main window.
    set_browse_mode()
        Sets the browse mode for selecting an image or video file.
    set_stream_mode()
        Sets the stream mode for selecting an IP camera.
    export()
        Exports the table data to an Excel file.
    validate_ip_cam()
        Validates the IP camera address entered by the user.
    start_video_thread(capture, mode=0, ocr=None)
        Starts the video processing thread.
    stop_video_thread()
        Stops the video processing thread.
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Ronicom")

        # Declare Variables
        self.stream = None
        self.file = None
        self.file_type = None

        tab_widget = InitializeTabs(self)

        # Application Widgets
        self.central_widget, self.table, self.alpr_widgets, self.report_widgets = \
            tab_widget.get_widgets()

        self.initialize_ui()
        self.ocr = ALPR()

    def initialize_ui(self):
        """
        Initializes the user interface by connecting button signals to slots and
        setting the central widget.

        """
        # Connect button signals to slots
        self.alpr_widgets['start_processing_btn'].clicked.connect(lambda: self.start_video_thread
        (self.file, mode=1, ocr=self.ocr))
        self.alpr_widgets['stop_processing_btn'].clicked.connect(self.stop_video_thread)
        self.alpr_widgets['browse_btn'].clicked.connect(self.open_file)
        self.alpr_widgets['play_btn'].clicked.connect(lambda: play_video
        (self, self.stream, self.alpr_widgets['play_btn']))
        self.alpr_widgets['validate_button'].clicked.connect(self.validate_ip_cam)
        self.alpr_widgets['browse_mode'].clicked.connect(self.set_browse_mode)
        self.alpr_widgets['stream_mode'].clicked.connect(self.set_stream_mode)

        self.report_widgets['export_btn'].clicked.connect(self.export)
        self.report_widgets['reset_btn'].clicked.connect(self.table.reset)
        self.report_widgets['filter_button'].clicked.connect(self.filter)

        # Set the central widget
        self.setCentralWidget(self.central_widget)

        # Stop any currently running video thread
        self.stop_video_thread()

    def set_browse_mode(self):
        """
        Sets the UI to browse mode.

        Side Effects:
            - Changes the UI to browse mode.
            - Disables IP camera input and validate button.
            - Enables browse button.
            - Clears the status label.

        """
        # Set the browse mode button style
        self.alpr_widgets['browse_mode'].setStyleSheet(SELECT_BTN_STYLE)

        # Set the stream mode button style
        self.alpr_widgets['stream_mode'].setStyleSheet(UNSELECT_BTN_STYLE)

        # Disable IP camera input and validate button
        self.alpr_widgets['ip_cam_input'].setEnabled(False)
        self.alpr_widgets['validate_button'].setEnabled(False)

        # Enable browse button
        self.alpr_widgets['browse_btn'].setEnabled(True)

        # Clear the status label
        self.alpr_widgets['status_label'].setText('')

    def set_stream_mode(self):
        """
        Sets the UI to stream mode.

        Side Effects:
            - Changes the UI to stream mode.
            - Enables IP camera input and validate button.
            - Disables browse button.

        """
        # Set the browse mode button style
        self.alpr_widgets['browse_mode'].setStyleSheet(UNSELECT_BTN_STYLE)

        # Set the stream mode button style
        self.alpr_widgets['stream_mode'].setStyleSheet(SELECT_BTN_STYLE)

        # Enable IP camera input and validate button
        self.alpr_widgets['ip_cam_input'].setEnabled(True)
        self.alpr_widgets['validate_button'].setEnabled(True)

        # Disable browse button
        self.alpr_widgets['browse_btn'].setEnabled(False)

    def export(self):
        """
        Export the data in the table to an Excel file.

        Displays a file dialog to prompt the user to select a location to save the Excel file.
        The data from the table is then extracted and stored in a Pandas DataFrame which is
        then saved to the specified file location.

        """
        # Set options for file dialog
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Create file dialog and set default directory
        dialog = QFileDialog()
        dialog.setDirectory('data')

        # Get file path from user and check for valid file extension
        file_path, _ = dialog.getSaveFileName(self, 'Export Table', '', 'Excel files (*.xlsx)',
                                              options=options)
        if file_path and file_path != '':
            temp = file_path.split('.')
            if len(temp) == 2 and temp[-1] == "xlsx":
                pass
            elif len(temp) == 1:
                file_path += '.xlsx'
            else:
                file_path = None

        if file_path is not None:
            # Extract data from table
            num_rows = self.table.rowCount()
            time_stamp = []
            license_plate = []
            conf = []
            camera = []
            for i in range(num_rows - 1, -1, -1):
                time_stamp.append(self.table.item(i, 2).text())
                license_plate.append(self.table.item(i, 3).text())
                conf.append(self.table.item(i, 4).text())
                camera.append(self.table.item(i, 5).text())

            # Create dictionary and DataFrame of extracted data
            data = {"Time": time_stamp,
                    "LICENSE PLATE": license_plate,
                    "CL": conf,
                    "CAMERA": camera}
            df = pd.DataFrame(data)

            # Save the data to the Excel file
            df.to_excel(file_path)

    def validate_ip_cam(self):
        """
        Validates the input IP camera address and starts a video thread to stream from the camera.

        This function reads the IP camera address from the `ip_cam_input` text field and creates
        a VideoCapture object to read from the IP camera. If the camera is successfully connected
        and a frame can be read from it, the function updates the `status_label` to indicate that
        the IP camera address is valid and starts a video thread to stream from the camera.
        If the camera cannot be connected or a frame cannot be read from it, the function updates
        the `status_label` to indicate that the IP camera address is invalid.

        """
        # Get IP camera address from input
        ip_cam_address = self.ip_cam_input.text()

        try:
            # construct IP camera address with "https" protocol and "/video" endpoint
            ip_cam_address = 'https://' + ip_cam_address + '/video'
            # create a VideoCapture object to read from the IP camera
            cap = cv2.VideoCapture(ip_cam_address)

            # Check if the camera was successfully connected
            if not cap.isOpened():
                self.alpr_widgets['status_label'].setText('IP Camera address is invalid.')
            else:

                ret, _ = cap.read()

                # Check if the frame was successfully read
                if not ret:
                    self.alpr_widgets['status_label'].setText('IP Camera address is invalid.')
                else:
                    self.alpr_widgets['status_label'].setText('Success! \
                        IP Camera address is valid.')

                # Release the VideoCapture object and close the window
                cap.release()
                cv2.destroyAllWindows()
                self.file = ip_cam_address
                self.file_type = "Live Stream"
                self.start_video_thread(ip_cam_address)

        except cv2.error:
            # handle the exception raised by cv2 if IP camera address is invalid
            self.alpr_widgets['status_label'].setText('IP Camera address is invalid.')

    def start_video_thread(self, capture, mode=0, ocr=None):
        """
        Starts a new thread to capture video frames from the specified capture device,
        with the given mode and OCR settings.

        Args:
            capture (cv2.VideoCapture): The capture path to use for inmage/video/stream input.
            mode (int, optional): The mode to use for video processing (default 0).
            ocr (OCR, optional): The OCR engine to use for text recognition (default None).

        Side Effects:
            - Stops any currently running video thread.
            - Creates a new VideoThread object with the specified settings.
            - Sets the play button icon to the "play" icon.
            - Connects the change_pixmap_signal and add_row_signal signals to the update_image()
                and add_row() functions, respectively.
            - Starts the new thread.

        """
        # Stop any currently running video thread
        self.stop_video_thread()

        # Create a new VideoThread object with the specified settings
        self.stream = VideoThread(capture, mode=mode, ocr=ocr)

        # Set the play button icon to the "pause" icon
        self.alpr_widgets['play_btn'].setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        # Connect the signals functions
        self.stream.change_pixmap_signal.connect(self.update_image)
        self.stream.add_row_signal.connect(self.add_row)

        # Start the new thread
        self.stream.start()

        # Enable/disable the start/stop processing buttons based on the mode
        if mode == 0:
            self.alpr_widgets['start_processing_btn'].setEnabled(True)
            self.alpr_widgets['stop_processing_btn'].setEnabled(False)
        else:
            self.alpr_widgets['start_processing_btn'].setEnabled(False)
            self.alpr_widgets['stop_processing_btn'].setEnabled(True)

    def stop_video_thread(self):
        """
        Stops the video thread and resets the GUI.

        """
        # Check if the video thread is running
        if self.stream is not None:
            if self.stream.isRunning():
                # Stop the thread
                self.stream.stop()

        # Disable the stop processing button
        self.alpr_widgets['stop_processing_btn'].setEnabled(False)

        # Reset the image in the video stream widget to the default image
        cv_img = cv2.imread(DEFAULT_IMG_PATH)
        qt_img = convert_cv_qt(cv_img)
        self.alpr_widgets['stream'].setPixmap(qt_img)

    def filter(self):
        """
        Filter the data in the table based on user input.

        Retrieves the user input from the filter widgets and constructs a dictionary
        containing the filter criteria.
        Passes the dictionary to the display method of the table object to filter the
        data and display the results.

        """

        # Construct filter dictionary
        filter_dict = {'LICENSE': self.license_input.text(), 'SCORE': self.score_input.text(),
                       'FROM': self.date_from_picker.date().toString("yyyy-MM-dd"),
                       'TO': self.date_to_picker.date().toString("yyyy-MM-dd"),
                       'MEDIA': self.media_type_combo.currentText()}

        # Pass the filter dictionary to the display method of the table object.
        self.table.display(filter_dict=filter_dict, mode='filter')

    def open_file(self):
        """
        Open a file dialog to select a file and determine its type.

        """
        # Open a file dialog to select a file
        self.file = QFileDialog.getOpenFileName(self, "Select File")[0]

        if self.file is not None and self.file != '':
            # Determine the MIME type of the selected file
            mime_type = magic.from_file(self.file, mime=True)
            self.file_type = None
            if mime_type.startswith('image/'):
                self.file_type = "Image"
            elif mime_type.startswith('video/'):
                self.file_type = "Video"
            # If the file is an image or a video, start the video thread
            if self.file_type is not None:
                self.start_video_thread(self.file)

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """
        Slot function that updates the image on the GUI with a new OpenCV image.

        Args:
            cv_img (np.ndarray): An OpenCV image.

        """
        # Convert the OpenCV image to a Qt image.
        qt_img = convert_cv_qt(cv_img)

        # Set the Qt image as the pixmap for the stream label.
        self.alpr_widgets['stream'].setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def add_row(self, detections):
        """
        Adds a new row to the table with license plate detection data.

        Args:
        - detections: A list of tuples, where each tuple contains the license plate string,
                    confidence score, and the corresponding license plate image.
        """

        # Get the current time
        ct = datetime.datetime.now().strftime("%B %d, %Y; %I:%M")

        # Define the field names for the CSV file
        field_names = ["Time", "LICENSE PLATE", "CL", "CAMERA"]

        # Iterate through the detections and add a row for each one
        for detection in detections:
            # Check if the license plate is already in the table
            if not check_duplicate(detection[0]):
                # Save the license plate image to disk
                cv2.imwrite(f'license_plates/{detection[0]}.jpg', detection[2])

                # Set the file type based on whether it's an image or video
                self.file_type = "Image" if self.file_type is None else self.file_type

                # Create a dictionary with the detection data
                temp = {"Time": ct,
                        "LICENSE PLATE": detection[0],
                        "CL": '{:.4f}'.format(detection[1]),
                        "CAMERA": self.file_type}

                # Write the data to the CSV file
                with open(DATA_PATH, 'a', encoding="utf-8") as csv_file:
                    dict_object = csv.DictWriter(csv_file, fieldnames=field_names)
                    dict_object.writerow(temp)

                # Update the table display
                self.table.display()

    def closeEvent(self, event):
        """
        Overrides the default close event handler.

        Stops the video thread and prints a message to the console.

        Args:
        - event (QCloseEvent): The close event to handle.
        """
        # stop the video thread
        self.stop_video_thread()
        print('Close Event')
        # accept the close event
        event.accept()
