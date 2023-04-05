"""
This code defines several constants, each of which specifies a style for a particular
type of widget used in a graphical user interface. The styles are written in CSS-like
syntax and define various properties such as colors, font sizes, and border styles.

TABLE_STYLE: Defines the style for items within a QTableWidget,
    including border styles and text alignment.
HORIZONTAL_HEADER_STYLE: Defines the style for headers in a QTableWidget,
    including background color and text alignment.
VERTICAL_HEADER_STYLE: Defines the style for vertical headers in a QTableWidget,
    including height.
BUTTON_STYLE: Defines the style for a QPushButton, including background color,
    font size, and padding.
SEARCH_INPUT_STYLE: Defines the style for a QLineEdit used for searching, including font size,
    border styles, and background color.
LABEL_STYLE: Defines the style for a QLabel, including font size, border styles, background color,
    and text alignment.
COMBOBOX_STYLE: Defines the style for a QComboBox, including border styles, font size,
    background color, and text alignment.
TITLE_STYLE: Defines the style for a QLabel used as a title, including font, border styles,
    background color, and text alignment.
STATUS_LABEL_STYLE: Defines the style for a QLabel used to display status information,
    including font size, border styles, background color, and text alignment.
IP_LABEL_STYLE: Defines the style for a QLabel used to display an IP address,
    including font size, border styles, background color, and text alignment.
START_PROCESSING_BTN_STYLE: Defines the style for a QPushButton used to start processing,
    including background color, font, padding, and border styles.
STOP_PROCESSING_BTN_STYLE: Defines the style for a QPushButton used to stop processing,
    including background color, font, padding, and border styles.
BROWSE_BTN_STYLE: Defines the style for a QPushButton used to browse for files, including font,
    background color, height, border styles, and text alignment.
PLAY_BTN_STYLE: Defines the style for a QPushButton used to play audio, including background color,
    height, border styles, and text alignment.
RESET_BTN_STYLE: Defines the style for a QPushButton used to reset settings, including
    background color, font weight, padding, border radius, and border styles.
EXPORT_BTN_STYLE: Defines the style for a QPushButton used to export data, including
    background color, font weight, padding, border radius, and border styles.
UNSELECT_BTN_STYLE: Defines the style for a QPushButton used to unselect items, including
    font size, padding, border styles, background color, and text alignment.
SELECT_BTN_STYLE: Defines the style for a QPushButton used to select items, including
    font size, padding, border styles, background color, and text alignment.
VALIDATE_BTN_STYLE: Defines the style for a QPushButton used to select items, including
    font size, padding, border styles, background color, and text alignment.
IP_CAM_INPUT_STYLE: Defines the style for a QPushButton used to select items, including
    font size, padding, border styles, background color, and text alignment.
"""

TABLE_STYLE = """
    QTableWidget::item { 
        border-bottom: 1px solid #FFFFFF; 
        border-right: 1px solid #FFFFFF; 
        text-align: center;
    }
    QTableWidget::item:selected {
        background-color: #93C5FF;
        color: #FFFFFF;
    }
"""

HORIZONTAL_HEADER_STYLE = """
    QHeaderView::section {
        color: white;
        background-color: #3D87C9;
        border: none;
        border-bottom: 1px solid #FFFFFF;
        text-align: center;
    }
"""

VERTICAL_HEADER_STYLE = """
    QHeaderView::section:vertical {
        height: 2500px;
    }
"""

BUTTON_STYLE = '''
    QPushButton {
        background-color: blue;
        color: #fff;
        font-weight: bold;
        padding: 10px;
        border-radius: 3px;
        width: 100px;
        font-size: 16px;
    }
'''

SEARCH_INPUT_STYLE = '''
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

LABEL_STYLE = """
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

COMBOBOX_STYLE = '''
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

TITLE_STYLE = """
    QLabel {
        font: 75 bold 25pt "Yrsa";
        padding: 6px;
        border: 2px solid gray;
        border-radius: 3px;
        background-color: #f2f2f2;
        color: #333;
        text-align: center;
    }
"""

STATUS_LABEL_STYLE = """
    QLabel {
        padding: 8px;
        color: green;
        font-size: 10px;
        text-align: center;
    }
"""

IP_LABEL_STYLE = """
    QLabel {
        padding: 8px;
        font-size: 12px;
        text-align: center;
    }
"""

START_PROCESSING_BTN_STYLE = """
    QPushButton {
        background-color: green;
        font: 75 italic 18pt "Yrsa";
        padding: 0.75em 0.5em 0.75em 0.5em;
        border-radius: 3px;
        color: #fff;
        text-align: center;
    }
"""

STOP_PROCESSING_BTN_STYLE = """
    QPushButton {
        background-color: red;
        font: 75 italic 18pt "Yrsa";
        padding: 0.75em 0.5em 0.75em 0.5em;
        border-radius: 3px;
        color: #fff;
        text-align: center;
    }
"""

BROWSE_BTN_STYLE = """
    QPushButton {
        font: 75 italic 18pt "Yrsa";
        background-color: rgb(215, 215, 225);
        height: 28px;
        border: 2px solid gray;
        border-radius: 3px;
        color: #333;
        text-align: center;
    }
"""

PLAY_BTN_STYLE = """
    QPushButton {
        background-color: rgb(215, 215, 225);
        height: 30px;
        border: 2px solid gray;
        border-radius: 3px;
        color: #333;
        text-align: center;
    }
"""

RESET_BTN_STYLE = """
    QPushButton {
        background-color: red;
        color: white;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
"""

EXPORT_BTN_STYLE = """
    QPushButton {
        background-color: #27ae60;
        color: #fff;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
"""

UNSELECT_BTN_STYLE = """
    QPushButton {
        padding: 8px 8px;
        font-size: 13px;
        border: 1px solid #2c3e50;
        border-radius: 5px;
        color: #fff;
        background-color: #2c3e50;
        text-align: center;
    }
"""

SELECT_BTN_STYLE = """QPushButton {
    font-size: 13px;
    padding: 8px 8px;
    border: 1px solid #2c3e50;
    border-radius: 5px;
    color: #fff;
    background-color: green;
}"""

VALIDATE_BUTTON_STYLE = """QPushButton {
    font-size: 14px;
    padding: 8px 16px;
    border: 1px solid #2c3e50;
    border-radius: 5px;
    color: #fff;
    background-color: #2c3e50;
}"""

IP_CAM_INPUT_STYLE = """QLineEdit {
    font-size: 14px;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f2f2f2;
}"""