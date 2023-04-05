"""
Module containing various constants used in the application.

Attributes:
    MODEL_PATH (str): The path to the trained model weights file.
    ICON_PATH (str): The path to the application icon.
    DEFAULT_IMG_PATH (str): The path to the default image file.
    DATA_PATH (str): The path to the data file.
    THRESHOLD (float): The confidence threshold for object detection.
"""
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

MODEL_PATH = config['DEFAULT']['MODEL_PATH']
ICON_PATH = config['DEFAULT']['ICON_PATH']
DEFAULT_IMG_PATH = config['DEFAULT']['DEFAULT_IMG_PATH']
DATA_PATH = config['DEFAULT']['DATA_PATH']
THRESHOLD = config['DEFAULT'].getfloat('THRESHOLD')
