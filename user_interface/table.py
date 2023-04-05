"""
This module contains the `TableWidget` class and the `CenterAlignedDelegate` class.

The `TableWidget` class is a subclass of the `QTableWidget` class from the PyQt5 module.
It is used to display and interact with a table of data. The table is populated with data
from a CSV file located at `DATA_PATH` and it can be filtered by license plate, score, and camera.

The `CenterAlignedDelegate` class is a subclass of the `QStyledItemDelegate` class from
the PyQt5 module. It is used to center align the content of the table cells.

"""
import csv
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QStyledItemDelegate, QPushButton, \
    QHeaderView, QWidget, QHBoxLayout
from constants import DATA_PATH
from user_interface.utils import convert_license_plate_image, filter_table
from user_interface.styles import TABLE_STYLE, HORIZONTAL_HEADER_STYLE, VERTICAL_HEADER_STYLE


class CenterAlignedDelegate(QStyledItemDelegate):
    """
    A custom delegate to center-align the displayed content in a QTableView or QListView.

    """
    def initStyleOption(self, option, index):
        """
        Initializes the style option for the given index using the default values
        from the base class and sets the displayAlignment of the option to center.

        Args:
            option (QStyleOptionViewItem): The style option to be initialized.
            index (QModelIndex): The model index of the item to be displayed.

        """
        super().initStyleOption(option, index)

        # Set the alignment of the displayed content to center
        option.displayAlignment = Qt.AlignCenter


class TableWidget(QTableWidget):
    """
    A custom QTableWidget for displaying data.

    Args:
    - data (list): A list of lists containing the data to be displayed in the table.

    Attributes:
    - data (list): The data to be displayed in the table.
    - filter_dict (dict): A dictionary containing filter values for each column.

    """
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.filter_dict = None
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface of the TableWidget instance.
        """
        # Set number of rows and columns of the table
        self.setRowCount(len(self.data))
        self.setColumnCount(7)

        # Set horizontal header labels
        self.setHorizontalHeaderLabels(["S No.",  "IMAGE", "Time", "LICENSE PLATE",
                                        "SCORE", "CAMERA", "DELETE"])

        # Set header label width
        header = self.horizontalHeader()

        # Set the color of header text to red
        self.horizontalHeader().setStyleSheet("color: red;")

        # Set header font
        font = header.font()
        font.setPointSize(12)
        font.setBold(True)
        header.setFont(font)

        # Set table alignment
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)

        # Set Style
        self.setStyleSheet(TABLE_STYLE)
        self.horizontalHeader().setStyleSheet(HORIZONTAL_HEADER_STYLE)
        self.verticalHeader().setStyleSheet(VERTICAL_HEADER_STYLE)

        # Center Align Items
        delegate = CenterAlignedDelegate(self)
        self.setItemDelegate(delegate)

        # Initialize Table
        self.display()

    def reset(self):
        """
        Resets the table by setting the row count to zero and deleting all contents of the file.
        """
        self.setRowCount(0)

        # Delete all contents of the data file
        with open(DATA_PATH, mode='w', newline='', encoding="utf-8") as file:
            file.write('')
        print("Contents of data.csv have been deleted.")

    def display(self, mode="display", filter_dict=None):
        """
        Display the data in the table.

        Args:
        - mode: a string that indicates the table mode. Default is "display".
        - filter_dict: a dictionary containing filters to apply to the table. Default is None.
        """
        self.filter_dict = filter_dict
        with open(DATA_PATH, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            self.setRowCount(0)
            data = [row for row in reader][::-1]

        if mode != "display":
            if filter_dict is not None:
                data = filter_table(data, filter_dict)

        self.setRowCount(len(data))
        # Add data to the table
        for i, row in enumerate(data):
            item = QTableWidgetItem(str(i+1))
            self.setItem(i, 0, item)

            self.setRowHeight(i, 50)
            pixmap = convert_license_plate_image(row[1])
            scaled_pixmap = pixmap.scaled(self.columnWidth(1), 100, Qt.KeepAspectRatio)

            # create a QTableWidgetItem with the pixmap as its icon
            image_button = QPushButton()
            image_button.setIcon(QIcon(scaled_pixmap))
            image_button.setIconSize(QtCore.QSize(100, 50))
            image_button.clicked.connect(lambda _, row=i: self.display_img(row))
            image_widget = QWidget()
            image_layout = QHBoxLayout(image_widget)
            image_layout.addWidget(image_button)
            image_layout.setAlignment(Qt.AlignCenter)
            image_layout.setContentsMargins(0, 0, 0, 0)
            image_widget.setLayout(image_layout)
            self.setCellWidget(i, 1, image_widget)

            # Set the icon size of the table to the size of the cell
            self.setIconSize(scaled_pixmap.size())

            for j, item in enumerate(row):
                item = QTableWidgetItem(item)
                self.setItem(i, j+2, item)

            # create a custom widget for the delete button
            delete_button = QPushButton()
            delete_button.setIcon(QIcon('static/trash_can.png'))
            delete_button.clicked.connect(lambda _, row=i: self.delete_row(row))
            delete_widget = QWidget()
            delete_layout = QHBoxLayout(delete_widget)
            delete_layout.addWidget(delete_button)
            delete_layout.setAlignment(Qt.AlignCenter)
            delete_layout.setContentsMargins(0, 0, 0, 0)
            delete_widget.setLayout(delete_layout)
            self.setCellWidget(i, 6, delete_widget)

    def display_img(self, row):
        """
        Display the image of the selected row in a separate window.

        Args:
        - row: an integer indicating the row number of the selected item.

        """
        cell_value = self.item(row, 3).text()
        # Open the image file
        image = Image.open(f'license_plates/{cell_value}.jpg')

        # Display the image
        image.show()

    def delete_row(self, row):
        """
        Delete a row from the table and corresponding data in a CSV file.

        Args:
        - row: row number to delete

        """

        # Get the license plate number to delete
        license_number = self.item(row, 3).text()

        # Read the contents of the CSV file into memory
        with open(DATA_PATH, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            data = list(reader)

        # Find the index of the row to delete
        idx = None
        for i, entry in enumerate(data):
            if entry[1] == license_number:
                idx = i
                break

        # Delete the row corresponding to the row that was deleted from the table
        data_to_delete = idx
        del data[data_to_delete]

        # Write the updated data back to the CSV file
        with open(DATA_PATH, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        # Update the table to reflect the changes
        self.display(mode='filter', filter_dict=self.filter_dict)
