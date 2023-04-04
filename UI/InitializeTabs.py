
from PyQt5.QtWidgets import QStyle,  QTabWidget, QPushButton, QLabel, QLineEdit, QDateEdit, QComboBox
from PyQt5 import QtWidgets, QtCore, QtGui
from UI.table import TableWidget
from UI.utils import media_player, fetch_data
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate, Qt
from UI.styles import button_style, search_input_style, label_style, combobox_style, title_style, start_processing_btn_style, stop_processing_btn_style ,\
    browse_btn_style, play_btn_style, ip_label_style, ipcam_input_style, status_label_style, validate_button_style, export_btn_style, reset_btn_style, \
        unselect_btn_style



class InitializeTabs:
    def __init__(self, obj):
        # Central Widgets
        self.obj = obj
        self.central_widget = QTabWidget()
        
        # Central Widgets
        self.central_widget = QTabWidget()
        
        self.tab1 = QtWidgets.QWidget(self.central_widget)
        self.tab2 = QtWidgets.QWidget(self.central_widget)
        self.central_widget.addTab(self.tab1, "ALPR")
        self.central_widget.addTab(self.tab2, "VIEW REPORTS")

    def initialize_anpr_content(self):
        gridLayout_4 = QtWidgets.QGridLayout(self.tab1)
        
        # Title
        title = QtWidgets.QLabel(self.tab1)
        title.setAlignment(Qt.AlignHCenter)
        title.setText('Ronicom')
        title.setStyleSheet(title_style)

        start_processing_btn = QtWidgets.QPushButton(self.tab1)
        start_processing_btn.setEnabled(False)
        start_processing_btn.setFixedSize(QtCore.QSize(200, 70))
        start_processing_btn.setStyleSheet(start_processing_btn_style)
        start_processing_btn.setText("Start Processing")

        stop_processing_btn = QtWidgets.QPushButton(self.tab1)
        stop_processing_btn.setEnabled(False)
        stop_processing_btn.setFixedSize(QtCore.QSize(200, 70))
        stop_processing_btn.setStyleSheet(stop_processing_btn_style)
        stop_processing_btn.setText("Stop Processing")

        # Media Buttons
        browse_btn = QtWidgets.QPushButton(self.obj)
        browse_btn.setFixedSize(QtCore.QSize(200, 70))
        browse_btn.setText('Browse')
        browse_btn.setStyleSheet(browse_btn_style)

        play_btn = QtWidgets.QPushButton(self.obj)
        play_btn.setIcon(self.obj.style().standardIcon(QStyle.SP_MediaPlay))
        play_btn.setStyleSheet(play_btn_style)

        # Media Player
        stream = media_player(self.tab1)

        # Line
        line = QtWidgets.QFrame(self.tab1)
        line.setLineWidth(3)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Spacer
        vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # Set font styles for labels
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
                
        # Create UI elements
        ipcam_label = QLabel('Enter IP Camera Address:')
        ipcam_label.setStyleSheet(ip_label_style)
        ipcam_label.setFont(font)

        ipcam_input = QLineEdit()
        ipcam_input.setStyleSheet(ipcam_input_style)

        browse_mode = QPushButton("Browse Mode")
        stream_mode = QPushButton("Stream Mode")
        browse_mode.setStyleSheet(unselect_btn_style)    
        stream_mode.setStyleSheet(unselect_btn_style)      
        
        status_label = QLabel('')
        status_label.setStyleSheet(status_label_style)
        status_label.setFont(font)

        validate_button = QPushButton('Validate IP CAM')
        validate_button.setStyleSheet(validate_button_style)

        ipcam_input.setEnabled(False)
        validate_button.setEnabled(False)
        browse_btn.setEnabled(False)
        
        # Place items in the bottom media player layout
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        horizontalLayout_3 = QtWidgets.QHBoxLayout()
        
        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout_2 = QtWidgets.QVBoxLayout()
        verticalLayout_3 = QtWidgets.QVBoxLayout()
        
        gridLayout = QtWidgets.QGridLayout()
        gridLayout_2 = QtWidgets.QGridLayout()
        gridLayout_3 = QtWidgets.QGridLayout()

        horizontalLayout_3.addWidget(browse_mode)
        horizontalLayout_3.addWidget(stream_mode)        

        horizontalLayout_2.addWidget(play_btn)
        verticalLayout.addWidget(stream)
        verticalLayout.addLayout(horizontalLayout_2)
        verticalLayout_2.addItem(vertical_spacer)
        verticalLayout_2.addLayout(horizontalLayout_3)
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

        return start_processing_btn, stop_processing_btn, browse_btn, play_btn, browse_mode, stream_mode, validate_button,\
            status_label, ipcam_input, stream
    
    def initialize_report_content(self):
        # create table 
        table = TableWidget(fetch_data())

        # Create components
        title_label = QtWidgets.QLabel('Filter Search Results', self.obj)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet(title_style)

        export_btn = QtWidgets.QPushButton('Export Table', self.obj)
        export_btn.setFixedSize(QtCore.QSize(120, 35))
        export_btn.setStyleSheet(export_btn_style)

        reset_btn = QtWidgets.QPushButton('Reset Table', self.obj)
        reset_btn.setStyleSheet(reset_btn_style)
        reset_btn.setFixedSize(QtCore.QSize(120, 40))

        license_label = QLabel('License Plate:', self.obj)
        license_label.setStyleSheet(label_style)
        license_input = QLineEdit( self.obj)
        license_input.setPlaceholderText('License Plate')
        license_input.setStyleSheet(search_input_style)
                
        date_label = QLabel('Date Range:', self.obj)
        date_label.setStyleSheet(label_style)
        date_from_picker = DatePicker() 
        date_from_picker.setDate(QDate.currentDate().addDays(-8))       
        date_to_picker = DatePicker()
        date_to_picker.setDate(QDate.currentDate().addDays(2))
        
        media_label = QLabel('Camera:', self.obj)
        media_label.setStyleSheet(label_style)
        media_type_combo = QComboBox()
        media_type_combo.addItems(["All","Image", "Video", "Live Stream"])
        media_type_combo.setStyleSheet(combobox_style)

        score_label = QLabel('Score:', self.obj)
        score_label.setStyleSheet(label_style)
        score_input = QLineEdit()
        score_input.setPlaceholderText("Score")
        score_input.setValidator(QtGui.QDoubleValidator(0, 1, 3))
        score_input.setStyleSheet(search_input_style)

        filter_button = QPushButton("Filter")
        filter_button.setStyleSheet(button_style)

        # Spacer
        horizontal_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        # Layouts
        gridLayout = QtWidgets.QGridLayout(self.tab2)
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        verticalLayout = QtWidgets.QVBoxLayout()
        
        horizontalLayout.setSpacing(5)
        horizontalLayout.addWidget(license_label)
        horizontalLayout.addWidget(license_input)
        horizontalLayout.addWidget(score_label)
        horizontalLayout.addWidget(score_input)
        horizontalLayout.addWidget(media_label)
        horizontalLayout.addWidget(media_type_combo)
        horizontalLayout.addWidget(date_label)
        horizontalLayout.addWidget(date_from_picker)
        horizontalLayout.addWidget(date_to_picker)
        horizontalLayout.addWidget(filter_button)
        horizontalLayout_2.addWidget(export_btn)
        horizontalLayout_2.addItem(horizontal_spacer)
        horizontalLayout_2.addWidget(reset_btn)
        verticalLayout.addLayout(horizontalLayout_2)
        verticalLayout.addWidget(title_label)
        verticalLayout.addLayout(horizontalLayout)
        verticalLayout.addWidget(table)

        gridLayout.addLayout(verticalLayout, 0, 0, 1, 1)
        
        return export_btn, reset_btn, license_input, score_input, media_type_combo, date_from_picker,date_to_picker, filter_button, table

    def get_central_widget(self):
        return self.central_widget

class DatePicker(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(150, 40)
        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy-MM-dd")
        self.setStyleSheet(search_input_style)