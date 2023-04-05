from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QStyle,  QTabWidget, QPushButton, QLabel, QLineEdit, QDateEdit, QComboBox
from UI.table import TableWidget
from UI.utils import media_player, fetch_data
from UI.styles import button_style, search_input_style, label_style, combobox_style, title_style, \
    start_processing_btn_style, stop_processing_btn_style, browse_btn_style, play_btn_style, ip_label_style,\
    ip_cam_input_style, status_label_style, validate_button_style, export_btn_style, reset_btn_style, \
    unselect_btn_style


class DatePicker(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(150, 40)
        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy-MM-dd")
        self.setStyleSheet(search_input_style)


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
        # Set font styles for labels
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)

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
        ip_cam_label = QLabel('Enter IP Camera Address:')
        ip_cam_label.setStyleSheet(ip_label_style)
        ip_cam_label.setFont(font)

        ip_cam_input = QLineEdit()
        ip_cam_input.setStyleSheet(ip_cam_input_style)

        browse_mode = QPushButton("Browse Mode")
        stream_mode = QPushButton("Stream Mode")
        browse_mode.setStyleSheet(unselect_btn_style)
        stream_mode.setStyleSheet(unselect_btn_style)

        status_label = QLabel('')
        status_label.setStyleSheet(status_label_style)
        status_label.setFont(font)

        validate_button = QPushButton('Validate IP CAM')
        validate_button.setStyleSheet(validate_button_style)

        ip_cam_input.setEnabled(False)
        validate_button.setEnabled(False)
        browse_btn.setEnabled(False)

        # Mode media layout
        mode_media_layout = QtWidgets.QHBoxLayout()
        mode_media_layout.addWidget(browse_mode)
        mode_media_layout.addWidget(stream_mode)

        # Bottom media player layout
        left_media_layout = QtWidgets.QVBoxLayout()
        left_media_layout.addSpacerItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        left_media_layout.addLayout(mode_media_layout)
        left_media_layout.addWidget(ip_cam_label, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(ip_cam_input, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(validate_button, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(status_label, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(start_processing_btn, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(stop_processing_btn, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(browse_btn)
        left_media_layout.addSpacerItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        # Media Buttons Layout
        media_buttons_layout = QtWidgets.QHBoxLayout()
        media_buttons_layout.addWidget(play_btn)

        # Top media player layout
        top_media_layout = QtWidgets.QVBoxLayout()
        top_media_layout.addWidget(title)

        # Stream Layout
        stream_layout = QtWidgets.QVBoxLayout()
        stream_layout.addWidget(stream)
        stream_layout.addLayout(media_buttons_layout)

        # Bottom Layout
        bottom_media_layout = QtWidgets.QHBoxLayout()
        bottom_media_layout.addLayout(left_media_layout)
        bottom_media_layout.addLayout(stream_layout)

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_media_layout)
        main_layout.addWidget(line)
        main_layout.addLayout(bottom_media_layout)

        # Tab 1 Layout
        tab1_layout = QtWidgets.QGridLayout(self.tab1)
        tab1_layout.addLayout(main_layout, 0, 0, 1, 1)

        return start_processing_btn, stop_processing_btn, browse_btn, play_btn, browse_mode, stream_mode, \
            validate_button, status_label, ip_cam_input, stream
    
    def initialize_report_content(self):
        # create table
        table = TableWidget(fetch_data())

        # create components
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
        license_input = QLineEdit(self.obj)
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
        media_type_combo.addItems(["All", "Image", "Video", "Live Stream"])
        media_type_combo.setStyleSheet(combobox_style)

        score_label = QLabel('Score:', self.obj)
        score_label.setStyleSheet(label_style)
        score_input = QLineEdit()
        score_input.setPlaceholderText("Score")
        score_input.setValidator(QtGui.QDoubleValidator(0, 1, 3))
        score_input.setStyleSheet(search_input_style)

        filter_button = QPushButton("Filter")
        filter_button.setStyleSheet(button_style)

        # create layout
        grid_layout = QtWidgets.QGridLayout(self.tab2)
        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout_2 = QtWidgets.QHBoxLayout()
        vertical_layout = QtWidgets.QVBoxLayout()

        horizontal_layout.setSpacing(5)
        horizontal_layout.addWidget(license_label)
        horizontal_layout.addWidget(license_input)
        horizontal_layout.addWidget(score_label)
        horizontal_layout.addWidget(score_input)
        horizontal_layout.addWidget(media_label)
        horizontal_layout.addWidget(media_type_combo)
        horizontal_layout.addWidget(date_label)
        horizontal_layout.addWidget(date_from_picker)
        horizontal_layout.addWidget(date_to_picker)
        horizontal_layout.addWidget(filter_button)
        horizontal_layout_2.addWidget(export_btn)
        horizontal_layout_2.addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        horizontal_layout_2.addWidget(reset_btn)
        vertical_layout.addLayout(horizontal_layout_2)
        vertical_layout.addWidget(title_label)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(table)

        grid_layout.addLayout(vertical_layout, 0, 0, 1, 1)

        return export_btn, reset_btn, license_input, score_input, media_type_combo, date_from_picker, date_to_picker, \
            filter_button, table

    def get_central_widget(self):
        return self.central_widget
