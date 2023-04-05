"""
utils.py - contains utility functions used in the project.

Functions:
- crop_image(image: np.ndarray, coord: List[int]) -> np.ndarray
- fetch_data() -> List[List[str]]
- media_player(central_widget) -> QtWidgets.QLabel
- check_duplicate(a) -> bool
- convert_cv_qt(cv_img) -> QtGui.QPixmap
- convert_license_plate_image(license_plate) -> QtGui.QPixmap
- play_video(obj, thread, play_btn) -> None
- resize_image(image: np.ndarray) -> np.ndarray
- filter_table(data:List[List[str]], filter_dict:dict) -> List[List[str]]

"""
import csv
import os
from datetime import datetime
from typing import List
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyle
from constants import DATA_PATH


def crop_image(image: np.ndarray, coord: List[int]) -> np.ndarray:
    """Crop a given image using the coordinates provided and return the cropped image.

    Args:
        image (np.ndarray): The input image to crop.
        coord (List[int]): A list of 4 integers representing the (x1, y1, x2, y2)
        coordinates of the region to be cropped.

    Returns:
        np.ndarray: The cropped image.
    """
    return image[coord[1]: coord[3], coord[0]: coord[2]]


def fetch_data():
    """Fetch the data from the CSV file.

    Returns:
        List[List[str]]: A list of lists representing the data from the CSV file.
    """
    data = []

    file_exists = os.path.exists(DATA_PATH)
    if file_exists:
        with open(DATA_PATH, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            data = [row for row in reader][::-1]
    else:
        with open(DATA_PATH, mode='w', newline='', encoding="utf-8") as file:
            file.write('')

    return data


def media_player(central_widget):
    """Create and return a media player widget.

    Args:
        central_widget: The parent widget for the media player.

    Returns:
        QtWidgets.QLabel: A QLabel object representing the media player widget.
    """
    stream = QtWidgets.QLabel(central_widget)
    stream.resize(1280, 720)
    stream.setAlignment(Qt.AlignCenter)
    return stream


def check_duplicate(a):
    """
    Checks if a value is already present in a CSV file.
    :param a: The value to check for duplicates.
    :return: True if the value is already present in the CSV file, False otherwise.
    """
    try:
        with open(DATA_PATH, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == a:
                    return True
        return False
    except FileNotFoundError:
        print(f"File not found: {DATA_PATH}")
        return True
    except IOError:
        print(f"Error reading file: {DATA_PATH}")
        return True


def convert_cv_qt(cv_img):
    """
    Converts an OpenCV image to a QPixmap format.
    :param cv_img: The OpenCV image to convert.
    :return: The QPixmap format of the image.
    """
    cv_img = resize_image(cv_img)
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line,
                                        QtGui.QImage.Format_RGB888)
    return QPixmap.fromImage(convert_to_qt_format)


def convert_license_plate_image(license_plate):
    """
    Converts an OpenCV image of a license plate to a QPixmap format.
    :param license_plate: The filename of the license plate image.
    :return: The QPixmap format of the license plate image.
    """
    cv_img = cv2.imread(f'license_plates/{license_plate}.jpg')
    cv_img = cv2.resize(cv_img, (400, 250), interpolation=cv2.INTER_NEAREST)
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line,
                                        QtGui.QImage.Format_RGB888)
    return QPixmap.fromImage(convert_to_qt_format)


def play_video(obj, thread, play_btn):
    """
    Plays or pauses a video being streamed from a thread.
    :param obj: The object from which the function is called.
    :param thread: The thread in which the video is being streamed.
    :param play_btn: The button used to play or pause the video.
    """
    if thread is not None:
        if thread.isRunning():
            if thread.play:
                thread.play = False
                play_btn.setIcon(obj.style().standardIcon(QStyle.SP_MediaPause))


def resize_image(image):
    """
    Resizes an input image to a target size of 1280x720 while maintaining the original aspect ratio.
    If the aspect ratio of the input image is greater than or equal to the aspect ratio of the
    target size, black padding is added to the top and bottom of the resized image. Otherwise,
    black padding is added to the left and right of the resized image.

    Args:
        image (numpy.ndarray): The input image to resize.

    Returns:
        numpy.ndarray: The resized image.
    """
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
        resized_image = cv2.copyMakeBorder(resized_image, padding_top, padding_bottom, 0, 0,
                                           cv2.BORDER_CONSTANT, value=0)

    else:
        # Calculate the new width based on the target height and the aspect ratio
        new_width = int(target_height * aspect_ratio)

        # Resize the image using the calculated dimensions
        resized_image = cv2.resize(image, (new_width, target_height))

        # Add black padding to the left and right of the image
        padding_left = int((target_width - new_width) / 2)
        padding_right = target_width - new_width - padding_left
        resized_image = cv2.copyMakeBorder(resized_image, 0, 0, padding_left, padding_right,
                                           cv2.BORDER_CONSTANT, value=0)

    # Return the resized image
    return resized_image


def filter_table(data, filter_dict):
    """
    Filter the given `data` according to the given `filter_dict`.

    Args:
        data (list): A list of rows where each row is a list of values.
        filter_dict (dict): A dictionary containing filter criteria.

    Returns:
        list: A filtered list of rows where each row is a list of values.

    """
    # Parse the 'FROM' and 'TO' dates
    from_date = parse_date(filter_dict['FROM'])
    to_date = parse_date(filter_dict['TO'])

    # Use list comprehension to filter rows
    filtered_rows = [row for row in data if
                     (filter_dict['LICENSE'] == '' or filter_dict['LICENSE'] in row[1]) &
                     (filter_dict['SCORE'] == '' or float(filter_dict['SCORE']) <= float(row[2])) &
                     (filter_dict['MEDIA'] == 'All' or filter_dict['MEDIA'] == row[3]) &
                     (from_date is None or from_date <= datetime.strptime(row[0],
                                                                          '%B %d, %Y; %H:%M')) &
                     (to_date is None or datetime.strptime(row[0], '%B %d, %Y; %H:%M') <= to_date)]

    return filtered_rows


def parse_date(date_string):
    """
    Convert the given `date_string` into a datetime object.

    Args:
        date_string (str): A string representing a date in YYYY-MM-DD format.

    Returns:
        datetime.datetime: A datetime object representing the given date.

    """
    if not date_string:
        return None

    return datetime.strptime(date_string, '%Y-%m-%d')
