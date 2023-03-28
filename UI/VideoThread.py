from PyQt5.QtCore import pyqtSignal, QThread
import cv2
import numpy as np
import datetime
import time


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    add_row_signal = pyqtSignal(np.ndarray)

    def __init__(self, capture, mode=0, ocr=None):
        super().__init__()
        self._run_flag = True
        self.play = True
        self.mutex = False
        self.delay = 0.01
        self.capture = capture
        self.mode = mode
        self.ocr = ocr
        self.filename = capture.split('/')[-1]
        self.cap = cv2.VideoCapture(capture)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps > 0:
            self.delay = self.delay * (60/fps)
        self.lower_limit, self.curr_frame, self.upper_limit = 0, 0, int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1

    def run(self):
        while self._run_flag:
            if self.mode == 0:
                if self.curr_frame <= self.upper_limit and self.play:
                    if not self.mutex:
                        self.mutex = True
                        ret, cv_img = self.cap.read()
                        if ret:
                            self.change_pixmap_signal.emit(cv_img)

                        self.curr_frame += 1
                        self.mutex = False
                        time.sleep(self.delay)
            elif self.mode == 1:
                if self.curr_frame <= self.upper_limit and self.play:
                    if not self.mutex:
                        self.mutex = True
                        ret, image = self.cap.read()
                        if ret:
                            try:
                                image, detections = self.ocr.process_image(image)
                                ct = str(datetime.datetime.now())
                                row = np.array([self.filename, detections, ct])
                                self.add_row_signal.emit(row)                            
                                
                            except:
                                pass
                            self.change_pixmap_signal.emit(image)
                            time.sleep(self.delay)
                                
                        self.curr_frame += 1
                        self.mutex = False
        self.cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
