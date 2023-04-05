"""
This file contains the definition of the VideoThread class, which is a QThread subclass
that handles the processing of video streams. It emits signals to update the GUI with the current
frame of the video, and it can also process the frames with OCR and emit signals with the
detected text.

Attributes:
    change_pixmap_signal (pyqtSignal): A signal that is emitted when a new frame is available
    to be displayed in the GUI.
    add_row_signal (pyqtSignal): A signal that is emitted when OCR detects text in a frame,
    with a ndarray argument containing the detections.

Methods:
    __init__(self, capture, mode=0, ocr=None): Initializes the object with the video capture object,
    the processing mode (default 0 for no OCR), and an OCR object if OCR is enabled.
    run(self): The main processing loop of the thread. It reads frames from the video capture object
    and emits signals to update the GUI and/or add detected text to a table.
    stop(self): Stops the thread by setting the run flag to False and waiting for the thread to
    finish.

Example usage:

    # Create a VideoThread object with a video file path and an OCR object
    vt = VideoThread('/path/to/video.mp4', mode=1, ocr=my_ocr_object)

    # Connect the signals to update the GUI
    vt.change_pixmap_signal.connect(my_gui_object.update_image)
    vt.add_row_signal.connect(my_gui_object.update_table)

    # Start the thread and wait for it to finish
    vt.start()
    vt.wait()
"""
import time
import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread


class VideoThread(QThread):
    """
    This class extends QThread and provides a threaded interface for capturing and
    displaying video frames.

    Attributes:
        change_pixmap_signal (pyqtSignal): PyQt signal emitted when a new video frame is available.
        add_row_signal (pyqtSignal): PyQt signal emitted when OCR text is detected in a video frame.

    Args:
        capture (str): The path to the image/video/stream file to be processed.
        mode (int): The processing mode to be used: 0 for display-only, 1 for OCR.
        ocr (OCR): Optional OCR object to be used for detecting text in video frames.
    """
    change_pixmap_signal = pyqtSignal(np.ndarray)
    add_row_signal = pyqtSignal(np.ndarray)

    def __init__(self, capture, mode=0, ocr=None):
        super().__init__()

        # Set up instance variables
        self._run_flag = True
        self.play = True
        self.mutex = False
        self.delay = 0.01
        self.capture = capture
        self.mode = mode
        self.ocr = ocr
        self.filename = capture.split('/')[-1]
        self.cap = cv2.VideoCapture(capture)

        # Set the delay between frames based on the video's FPS (if available)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps > 0:
            self.delay = self.delay * (60 / fps)

        # Set the lower and upper frame limits based on the video's frame count
        self.lower_limit, self.curr_frame, self.upper_limit = \
            0, 0, int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1

    def run(self):
        """
        Starts the video processing loop in a separate thread.

        If mode is 0 (no OCR), updates the GUI with the current frame.
        If mode is 1 (OCR), processes the frame with OCR and updates the GUI and/or table.
        """
        # Main processing loop
        while self._run_flag:
            # If mode 0 (no OCR), update the GUI with the current frame
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

            # If mode 1 (OCR), process the frame with OCR and update the GUI and/or table
            elif self.mode == 1:
                if self.curr_frame <= self.upper_limit and self.play:
                    if not self.mutex:
                        self.mutex = True
                        ret, image = self.cap.read()
                        if ret:

                            image, detections = self.ocr.process_image(image)
                            if len(detections) != 0:
                                self.add_row_signal.emit(detections)

                            self.change_pixmap_signal.emit(image)
                        self.curr_frame += 1
                        self.mutex = False
        self.cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
