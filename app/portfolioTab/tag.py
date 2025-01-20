import os
import sys
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.tag import Tag
from PyQt5.QtCore import Qt, QDate, QLocale, QSize
from PyQt5.QtWidgets import (
    QButtonGroup, QRadioButton, QCheckBox, QDateEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QPushButton, QSpacerItem, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QDoubleValidator, QColor
from app.QtCreateFunc.helper import getValorMilharVirgula, create_custom_button
from functools import partial

class NonInteractiveLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

class TagsWindow(QWidget):
    def __init__(self, portfolio_window):
        super().__init__()
        self.portfolio_window = portfolio_window

    def ListTags(self):
        listTagsWidget = QListWidget()
        listTagsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        listTagsWidget.setStyleSheet("""
        QListWidget {
            border: none;
            background-color: transparent;
        }
        
        """)
        

        dicTags = self.portfolio_window.userPortfolio.getTags()
        for tag in dicTags:
            list_item = QListWidgetItem()
            print(dicTags[tag])
            tagType = Tag(tag = dicTags[tag])
            list_item.setData(Qt.UserRole, tagType)
            tagColor = tagType.getColor()
            list_item.setBackground(QColor(tagColor[0],tagColor[1],tagColor[2]))

            tag_label = NonInteractiveLabel(tagType.getName())
            tag_label.setStyleSheet(f"""
                QLabel {{
                    text-align: center;
                    background-color: rgb({tagColor[0]}, {tagColor[1]}, {tagColor[2]});
                    border-radius: 10px;
                    padding: 5px;  # Ajusta o padding para não ser muito grande
                    color: white;
                    font-size: 14px;  # Ajusta o tamanho da fonte
                    font-weight: bold;  # Deixa o texto mais legível
                    font-family: Arial, sans-serif;  # Define uma fonte mais legível
                }}
            """)
            listTagsWidget.addItem(list_item)
            listTagsWidget.setItemWidget(list_item, tag_label)  


        main_layout = QVBoxLayout()
        main_layout.addWidget(listTagsWidget)

        return main_layout