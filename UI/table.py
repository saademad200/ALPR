from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
import csv
from constants import DATA_PATH


class TableWidget(QTableWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()
        
    def initUI(self):
        self.setRowCount(len(self.data))
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["FILE NAME", "NUMBER PLATE TEXT", "TIME STAMP"])

        # Set header label width
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        # Create a QBrush with the desired font color
        self.horizontalHeader().setStyleSheet("color: red;")

        # Set header font
        font = header.font()
        font.setPointSize(12)
        font.setBold(True)
        header.setFont(font)

        # Add data to the table
        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                self.setItem(i, j, QTableWidgetItem(item))
            
        # Set column widths
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 400)
        self.setColumnWidth(2, 200)

        # Set table colors and fonts
        self.setStyleSheet("""
            QTableWidget {
                font-size: 12pt;
                font-family: Arial;
                background-color: #F2F8FE;
                border: none;
                padding: 10px;
                border-radius: 5px;
                color: #333333;
                text-align: center;
                
            }
            
            QHeaderView::section {
                background-color: #3D87C9;
                color: white;
                padding: 4px;
                font-size: 11pt;
                font-family: Arial;
                border: none;
            }
            
            QTableWidget::item {
                padding: 8px;
                border: none;
                               
            }
            
            QTableWidget::item:selected {
                background-color: #93C5FF;
                color: #FFFFFF;
            }
        """)
        
        # Set table alignment
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
                
        # Set table grid
        self.horizontalHeader().setStyleSheet("QHeaderView::section \
        { color:white; background-color: #3D87C9; border: none; border-bottom: 1px solid #FFFFFF; }")
        self.verticalHeader().setStyleSheet("QHeaderView::section \
        { color:white; background-color: #3D87C9; border: none; border-right: 1px solid #FFFFFF; }")
        self.setStyleSheet("QTableWidget::item { border-bottom: 1px solid #FFFFFF; border-right: 1px solid #FFFFFF; }")
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def addRow(self, row):
        rowPosition = self.rowCount()
        self.insertRow(rowPosition)
        for i, item in enumerate(row):
            self.setItem(rowPosition, i, QTableWidgetItem(item))
    
    def reset(self):
        self.setRowCount(0)
        
        with open(DATA_PATH, mode='w', newline='') as file:
            file.write('')
        print(f"Contents of data.csv have been deleted.")    
        
    def display(self, text=None):
        
        try:
            with open(DATA_PATH, 'r') as f:
                reader = csv.reader(f)
                self.setRowCount(0)
                data = [row for row in reader][::-1]
                if text is not None:
                    temp = []
                    for row in data:
                        for elem in row:
                            if text in elem:
                                temp.append(row)
                                break
                    data = temp
                self.setRowCount(len(data))
                # Add data to the table
                for i, row in enumerate(data):
                    for j, item in enumerate(row):
                        self.setItem(i, j, QTableWidgetItem(item))
        except:
            # self.setRowCount(0)
            pass
        
        
