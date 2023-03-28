
from PyQt5.QtWidgets import QStyle, QFileDialog, QMainWindow,  QTabWidget, QPushButton, QLabel, QLineEdit
from PyQt5 import QtWidgets, QtCore
from UI.table import TableWidget
from UI.utils import media_player, fetch_data
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from UI.AnimatedToggle import AnimatedToggle


class InitializeTabs:
    def __init__(self, obj):
        # Central Widgets
        self.obj = obj
        self.central_widget = QTabWidget()
        
        # Central Widgets
        self.central_widget = QTabWidget()
        self.table = TableWidget(fetch_data())

        self.tab1 = QtWidgets.QWidget(self.central_widget)
        self.tab2 = QtWidgets.QWidget(self.central_widget)
        self.central_widget.addTab(self.tab1, "ANPR")
        self.central_widget.addTab(self.tab2, "VIEW REPORTS")

    def initialize_anpr_content(self):
        gridLayout_4 = QtWidgets.QGridLayout(self.tab1)
        
        # Title
        title = QtWidgets.QLabel(self.tab1)
        title.setAlignment(Qt.AlignHCenter)
        title.setText('Ronicom')
        title.setStyleSheet(f"font: 75 bold 25pt \"Yrsa\";")

        start_processing_btn = QtWidgets.QPushButton(self.tab1)
        start_processing_btn.setFixedSize(QtCore.QSize(200, 70))
        start_processing_btn.setStyleSheet(
            "background-color: green; font: 75 italic 18pt \"Yrsa\"; padding: 0.75em 0.5em 0.75em 0.5em;")
        start_processing_btn.setText("Start Processing")

        stop_processing_btn = QtWidgets.QPushButton(self.tab1)
        stop_processing_btn.setFixedSize(QtCore.QSize(200, 70))
        stop_processing_btn.setStyleSheet(
            "background-color: red; font: 75 italic 18pt \"Yrsa\"; padding: 0.75em 0.5em 0.75em 0.5em;")
        stop_processing_btn.setText("Stop Processing")

        # Media Buttons
        browse_btn = QtWidgets.QPushButton(self.obj)
        browse_btn.setFixedSize(QtCore.QSize(200, 70))
        browse_btn.setText('Browse')
        browse_btn.setStyleSheet(
            "font: 75 italic 18pt \"Yrsa\"; background-color: rgb(215, 215, 225); height:28px; ")

        play_btn = QtWidgets.QPushButton(self.obj)
        play_btn.setIcon(self.obj.style().standardIcon(QStyle.SP_MediaPlay))
        play_btn.setStyleSheet(" background-color: rgb(215, 215, 225); height:30px;")

        # Media Player
        stream = media_player(self.tab1)

        # Line
        line = QtWidgets.QFrame(self.tab1)
        line.setLineWidth(3)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Spacer
        vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        
        # Create UI elements
        ipcam_label = QLabel('Enter IP Camera Address:')
        ipcam_input = QLineEdit()

        toggle_button = AnimatedToggle()
        toggle_button.setText("OFF")

        status_label = QLabel('')

        validate_button = QPushButton('Validate IP CAM')

        # Set font styles for labels
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        ipcam_label.setFont(font)
        status_label.setFont(font)

        validate_button.setStyleSheet("""
                    font-size: 12px;
                    padding: 8px 16px;
                    border: 1px solid #2c3e50;
                    border-radius: 5px;
                    color: #fff;
                    background-color: #2c3e50;
                """)

        # Set Style for IPcam Label
        ipcam_label.setStyleSheet("""
                padding: 8px;
                font-size: 12px;
           """)

        # Set Style for IPcam Label
        status_label.setStyleSheet("""
                padding: 8px;
                color: green;
                font-size:10px;

                """)

        # Set styles for QLineEdit
        ipcam_input.setStyleSheet("""
                    font-size: 14px;
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f2f2f2;
                """)

        # Place items in the bottom media player layout
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        
        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout_2 = QtWidgets.QVBoxLayout()
        verticalLayout_3 = QtWidgets.QVBoxLayout()
        
        gridLayout = QtWidgets.QGridLayout()
        gridLayout_2 = QtWidgets.QGridLayout()
        gridLayout_3 = QtWidgets.QGridLayout()

        horizontalLayout_2.addWidget(play_btn)
        verticalLayout.addWidget(stream)
        verticalLayout.addLayout(horizontalLayout_2)
        verticalLayout_2.addItem(vertical_spacer)
        verticalLayout_2.addWidget(toggle_button, alignment=Qt.AlignCenter)
        verticalLayout_2.addWidget(ipcam_label, alignment=Qt.AlignCenter)
        verticalLayout_2.addWidget(ipcam_input, alignment=Qt.AlignCenter)
        verticalLayout_2.addWidget(validate_button, alignment=Qt.AlignCenter)
        verticalLayout_2.addWidget(status_label, alignment=Qt.AlignCenter)
        verticalLayout_2.addWidget(browse_btn, alignment=Qt.AlignCenter)
        verticalLayout_2.addWidget(start_processing_btn, alignment=Qt.AlignCenter)
        verticalLayout_2.addWidget(stop_processing_btn, alignment=Qt.AlignCenter)
        verticalLayout_2.addItem(vertical_spacer)
        verticalLayout_3.addWidget(title)
        gridLayout.addLayout(verticalLayout_2, 4, 0, 25, 1)
        gridLayout_2.addLayout(verticalLayout_3, 0, 1, 1, 1)

        horizontalLayout.addLayout(gridLayout)
        horizontalLayout.addLayout(verticalLayout)

        gridLayout_3.addLayout(horizontalLayout, 2, 0, 1, 1)
        gridLayout_3.addLayout(gridLayout_2, 0, 0, 1, 1)
        gridLayout_3.addWidget(line, 1, 0, 1, 1)

        gridLayout_4.addLayout(gridLayout_3, 0, 0, 1, 1)

        return start_processing_btn, stop_processing_btn, browse_btn, play_btn, toggle_button, validate_button,\
            status_label, ipcam_input, stream
    
    def initialize_report_content(self):
        
        # Create components
        title_label = QLabel('Filter Search Results', self.obj)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 24px; margin-bottom: 20px;')

        export_btn = QPushButton('Export Table', self.obj)
        export_btn.setFixedSize(QtCore.QSize(120, 35))
        export_btn.setStyleSheet(
            'background-color: green;  color: white; font-weight: bold; padding: 10px; border-radius: 5px;')

        reset_btn = QPushButton('Reset Table', self.obj)
        reset_btn.setStyleSheet(
            'background-color: red; color: white; font-weight: bold; padding: 10px; border-radius: 5px;')
        reset_btn.setFixedSize(QtCore.QSize(120, 40))

        search_input = QLineEdit(self.obj)
        search_input.setPlaceholderText('Enter search term...')
        search_input.setStyleSheet('font-size: 16px; padding: 6px; border: 2px solid gray; border-radius: 10px; ')

        search_button = QPushButton('Search', self.obj)
        search_button.setStyleSheet(
            'font-size: 16px; padding: 8px; border-radius: 10px; color: #fff; background-color: #2ecc71;')
        search_button.setFixedSize(QtCore.QSize(120, 40))

        # Spacer
        horizontal_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        # Layouts
        gridLayout = QtWidgets.QGridLayout(self.tab2)
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        verticalLayout = QtWidgets.QVBoxLayout()
        
        horizontalLayout.addWidget(search_input)
        horizontalLayout.addWidget(search_button)
        horizontalLayout_2.addWidget(export_btn)
        horizontalLayout_2.addItem(horizontal_spacer)
        horizontalLayout_2.addWidget(reset_btn)
        verticalLayout.addLayout(horizontalLayout_2)
        verticalLayout.addWidget(title_label)
        verticalLayout.addLayout(horizontalLayout)
        verticalLayout.addWidget(self.table)

        gridLayout.addLayout(verticalLayout, 0, 0, 1, 1)
        
        return export_btn, reset_btn, search_input, search_button

    def get_central_widget(self):
        return self.central_widget

    def get_table(self):
        return self.table
