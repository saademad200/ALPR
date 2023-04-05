"""
This module contains two classes for initializing and managing date pickers and tabs for the UI.

Classes:
    DatePicker: A class for creating and managing date pickers.
    InitializeTabs: A class for initializing and managing tabs.
"""
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QStyle, QTabWidget, QPushButton, QLabel, QLineEdit, QDateEdit, \
    QComboBox
from user_interface.table import TableWidget
from user_interface.utils import media_player, fetch_data
from user_interface.styles import BUTTON_STYLE, SEARCH_INPUT_STYLE, LABEL_STYLE, COMBOBOX_STYLE, \
    TITLE_STYLE, START_PROCESSING_BTN_STYLE, STOP_PROCESSING_BTN_STYLE, BROWSE_BTN_STYLE, \
    PLAY_BTN_STYLE, IP_LABEL_STYLE, IP_CAM_INPUT_STYLE, STATUS_LABEL_STYLE, \
    VALIDATE_BUTTON_STYLE, EXPORT_BTN_STYLE, RESET_BTN_STYLE, UNSELECT_BTN_STYLE


class DatePicker(QDateEdit):
    """
    A custom QDateEdit widget that displays a calendar popup and allows users to select a date.

    This widget inherits from the QDateEdit class and sets various properties and styles to provide
    a consistent user experience.

    Attributes:
        parent (QWidget): The parent widget of this widget, if any.

    Methods:
        __init__(self, parent=None): Initializes a new DatePicker widget.
    """

    def __init__(self, parent=None):
        """
        Initializes a new DatePicker widget with a fixed size of 150x40, a calendar popup,
        and a display format of "yyyy-MM-dd". The widget is styled using the search_input_style
        constant defined in the module's constants.py file.

        Args:
            parent (QWidget): The parent widget of this widget, if any.
        """
        super().__init__(parent=parent)
        self.setFixedSize(150, 40)
        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy-MM-dd")
        self.setStyleSheet(SEARCH_INPUT_STYLE)


class InitializeTabs:
    """
    This class initializes a QTabWidget with two tabs - 'ALPR' and 'VIEW REPORTS'.
    The central_widget attribute contains the QTabWidget object, while tab1 and tab2
    attributes contain the corresponding tabs.

    Args:
        obj: The parent object of the QTabWidget.

    Attributes:
        obj: The parent object of the QTabWidget.
        central_widget: The QTabWidget object.
        tab1: The QWidget object representing the 'ALPR' tab.
        tab2: The QWidget object representing the 'VIEW REPORTS' tab.
    """

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

        self.alpr_widgets = self.initialize_alpr_content()
        self.report_widgets, self.table = self.initialize_report_content()

    def initialize_alpr_content(self):
        """
        This method initializes the content of the 'ALPR' tab.
        """
        # Set font styles for labels
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)

        title = QtWidgets.QLabel(self.tab1)
        title.setAlignment(Qt.AlignHCenter)
        title.setText('Ronicom')
        title.setStyleSheet(TITLE_STYLE)

        start_processing_btn = QtWidgets.QPushButton(self.tab1)
        start_processing_btn.setEnabled(False)
        start_processing_btn.setFixedSize(QtCore.QSize(200, 70))
        start_processing_btn.setStyleSheet(START_PROCESSING_BTN_STYLE)
        start_processing_btn.setText("Start Processing")

        stop_processing_btn = QtWidgets.QPushButton(self.tab1)
        stop_processing_btn.setEnabled(False)
        stop_processing_btn.setFixedSize(QtCore.QSize(200, 70))
        stop_processing_btn.setStyleSheet(STOP_PROCESSING_BTN_STYLE)
        stop_processing_btn.setText("Stop Processing")

        # Media Buttons
        browse_btn = QtWidgets.QPushButton(self.obj)
        browse_btn.setFixedSize(QtCore.QSize(200, 70))
        browse_btn.setText('Browse')
        browse_btn.setStyleSheet(BROWSE_BTN_STYLE)

        play_btn = QtWidgets.QPushButton(self.obj)
        play_btn.setIcon(self.obj.style().standardIcon(QStyle.SP_MediaPlay))
        play_btn.setStyleSheet(PLAY_BTN_STYLE)

        # Media Player
        stream = media_player(self.tab1)

        # Line
        line = QtWidgets.QFrame(self.tab1)
        line.setLineWidth(3)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Set font styles for labels
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)

        # Create UI elements
        ip_cam_label = QLabel('Enter IP Camera Address:')
        ip_cam_label.setStyleSheet(IP_LABEL_STYLE)
        ip_cam_label.setFont(font)

        ip_cam_input = QLineEdit()
        ip_cam_input.setStyleSheet(IP_CAM_INPUT_STYLE)

        browse_mode = QPushButton("Browse Mode")
        stream_mode = QPushButton("Stream Mode")
        browse_mode.setStyleSheet(UNSELECT_BTN_STYLE)
        stream_mode.setStyleSheet(UNSELECT_BTN_STYLE)

        status_label = QLabel('')
        status_label.setStyleSheet(STATUS_LABEL_STYLE)
        status_label.setFont(font)

        validate_button = QPushButton('Validate IP CAM')
        validate_button.setStyleSheet(VALIDATE_BUTTON_STYLE)

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
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Expanding))
        left_media_layout.addLayout(mode_media_layout)
        left_media_layout.addWidget(ip_cam_label, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(ip_cam_input, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(validate_button, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(status_label, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(browse_btn)
        left_media_layout.addWidget(start_processing_btn, alignment=Qt.AlignCenter)
        left_media_layout.addWidget(stop_processing_btn, alignment=Qt.AlignCenter)
        left_media_layout.addSpacerItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Expanding))

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

        alpr_widgets = {
            'start_processing_btn', start_processing_btn,
            'stop_processing_btn', stop_processing_btn,
            'browse_btn', browse_btn,
            'play_btn', play_btn,
            'browse_mode', browse_mode,
            'stream_mode', stream_mode,
            'validate_button', validate_button,
            'status_label', status_label,
            'ip_cam_input', ip_cam_input,
            'stream', stream
        }

        return alpr_widgets

    def initialize_report_content(self):
        """
        This method initializes the content of the 'VIEW REPORT' tab.
        """
        # create table
        report_table = TableWidget(fetch_data())

        # create components
        filter_title_label = QtWidgets.QLabel('Filter Search Results', self.obj)
        filter_title_label.setAlignment(QtCore.Qt.AlignCenter)
        filter_title_label.setStyleSheet(TITLE_STYLE)

        export_table_button = QtWidgets.QPushButton('Export Table', self.obj)
        export_table_button.setFixedSize(QtCore.QSize(120, 35))
        export_table_button.setStyleSheet(EXPORT_BTN_STYLE)

        reset_table_button = QtWidgets.QPushButton('Reset Table', self.obj)
        reset_table_button.setStyleSheet(RESET_BTN_STYLE)
        reset_table_button.setFixedSize(QtCore.QSize(120, 40))

        license_label = QLabel('License Plate:', self.obj)
        license_label.setStyleSheet(LABEL_STYLE)
        license_input = QLineEdit(self.obj)
        license_input.setPlaceholderText('License Plate')
        license_input.setStyleSheet(SEARCH_INPUT_STYLE)

        date_range_label = QLabel('Date Range:', self.obj)
        date_range_label.setStyleSheet(LABEL_STYLE)
        date_from_picker = DatePicker()
        date_from_picker.setDate(QDate.currentDate().addDays(-8))
        date_to_picker = DatePicker()
        date_to_picker.setDate(QDate.currentDate().addDays(2))

        camera_label = QLabel('Camera:', self.obj)
        camera_label.setStyleSheet(LABEL_STYLE)
        media_type_combo_box = QComboBox()
        media_type_combo_box.addItems(["All", "Image", "Video", "Live Stream"])
        media_type_combo_box.setStyleSheet(COMBOBOX_STYLE)

        score_label = QLabel('Score:', self.obj)
        score_label.setStyleSheet(LABEL_STYLE)
        score_input = QLineEdit()
        score_input.setPlaceholderText("Score")
        score_input.setValidator(QtGui.QDoubleValidator(0, 1, 3))
        score_input.setStyleSheet(SEARCH_INPUT_STYLE)

        filter_button = QPushButton("Filter")
        filter_button.setStyleSheet(BUTTON_STYLE)

        # create layout
        tab2_layout = QtWidgets.QGridLayout(self.tab2)
        filter_horizontal_layout = QtWidgets.QHBoxLayout()
        export_reset_horizontal_layout = QtWidgets.QHBoxLayout()
        main_layout = QtWidgets.QVBoxLayout()

        filter_horizontal_layout.setSpacing(5)
        filter_horizontal_layout.addWidget(license_label)
        filter_horizontal_layout.addWidget(license_input)
        filter_horizontal_layout.addWidget(score_label)
        filter_horizontal_layout.addWidget(score_input)
        filter_horizontal_layout.addWidget(camera_label)
        filter_horizontal_layout.addWidget(media_type_combo_box)
        filter_horizontal_layout.addWidget(date_range_label)
        filter_horizontal_layout.addWidget(date_from_picker)
        filter_horizontal_layout.addWidget(date_to_picker)
        filter_horizontal_layout.addWidget(filter_button)

        export_reset_horizontal_layout.addWidget(export_table_button)
        export_reset_horizontal_layout.addItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Minimum))
        export_reset_horizontal_layout.addWidget(reset_table_button)

        main_layout.addLayout(export_reset_horizontal_layout)
        main_layout.addWidget(filter_title_label)
        main_layout.addLayout(filter_horizontal_layout)
        main_layout.addWidget(report_table)

        tab2_layout.addLayout(main_layout, 0, 0, 1, 1)

        report_widgets = {
            'export_table_button', export_table_button,
            'reset_table_button', reset_table_button,
            'license_input', license_input,
            'score_input', score_input,
            'media_type_combo_box', media_type_combo_box,
            'date_from_picker', date_from_picker,
            'date_to_picker', date_to_picker,
            'filter_button', filter_button
        }

        return report_widgets, report_table

    def get_widgets(self):
        """
            Returns the widgets of the app.

            Returns:
            --------
            QWidget: The central widget of the app.
            QTableWidget: Table Widget.
            dict: Containing alpr widgets.
            dict: Containing report widgets.
        """
        return self.central_widget, self.table, self.alpr_widgets, self.report_widgets
