from UI.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
import os
import sys
from constants import ICON_PATH

basedir = os.path.dirname(__file__)

app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, ICON_PATH)))
win = MainWindow()
win.show()
sys.exit(app.exec_())
