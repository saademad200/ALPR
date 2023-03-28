from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtWidgets import QPushButton


class AnimatedToggle(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(64)
        self.setMinimumHeight(36)
        self.setMaximumHeight(36)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)

    def toggle(self):
        if self.isChecked():
            self.animation.setStartValue(QRect(self.width()-self.height(), 0, self.height(), self.height()))
            self.animation.setEndValue(QRect(0, 0, self.height(), self.height()))
            self.animation.start()
        else:
            self.animation.setStartValue(QRect(0, 0, self.height(), self.height()))
            self.animation.setEndValue(QRect(self.width()-self.height(), 0, self.height(), self.height()))
            self.animation.start()
        super().toggle()
