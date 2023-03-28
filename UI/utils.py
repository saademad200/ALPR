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


def resize_image(img):
    # Get the image width and
    try:
        height, width = img.shape[:2]
        # Calculate the new dimensions based on a width of 1280 pixels (720p)
        if width > height:
            new_width = 1280
            new_height = int((1280 / width) * height)
        else:
            new_width = int((720 / height) * width)
            new_height = 720

        # Resize the image while maintaining its aspect ratio
        resized_img = cv2.resize(img, (new_width, new_height))

        # Create a new image with black padding if necessary
        img = cv2.copyMakeBorder(
            resized_img,
            top=int((720 - new_height) / 2),
            bottom=int((720 - new_height) / 2),
            left=int((1280 - new_width) / 2),
            right=int((1280 - new_width) / 2),
            borderType=cv2.BORDER_CONSTANT,
            value=(0, 0, 0)
        )
    except:
        new_width, new_height = 1280, 720
        img = cv2.resize(img, (new_width, new_height))
    return img, new_height, new_width


def check_duplicate(a, b):
    try:
        with open(DATA_PATH, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == a and row[1] == b:
                    return False
        return True
    except Exception as e:
        print(f"Exception {e}")
        return False


def convert_cv_qt(cv_img):

    """Convert from an opencv image to QPixmap"""
    cv_img, _, _ = resize_image(cv_img)
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
