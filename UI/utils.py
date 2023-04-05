import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QStyle
from typing import List
import numpy as np
import csv
import os
from constants import DATA_PATH


def crop_image(image: np.ndarray, coord: List[int]) -> np.ndarray:
    return image[coord[1]: coord[3], coord[0]: coord[2]]


def fetch_data():
    data = []
    
    file_exists = os.path.exists(DATA_PATH)
    if file_exists:
        with open(DATA_PATH, 'r') as f:
            reader = csv.reader(f)
            data = [row for row in reader][::-1]
    else:
        with open(DATA_PATH, mode='w', newline='') as file:
            file.write('')

    return data


def media_player(central_widget):
    stream = QtWidgets.QLabel(central_widget)
    stream.resize(1280, 720)
    stream.setAlignment(Qt.AlignCenter)
    return stream


def resize_image(image):
    # Get the original dimensions of the image
    height, width = image.shape[:2]

    # Calculate the aspect ratio of the image
    aspect_ratio = width / height

    # Calculate the new dimensions based on the target width
    target_width = 1280
    target_height = 720
    
    if aspect_ratio >= target_width / target_height:
        # Calculate the new height based on the target width and the aspect ratio
        new_height = int(target_width / aspect_ratio)

        # Resize the image using the calculated dimensions
        resized_image = cv2.resize(image, (target_width, new_height))

        # Add black padding to the top and bottom of the image
        padding_top = int((target_height - new_height) / 2)
        padding_bottom = target_height - new_height - padding_top
        resized_image = cv2.copyMakeBorder(resized_image, padding_top, padding_bottom, 0, 0, cv2.BORDER_CONSTANT,
                                           value=0)

    else:
        # Calculate the new width based on the target height and the aspect ratio
        new_width = int(target_height * aspect_ratio)

        # Resize the image using the calculated dimensions
        resized_image = cv2.resize(image, (new_width, target_height))

        # Add black padding to the left and right of the image
        padding_left = int((target_width - new_width) / 2)
        padding_right = target_width - new_width - padding_left
        resized_image = cv2.copyMakeBorder(resized_image, 0, 0, padding_left, padding_right, cv2.BORDER_CONSTANT,
                                           value=0)

    # Return the resized image
    return resized_image


def check_duplicate(a):
    try:
        with open(DATA_PATH, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == a:
                    return True
        return False
    except Exception as e:
        print(f"Exception {e}")
        return True


def convert_cv_qt(cv_img):

    """Convert from an opencv image to QPixmap"""
    cv_img = resize_image(cv_img)
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    return QPixmap.fromImage(convert_to_qt_format)


def convert_license_plate_image(license_plate):
    """Convert from an opencv image to QPixmap"""
    cv_img = cv2.imread(f'license_plates/{license_plate}.jpg')
    cv_img = cv2.resize(cv_img, (400, 250), interpolation=cv2.INTER_NEAREST)
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    return QPixmap.fromImage(convert_to_qt_format)


def play_video(obj, thread, play_btn):
    if thread is not None:
        if thread.isRunning():
            if thread.play:
                thread.play = False
                play_btn.setIcon(obj.style().standardIcon(QStyle.SP_MediaPlay))
            else:
                thread.play = True
                play_btn.setIcon(obj.style().standardIcon(QStyle.SP_MediaPause))
