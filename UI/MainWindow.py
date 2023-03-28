from PyQt5.QtWidgets import QStyle, QFileDialog, QMainWindow,  QTabWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSlot, Qt
import cv2
import csv
import numpy as np
from model.model import ANPR
from UI.VideoThread import VideoThread
from UI.utils import convert_cv_qt, play_video, check_duplicate
import re
import pandas as pd
from UI.InitializeTabs import InitializeTabs
from constants import DEFAULT_IMG_PATH, DATA_PATH

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.thread = None
        self.file = None
        self.setFixedSize(1500, 900)
        self.setWindowTitle("Ronicom")
        self.initialize_ui()
        self.ocr = ANPR()
        
    def initialize_ui(self):

        tab_widget = InitializeTabs(self)

        # Central Widgets
        self.central_widget = tab_widget.get_central_widget()

        # Table
        self.table = tab_widget.get_table()

        self.start_processing_btn, self.stop_processing_btn, self.browse_btn, self.play_btn, self.toggle_button, \
            self.validate_button, self.status_label, self.ipcam_input, self.stream = tab_widget.initialize_anpr_content()
        self.export_btn, self.reset_btn, self.search_input, self.search_button = tab_widget.initialize_report_content()

        # Connect button signals to slots

        self.start_processing_btn.clicked.connect(self.start_processing)
        self.stop_processing_btn.clicked.connect(self.stop_video_thread)
        self.browse_btn.clicked.connect(self.open_file)
        self.play_btn.clicked.connect(lambda: play_video(self, self.thread, self.play_btn))
        self.toggle_button.clicked.connect(self.toggle_input)
        self.validate_button.clicked.connect(self.validate_ipcam)

        self.export_btn.clicked.connect(self.export)
        self.reset_btn.clicked.connect(self.table.reset)
        self.search_button.clicked.connect(self.search)

        # Set initial state of IP Camera input
        self.toggle_input()

        self.setCentralWidget(self.central_widget)
        self.stop_video_thread()
        
    def toggle_input(self):
        if self.toggle_button.isChecked():
            self.ipcam_input.setEnabled(True)
            self.validate_button.setEnabled(True)
            self.browse_btn.setEnabled(False)
            self.toggle_button.setText("LIVE STREAM MODE")
            self.toggle_button.setStyleSheet("""
                font-size: 14px;
                padding: 8px;
                border: none;
                border-radius: 18px;
                color: #fff;
                background-color: #2ecc71;
            """)
        else:
            self.ipcam_input.setEnabled(False)
            self.validate_button.setEnabled(False)
            self.browse_btn.setEnabled(True)
            self.status_label.setText('')
            self.toggle_button.setText("BROWSE MODE")
            self.toggle_button.setStyleSheet("""
                font-size: 14px;
                padding: 8px;
                border: none;
                border-radius: 18px;
                color: #fff;
                background-color: #e74c3c;
            """)

    def export(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, 'Export Table', '', 'Excel files (*.xlsx)', options=options)
        if file_path:
            print("File saved as:", file_path)
            temp = file_path.split('.')
            if len(temp) == 2 and temp[-1] == "xlsx":
                pass
            elif len(temp) == 1:
                file_path += '.xlsx'
            else:
                file_path = None

        if file_path is not None:            
            text = self.search_input.text()
            try:
                with open(DATA_PATH, 'r') as f:
                    reader = csv.reader(f)
                    data = [row for row in reader][::-1]
                    if text is not None:
                        temp = []
                        for row in data:
                            for elem in row:
                                if text in elem:
                                    temp.append(row)
                                    break
                data_transposed = list(zip(*temp))
                data = {"FILE NAME": list(data_transposed[0]),
                        "NUMBER PLATE TEXT": list(data_transposed[1]),
                        "TIME STAMP": list(data_transposed[2])}
                df = pd.DataFrame(data)

                # Save the data to the Excel file
                df.to_excel(file_path)
            except:
                pass

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
                # self.file = ipcam_address
                # self.start_video_thread(ipcam_address)
        except:
            self.status_label.setText('IP Camera address is invalid.')

        
    def start_video_thread(self, capture, mode=0, ocr=None):
        self.stop_video_thread()
        self.thread = VideoThread(capture, mode, ocr)
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.add_row_signal.connect(self.add_row)
        self.thread.start()

    def stop_video_thread(self):
        if self.thread is not None:
            if self.thread.isRunning():
                self.thread.stop()

        cv_img = cv2.imread(DEFAULT_IMG_PATH)
        qt_img = convert_cv_qt(cv_img)
        self.stream.setPixmap(qt_img)
    
    def search(self):
        text = self.search_input.text()
        self.table.display(text=text)
        
    def start_processing(self):
        self.start_video_thread(self.file, 1, self.ocr)

    def open_file(self):
        self.file = QFileDialog.getOpenFileName(self, "Select File")[0]
        if self.file is not None:
            self.start_video_thread(self.file)

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        self.stream.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def add_row(self, row):
        txts = row[1]
        for txt in txts:
            if check_duplicate(row[0], txt):
                field_names = ["FILE NAME", "NUMBER PLATE TEXT", "TIME STAMP"]
                temp = {"FILE NAME": row[0], "NUMBER PLATE TEXT": txt, "TIME STAMP": row[2]}

                with open(DATA_PATH, 'a') as csv_file:
                    dict_object = csv.DictWriter(csv_file, fieldnames=field_names) 
                    dict_object.writerow(temp)
                self.table.display()
        
    def closeEvent(self, event):
        self.stop_video_thread()
        print('Close Event')
        event.accept()
