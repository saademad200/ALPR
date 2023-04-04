# Define custom styles

table_style = """
            QTableWidget::item { 
                border-bottom: 1px solid #FFFFFF; 
                border-right: 1px solid #FFFFFF; 
                text-align: center;}
                
            QTableWidget::item:selected {
                background-color: #93C5FF;
                color: #FFFFFF;
            }
        """

horizontal_header_style = "QHeaderView::section  { color:white; background-color: #3D87C9; border: none; border-bottom: 1px solid #FFFFFF; text-align: center; }"

vertical_header_style = "QHeaderView::section:vertical { height: 2500px; }"

button_style = '''
    QPushButton {
        background-color: blue; color: #fff; font-weight: bold; padding: 10px; border-radius: 3px; width: 100px; font-size: 16px;
    }
   '''
search_input_style = '''
    QLineEdit {
        font-size: 16px;
        padding: 6px;
        border: 2px solid gray;
        border-radius: 3px;
        background-color: #f2f2f2;
        color: #333;
    }
    QLineEdit:focus {
        border-color: #2ecc71;
    }
'''
label_style = """
    QLabel {
        font-size: 16px;
        padding: 6px;
        border: 2px solid gray;
        border-radius: 3px;
        background-color: #f2f2f2;
        color: #333;
        text-align: center;
    }
"""

combobox_style = '''
        QComboBox {
            border: 2px solid gray;
            border-radius: 3px;
            padding: 6px;
            font-size: 16px;
            background-color: #f2f2f2;
            color: #333;
            text-align: center;
            width: 150px;           
            
        }
        
        QComboBox::drop-down {
            width: 0px;
        }
        
        QComboBox::down-arrow:hover {
            background-color: gray;
        }
        
        QComboBox::down-arrow:on {
            background-color: gray;
        }        
'''

title_style = "font: 75 bold 25pt \"Yrsa\";"

start_processing_btn_style = "background-color: green; font: 75 italic 18pt \"Yrsa\"; padding: 0.75em 0.5em 0.75em 0.5em;"

stop_processing_btn_style = "background-color: red; font: 75 italic 18pt \"Yrsa\"; padding: 0.75em 0.5em 0.75em 0.5em;"

browse_btn_style = "font: 75 italic 18pt \"Yrsa\"; background-color: rgb(215, 215, 225); height:28px; "

play_btn_style = " background-color: rgb(215, 215, 225); height:30px;"

reset_btn_style = 'background-color: #c0392b; color: #fff; font-weight: bold; padding: 10px; border-radius: 5px;'

export_btn_style = 'background-color: #27ae60; color: #fff; font-weight: bold; padding: 10px; border-radius: 5px;'

ipcam_input_style = """
                    font-size: 14px;
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    background-color: #f2f2f2;
                """

status_label_style = """
                padding: 8px;
                color: green;
                font-size:10px;

                """
ip_label_style = """
                    padding: 8px;
                    font-size: 12px;
                """
validate_button_style = """
                        font-size: 14px;
                        padding: 8px 16px;
                        border: 1px solid #2c3e50;
                        border-radius: 5px;
                        color: #fff;
                        background-color: #2c3e50;
                        """

unselect_btn_style = """
                padding: 8px 8px;
                font-size: 13px;
                        border: 1px solid #2c3e50;
                        border-radius: 5px;
                        color: #fff;
                        background-color: #2c3e50;
                
            """

select_btn_style = """
                font-size: 13px;
                padding: 8px 8px;
                border: 1px solid #2c3e50;
                border-radius: 5px;
                color: #fff;
                background-color: green
                
            """