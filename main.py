"""
This module initializes and runs the license plate manager application.

The license plate manager application allows users to add, view, filter, and
delete license plate entries. The application uses a CSV file to store the license plate data.

The main entry point for the application is the `MainWindow` class from the `UI.main_window` module.
The application creates an instance of the `MainWindow` class and sets the application icon.
The `MainWindow` instance is then shown and the application event loop is started.

Example:
    To run the application, execute the following command:

        $ python main.py

Attributes:
    basedir (str): The base directory of the module.
    app (QApplication): The instance of the PyQt5 application.
    win (MainWindow): The instance of the main window for the application.

"""
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from user_interface.main_window import MainWindow
from constants import ICON_PATH

basedir = os.path.dirname(__file__)

app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, ICON_PATH)))
win = MainWindow()
win.show()
sys.exit(app.exec_())
