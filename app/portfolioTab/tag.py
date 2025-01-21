import os
import sys
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.tag import Tag
from PyQt5.QtCore import Qt, QDate, QLocale, QSize, QEvent
from PyQt5.QtWidgets import (
    QButtonGroup, QColorDialog, QRadioButton, QCheckBox, QDateEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QPushButton, QSpacerItem, QListWidget, QListWidgetItem
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
        self.listTagsWidget = None

    def ListTags(self):
        self.listTagsWidget = QListWidget()
        self.listTagsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.listTagsWidget.setStyleSheet("""
        QListWidget {
            border: none;
            background-color: transparent;
        }
        
        """)
        self.listTagsWidget.installEventFilter(self)
        self.listTagsWidget.setDragEnabled(True)
        # self.listTagsWidget.setAcceptDrops(True)

        dicTags = self.portfolio_window.userPortfolio.getTags()
        for tag in dicTags:
            list_item = QListWidgetItem()
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
                    padding: 5px;  
                    color: black;
                    font-size: 14px;  
                    font-weight: bold;  
                    font-family: Arial, sans-serif;  
                }}
            """)
            self.listTagsWidget.addItem(list_item)
            self.listTagsWidget.setItemWidget(list_item, tag_label)  


        self.newTagName = QLineEdit()
        self.newTagName.setPlaceholderText("Nova Tag")

        horizontalLayout = QHBoxLayout()

        color_label = QLabel("Color: ")
        self.color_square = QPushButton()
        self.color_square.setStyleSheet(
            f"""
            background-color: rgb({255}, {255}, {255});
            border: 1px solid black;
            padding: 3px;  /* Adiciona um padding para diminuir o quadrado interno */
            """
        )
        self.save_color = [255,255,255]
        self.color_square.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.color_square.setMaximumSize(12, 12)
        self.color_square.setMinimumSize(12, 12)
        self.color_square.clicked.connect(self.changeColor)

        horizontalLayout.addWidget(color_label)
        horizontalLayout.addWidget(self.color_square)

        buttonAddTag = QPushButton("Add Tag")

        buttonAddTag.clicked.connect(self.addTagInList)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.listTagsWidget)
        main_layout.addWidget(self.newTagName)
        main_layout.addLayout(horizontalLayout)
        main_layout.addWidget(buttonAddTag)

        return main_layout
    
    def changeColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.save_color = color.getRgb()[:3]
            self.color_square.setStyleSheet(
                f"""
                background-color: rgb({self.save_color[0]}, {self.save_color[1]}, {self.save_color[2]});
                border: 1px solid black;
                padding: 3px;
                """
            )


    def addTagInList(self):
        list_item = QListWidgetItem()
        tagType = Tag(self.newTagName.text(),self.save_color)
        list_item.setData(Qt.UserRole, tagType)
        tagColor = tagType.getColor()
        list_item.setBackground(QColor(tagColor[0],tagColor[1],tagColor[2]))

        tag_label = NonInteractiveLabel(tagType.getName())
        tag_label.setStyleSheet(f"""
            QLabel {{
                text-align: center;
                background-color: rgb({tagColor[0]}, {tagColor[1]}, {tagColor[2]});
                border-radius: 10px;
                padding: 5px;  
                color: black;
                font-size: 14px;  
                font-weight: bold;  
                font-family: Arial, sans-serif;  
            }}
        """)
        self.listTagsWidget.addItem(list_item)
        self.listTagsWidget.setItemWidget(list_item, tag_label)
        self.portfolio_window.userPortfolio.addTag(self.listTagsWidget.count(),self.newTagName.text(),self.save_color)
    
    def deleteSelectedItems(self):
        selected_items = self.listTagsWidget.selectedItems()
        for item in selected_items:
            tag_data = item.data(Qt.UserRole)
            self.listTagsWidget.takeItem(self.listTagsWidget.row(item))
    
    def generateNewTagsDic(self):
        newTags = {}
        for i in range(self.listTagsWidget.count()):
            item = self.listTagsWidget.item(i)
            if item is not None: 
                print(i)
                tag_data = item.data(Qt.UserRole)
                newTags[i] = {
                    "name": tag_data.getName(),
                    "color": tag_data.getColor()
                }
        return newTags
            

    def eventFilter(self, source, event):
        if source == self.listTagsWidget and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Delete:
                print("chamou")
                self.deleteSelectedItems()
                return True
        return super().eventFilter(source, event)
    
    def dropEvent(self, event):
        # Verificar se o item foi arrastado dentro da própria lista
        if event.source() == self.listTagsWidget:
            # Impede a adição ou movimentação de um item dentro da mesma lista
            event.setDropAction(Qt.IgnoreAction)
            event.ignore()
        else:
            event.acceptProposedAction()