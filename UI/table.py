from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QStyledItemDelegate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QStyledItemDelegate, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import  QtCore
from UI.styles import table_style, horizontal_header_style, vertical_header_style
from datetime import datetime
import csv
from constants import DATA_PATH
from UI.utils import convert_license_plate_image
from PIL import Image

class CenterAlignedDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class TableWidget(QTableWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.filter_dict = None
        self.initUI()
        
    def initUI(self):
        self.setRowCount(len(self.data))
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(["S No.",  "IMAGE", "Time", "LICENSE PLATE", "SCORE", "CAMERA", "DELETE"])
        
        # Set header label width
        
        header = self.horizontalHeader()
        
        # Create a QBrush with the desired font color
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
        self.setStyleSheet(table_style)
        self.horizontalHeader().setStyleSheet(horizontal_header_style)
        self.verticalHeader().setStyleSheet(vertical_header_style)
                
        # Center Align Items
        delegate = CenterAlignedDelegate(self)
        self.setItemDelegate(delegate)

        # Initialize Table
        self.display()
    
    def reset(self):
        self.setRowCount(0)
        
        with open(DATA_PATH, mode='w', newline='') as file:
            file.write('')
        print(f"Contents of data.csv have been deleted.")       

    def display(self, mode= "display", filter_dict=None):  
        self.filter_dict = filter_dict
        with open(DATA_PATH, 'r') as f:
            reader = csv.reader(f)
            self.setRowCount(0)
            data = [row for row in reader][::-1]

        if mode!="display":      
            if filter_dict is not None:
                temp = []
                for row in data:
                    print("Filtering License")
                    if filter_dict['LICENSE'] != '' and filter_dict['LICENSE'] not in row[1]:
                        continue
                    print("Filtering Score")

                    if filter_dict['SCORE'] != '' and float(filter_dict['SCORE']) > float(row[2]):
                        continue
                    print("Filtering Media")
                    if filter_dict['MEDIA'] != 'All' and filter_dict['MEDIA'] != row[3]:
                        continue
                    print("Filtering Date")
                    # Convert the given date to datetime object
                    given_date = datetime.strptime(row[0], '%B %d, %Y; %H:%M')

                    # Convert the two other dates to datetime objects
                    start_date = datetime.strptime(filter_dict['FROM'], '%Y-%m-%d')
                    end_date = datetime.strptime(filter_dict['TO'], '%Y-%m-%d')

                    # Check if the given date is within the range of the two other dates
                    if start_date <= given_date <= end_date:
                        temp.append(row)
                    
                data = temp            

            
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
        cell_value = self.item(row, 3).text()
        # Open the image file
        image = Image.open(f'license_plates/{cell_value}.jpg')

        # Display the image
        image.show()
            
        
    def delete_row(self, row):
        license_number = self.item(row, 3).text()

        # read the contents of the CSV file into memory
        with open(DATA_PATH, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        idx = None
        for i, entry in enumerate(data):
            if entry[1] == license_number:
                idx = i
                break

        # delete the row corresponding to the row that was deleted from the table
        data_to_delete = idx
        del data[data_to_delete]
        
        # write the updated data back to the CSV file
        with open(DATA_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        self.display(mode='filter', filter_dict=self.filter_dict)