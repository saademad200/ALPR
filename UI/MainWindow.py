from PyQt5.QtWidgets import QStyle, QFileDialog, QMainWindow
from PyQt5.QtCore import pyqtSlot
import magic
import cv2
import csv
import numpy as np
from UI.model import ANPR
from UI.VideoThread import VideoThread
from UI.utils import convert_cv_qt, play_video, check_duplicate
import pandas as pd
from UI.InitializeTabs import InitializeTabs
from constants import DEFAULT_IMG_PATH, DATA_PATH
import datetime
from UI.styles import select_btn_style, unselect_btn_style

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.thread = None
        self.file = None
        self.file_type = None
        #self.setFixedSize(1500, 900)
        self.setWindowTitle("Ronicom")
        self.initialize_ui()
        self.ocr = ANPR()
        
    def initialize_ui(self):

        tab_widget = InitializeTabs(self)

        # Central Widgets
        self.central_widget = tab_widget.get_central_widget()

        self.start_processing_btn, self.stop_processing_btn, self.browse_btn, self.play_btn, self.browse_mode, self.stream_mode, \
            self.validate_button, self.status_label, self.ipcam_input, self.stream = tab_widget.initialize_anpr_content()
        self.export_btn, self.reset_btn, self.license_input, self.score_input, self.media_type_combo, self.date_from_picker,self.date_to_picker, self.filter_button, self.table = tab_widget.initialize_report_content()

        # Connect button signals to slots

        self.start_processing_btn.clicked.connect(self.start_processing)
        self.stop_processing_btn.clicked.connect(self.stop_video_thread)
        self.browse_btn.clicked.connect(self.open_file)
        self.play_btn.clicked.connect(lambda: play_video(self, self.thread, self.play_btn))
        #self.toggle_button.clicked.connect(self.toggle_input)
        self.validate_button.clicked.connect(self.validate_ipcam)

        self.export_btn.clicked.connect(self.export)
        self.reset_btn.clicked.connect(self.table.reset)
        self.filter_button.clicked.connect(self.filter)

        self.browse_mode.clicked.connect(self.set_browse_mode)
        self.stream_mode.clicked.connect(self.set_stream_mode)
        
        # Set initial state of IP Camera input
        #self.toggle_input()
        
        self.setCentralWidget(self.central_widget)
        self.stop_video_thread()

    def set_browse_mode(self):
        self.browse_mode.setStyleSheet(select_btn_style)
        self.stream_mode.setStyleSheet(unselect_btn_style)
        self.ipcam_input.setEnabled(False)
        self.validate_button.setEnabled(False)
        self.browse_btn.setEnabled(True)
        self.status_label.setText('')
        

    def set_stream_mode(self):
        self.browse_mode.setStyleSheet(unselect_btn_style)
        self.stream_mode.setStyleSheet(select_btn_style)
        self.ipcam_input.setEnabled(True)
        self.validate_button.setEnabled(True)
        self.browse_btn.setEnabled(False)
        
    def export(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dialog = QFileDialog()
        dialog.setDirectory('data')
        file_path, _ = dialog.getSaveFileName(self, 'Export Table', '', 'Excel files (*.xlsx)', options=options)
        if file_path and file_path != '':
            print("File saved as:", file_path)
            temp = file_path.split('.')
            if len(temp) == 2 and temp[-1] == "xlsx":
                pass
            elif len(temp) == 1:
                file_path += '.xlsx'
            else:
                file_path = None

        if file_path is not None:  
            num_rows = self.table.rowCount()    
            ["Time", "LICENSE PLATE", "CL", "CAMERA"]      
            time_stamp = []
            license_plate = []
            conf = []
            camera = []
            for i in range(num_rows-1, -1,-1):
                time_stamp.append(self.table.item(i,2).text())
                license_plate.append(self.table.item(i,3).text())
                conf.append(self.table.item(i,4).text())
                camera.append(self.table.item(i,5).text())

            data = {"Time": time_stamp,
                    "LICENSE PLATE": license_plate,
                    "CL": conf,
                    "CAMERA":camera}
            df = pd.DataFrame(data)

            # Save the data to the Excel file
            df.to_excel(file_path)
        
    def validate_ipcam(self):
        # Get IP camera address from input
        ipcam_address = self.ipcam_input.text()

        try:
            # Create a VideoCapture object to read from the IP camera
            ipcam_address = 'https://' + ipcam_address + '/video'
            cap = cv2.VideoCapture(ipcam_address)

            # Check if the camera was successfully connected
            if not cap.isOpened():
                print('not connected')
                self.status_label.setText('IP Camera address is invalid.')
            else:
                # Read a frame from the camera
                ret, frame = cap.read()

                # Check if the frame was successfully read
                if not ret:
                    self.status_label.setText('IP Camera address is invalid.')
                else:
                    self.status_label.setText('Success! IP Camera address is valid.')

                # Release the VideoCapture object and close the window
                cap.release()
                cv2.destroyAllWindows()
                self.file = ipcam_address
                self.file_type = "Live Stream"
                self.start_video_thread(ipcam_address)
        except:
            self.status_label.setText('IP Camera address is invalid.')

        
    def start_video_thread(self, capture, mode=0, ocr=None):
        self.stop_video_thread()
        self.thread = VideoThread(capture, mode=mode, ocr=ocr)
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.add_row_signal.connect(self.add_row)
        self.thread.start()
        if mode == 0:
            self.start_processing_btn.setEnabled(True)
            self.stop_processing_btn.setEnabled(False)
        else:
            self.start_processing_btn.setEnabled(False)
            self.stop_processing_btn.setEnabled(True)


    def stop_video_thread(self):
        if self.thread is not None:
            if self.thread.isRunning():
                self.thread.stop()
        self.stop_processing_btn.setEnabled(False)
        cv_img = cv2.imread(DEFAULT_IMG_PATH)
        qt_img = convert_cv_qt(cv_img)
        self.stream.setPixmap(qt_img)
    
    def filter(self):
        filter_dict = {}
        filter_dict['LICENSE'] = self.license_input.text()
        filter_dict['SCORE'] = self.score_input.text()
        filter_dict['FROM'] = self.date_from_picker.date().toString("yyyy-MM-dd")
        filter_dict['TO'] = self.date_to_picker.date().toString("yyyy-MM-dd")
        filter_dict['MEDIA'] = self.media_type_combo.currentText()
        self.table.display(filter_dict=filter_dict, mode='filter')
        
    def start_processing(self):
        self.start_video_thread(self.file, mode = 1, ocr = self.ocr)
        
    def open_file(self):
        self.file = QFileDialog.getOpenFileName(self, "Select File")[0]
        
        if self.file is not None and self.file != '':
            
            mime_type = magic.from_file(self.file, mime=True)
            self.file_type = None
            if mime_type.startswith('image/'):
                self.file_type = "Image"
            elif mime_type.startswith('video/'):
                self.file_type = "Video"
            if self.file_type is not None:
                self.start_video_thread(self.file)
                        
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        self.stream.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def add_row(self, detections):
        ct = datetime.datetime.now().strftime("%B %d, %Y; %I:%M")
        field_names = ["Time", "LICENSE PLATE", "CL", "CAMERA"]
                
        for detection in detections:
            if not check_duplicate(detection[0]):
                cv2.imwrite(f'license_plates/{detection[0]}.jpg', detection[2])
                self.file_type = "Image" if self.file_type is None else self.file_type
                temp = {"Time": ct, "LICENSE PLATE": detection[0], "CL":'{:.3f}'.format(detection[1]), "CAMERA": self.file_type}

                with open(DATA_PATH, 'a') as csv_file:
                    dict_object = csv.DictWriter(csv_file, fieldnames=field_names) 
                    dict_object.writerow(temp)
                self.table.display()
        
    def closeEvent(self, event):
        self.stop_video_thread()
        print('Close Event')
        event.accept()
