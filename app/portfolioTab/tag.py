import os
import sys
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.tag import Tag
from PyQt5.QtCore import Qt, QDate, QLocale, QSize, QEvent, QMimeData
from PyQt5.QtWidgets import (
    QButtonGroup, QColorDialog, QRadioButton, QCheckBox, QDateEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QPushButton, QSpacerItem, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QDoubleValidator, QColor, QDrag
from app.QtCreateFunc.helper import NonInteractiveLabel
from functools import partial

class DragTagList(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setDragEnabled(True)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item:
            return
        
        data = item.data(Qt.UserRole)
        if data is None:
            return
        
        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setData("application/tag-item-data", str(data).encode())
        drag.setMimeData(mimeData)

        drag.exec_(Qt.MoveAction)

class TagsWindow(QWidget):
    def __init__(self, portfolio_window):
        super().__init__()
        self.portfolio_window = portfolio_window
        self.listTagsWidget = None

    def ListTags(self, dicTags = {}, dragAble = True, should = True):
        self.listTagsWidget = DragTagList()
        self.listTagsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.listTagsWidget.setStyleSheet("""
        QListWidget {
            border: none;
            background-color: transparent;
        }
        """)
        self.listTagsWidget.installEventFilter(self)
        if not dragAble:
            print("Dragabel disable")
            self.listTagsWidget.setDragEnabled(False)

        for tag in dicTags:
            print(dicTags[tag])
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

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.listTagsWidget)

        if should:
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

    def getTagList(self):
        print("getTagList")
        tagList = []
        for index in range(self.listTagsWidget.count()):
            item = self.listTagsWidget.item(index)
            tag = item.data(Qt.UserRole)
            tagList.append(tag.get())

        return tagList

    def makeDragDisable(self,listTag):
        print("makeDragDisable")
        print(listTag)
        for index in range(self.listTagsWidget.count()):
            item = self.listTagsWidget.item(index)
            tag = item.data(Qt.UserRole)
            tagdic = tag.get()
            tagColor = tag.getColor()
            if tagdic['name'] in listTag and (item.flags() & Qt.ItemIsDragEnabled):
                item.setFlags(item.flags() & ~Qt.ItemIsDragEnabled)
                multiplier = 4
                divisor = 5
                disableColor = QColor(tagColor[0]*multiplier//divisor,tagColor[1]*multiplier//divisor,tagColor[2]*multiplier//divisor)
                item.setBackground(disableColor)
                widget = self.listTagsWidget.itemWidget(item)
                if widget:
                    widget.setStyleSheet(f"""
                        QLabel {{
                            text-align: center;
                            background-color: rgb({disableColor.red()}, {disableColor.green()}, {disableColor.blue()});
                            border-radius: 10px;
                            padding: 5px;  
                            color: gray;  /* Cor do texto desativado */
                            font-size: 14px;  
                            font-weight: bold;  
                            font-family: Arial, sans-serif;  
                        }}
                    """)
            elif tagdic['name'] not in listTag:
                if not (item.flags() & Qt.ItemIsDragEnabled):  # Verificar se o drag está desabilitado
                    item.setFlags(item.flags() | Qt.ItemIsDragEnabled)  # Habilitar o drag
                    Color = QColor(tagColor[0], tagColor[1], tagColor[2])
                    item.setBackground(Color)

                    widget = self.listTagsWidget.itemWidget(item)
                    if widget:
                        widget.setStyleSheet(f"""
                            QLabel {{
                                text-align: center;
                                background-color: rgb({Color.red()}, {Color.green()}, {Color.blue()});
                                border-radius: 10px;
                                padding: 5px;  
                                color: black;  /* Cor do texto habilitado */
                                font-size: 14px;  
                                font-weight: bold;  
                                font-family: Arial, sans-serif;  
                            }}
                        """)

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
    
    def deleteSelectedItems(self, action1 = None, action2 = None):
        selected_items = self.listTagsWidget.selectedItems()
        for item in selected_items:
            tag_data = item.data(Qt.UserRole)
            print(f"Deleta: {tag_data}")
            self.listTagsWidget.takeItem(self.listTagsWidget.row(item))
            if action1 is not None:
                action1(tag_data.getName())
            item.setData(Qt.UserRole, None)
            if action2 is not None:
                action2(self.generateNewTagsDic(), tag_data.getName())
    
    def generateNewTagsDic(self):
        newTags = {}
        print("GenerateNewTags")
        for i in range(self.listTagsWidget.count()):
            item = self.listTagsWidget.item(i)
            if item and item is not None:
                tag_data = item.data(Qt.UserRole)
                print(f"Tag: {tag_data}")
                newTags[i] = {
                    "name": tag_data.getName(),
                    "color": tag_data.getColor()
                }
        print("Terminou")
        return newTags

    def eventFilter(self, source, event):
        if source == self.listTagsWidget and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Delete:
                if self.listTagsWidget.dragEnabled():
                    updateAtivosWindow = None
                    if self.portfolio_window.current_scene == "active" :
                        print("Cena active")
                        updateAtivosWindow = self.portfolio_window.ativosWindow.deleteTagAllAtivoList
                    self.deleteSelectedItems(action1= updateAtivosWindow, action2= self.portfolio_window.userPortfolio.setTag)
                else:
                    self.deleteSelectedItems()

                return True
        return super().eventFilter(source, event)