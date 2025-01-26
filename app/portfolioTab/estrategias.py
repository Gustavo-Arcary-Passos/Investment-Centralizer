import os
import ast
import sys
import types
import copy
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt, QDate, QLocale, QSize, QEvent, QMimeData
from PyQt5.QtWidgets import (
    QButtonGroup, QRadioButton, QCheckBox, QDateEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QPushButton, QSpacerItem, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,  QHeaderView, QStyledItemDelegate
)
from PyQt5.QtGui import QIntValidator
from app.QtCreateFunc.helper import NonInteractiveLabel
from app.estrategia import Estrategia
from app.ativo import Ativo
from app.tag import Tag

class NumericDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QIntValidator(0, 9999, editor)
        editor.setValidator(validator)
        return editor

class DropTable(QTableWidget):
    def __init__(self, rows, cols, portfolio = None):
        super().__init__(rows, cols)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.portfolio_window = portfolio
        if self.portfolio_window is not None:
            print(portfolio.userPortfolio.getAllAtivos())
            self.ativos = copy.deepcopy(portfolio.userPortfolio.getAllAtivos())
            self.tags = []
        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem(f"Item {row + 1}, {col + 1}")
                self.setItem(row, col, item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/tag-item-data"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/tag-item-data"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        print("Drop em table")
    
        data = event.mimeData().data("application/tag-item-data").data().decode()
        data = ast.literal_eval(data)
        tag = Tag(tag=data)

        rows = self.rowCount()
        for row in range(rows):
            item = self.item(row, 0)
            if item and item.text() == tag.getName():
                return
        
        self.insertRow(rows)
        
        tableTagName = NonInteractiveLabel(tag.getName())
        tableTagColor = tag.getColor()
        tableTagName.setStyleSheet(f"""
            QLabel {{
                text-align: left;
                background-color: rgb({tableTagColor[0]}, {tableTagColor[1]}, {tableTagColor[2]});
                border-radius: 10px;
                padding: 5px;  
                color: black;
                font-size: 14px;  
                font-weight: bold;  
                font-family: Arial, sans-serif;  
            }}
        """)
        self.setCellWidget(rows, 0, tableTagName)
        item = QTableWidgetItem(tag.getName())
        item.setData(Qt.UserRole, tag)
        self.setItem(rows, 0, item)
        self.specificManipulation(rows,data)
        event.accept()

    def specificManipulation(self,row,tag):
        print("specificManipulation")
        #self.portfolio_window
        pass

class EstrategiaWindow(QWidget):
    def __init__(self, portfolio_window):
        super().__init__()
        self.portfolio_window = portfolio_window

    def EstrategiaSetUp(self):
        print("EstrategiaSetUp")
        item_widht = 100
        item_height = 80
        main_layout = QVBoxLayout()

        self.listEstrategyWidget = QListWidget()
        self.listEstrategyWidget.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidget::item {
                text-align: left;
                background-color: #3498db;
                color: black;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QListWidget::item:hover {
                background-color: #2980b9;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)

        dicAllEstrategy = self.portfolio_window.userPortfolio.getAllEstrategy()
        for estrategy in dicAllEstrategy:
            list_item = QListWidgetItem()
            estrategia = Estrategia(estrategy)
            list_item.setData(Qt.UserRole, estrategia)

            label_info = f"""
                <b>{estrategia.getNome()}</b>
            """
            label = NonInteractiveLabel(label_info) 
            label.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            list_item.setData(Qt.UserRole, estrategia)
            list_item.setSizeHint(QSize(item_widht,item_height))
            self.listEstrategyWidget.addItem(list_item)
            self.listEstrategyWidget.setItemWidget(list_item, label)
        list_item = QListWidgetItem()
        list_item.setData(Qt.UserRole, None)
        label = NonInteractiveLabel(f"""
                <div style="text-align: center; font-size: 32px">
                    <b>+</b>
                </div>
            """)
        label.setStyleSheet('''
            QLabel {
                color: #38ADFC;
                font-size: 32px;
                font-weight: bold;
            }
            QLabel:hover {
                background-color: #2980b9;
                color: #2778AE;
            }
        ''') 
        label.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            
        list_item.setSizeHint(QSize(item_widht,item_height))
        self.listEstrategyWidget.addItem(list_item)
        self.listEstrategyWidget.setItemWidget(list_item, label)
        self.listEstrategyWidget.clicked.connect(self.on_item_clicked)

        main_layout.addWidget(self.listEstrategyWidget)

        return main_layout
    
    def on_item_clicked(self, item):
        estrategia = item.data(Qt.UserRole)
        if estrategia is not None:
            print(f"{estrategia.getNome()}")
            self.portfolio_window.on_estrategy(
                show = True,
                estrategiaData = estrategia
            )
        else:
            print("None")
            self.portfolio_window.on_estrategy(
                add = True
            )

        if estrategia:
            print(f"Ativo selecionado: {estrategia.getNome()}")

    def createListWithLabel(self, column_label, portfolio = None):
        tableWithLabelLayout = QVBoxLayout()

        tabela = DropTable(0,len(column_label), portfolio)
        tabela.setHorizontalHeaderLabels(column_label)
        tabela.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        header = tabela.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        tableWithLabelLayout.addWidget(tabela)

        return tableWithLabelLayout, tabela

    def AddEstrategia2Portfolio(self):
        main_layout = QVBoxLayout()

        # Back_to_Principal_Layout
        back_button_layout = QHBoxLayout()
        back_button = QPushButton("<")
        back_button.clicked.connect(self.portfolio_window.on_estrategy)
        back_button_layout.addWidget(back_button)
        back_button_layout.addStretch()
        main_layout.addLayout(back_button_layout)

        # Nome do ativo
        nome_estrategia_label = QLabel("Nome da Estrategia:")
        self.add_nome_estrategia_text = QLineEdit()
        self.add_nome_estrategia_text.setPlaceholderText("Nome")
        nome_layout = QHBoxLayout()
        nome_layout.addWidget(nome_estrategia_label)
        nome_layout.addWidget(self.add_nome_estrategia_text)
        main_layout.addLayout(nome_layout)

        estrategi_base_layout = QHBoxLayout()
        tags_filtro_list_layout,self.tags_filtro_list = self.createListWithLabel(["Tags para filtro:","Quantidade"],self.portfolio_window)
        def ativosWithThisTag(self, row, tag):
            print(f"ativosWithThisTag {tag}")
            disableTagsList = self.portfolio_window.tagsWindow.getTagNameList()
            print(disableTagsList)
            quantidade = 0
            self.tags.append(tag)
            for ativo in self.ativos:
                ativo = Ativo(ativo)
                inFilters = True
                if ativo.haveTag(tag):
                    quantidade += 1
                for tagItem in self.tags:
                    if not ativo.haveTag(tagItem):
                        inFilters = False
                if inFilters:
                    for i in range(len(disableTagsList) - 1, -1, -1):
                        print(disableTagsList[i])
                        if ativo.haveTag(disableTagsList[i].get()):
                            del disableTagsList[i]
            item = QTableWidgetItem(str(quantidade))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 1, item)
            self.portfolio_window.tagsWindow.makeDragDisable(disableTagsList)

        self.tags_filtro_list.specificManipulation = types.MethodType(ativosWithThisTag, self.tags_filtro_list)
        self.tags_filtro_list.installEventFilter(self)

        tags_comparacao_list_layout,self.tags_comparacao_list = self.createListWithLabel(["Tags para comparar:","Partes","Percentual(%)"])
        self.tags_comparacao_list.setItemDelegateForColumn(1, NumericDelegate(self))
        self.tags_comparacao_list.installEventFilter(self)

        estrategi_base_layout.addLayout(tags_filtro_list_layout)
        estrategi_base_layout.addLayout(tags_comparacao_list_layout)
        main_layout.addLayout(estrategi_base_layout)

        confirm_button_layout = QHBoxLayout()
        
        confirm_button = QPushButton("Confirmar")
        confirm_button.clicked.connect(lambda: self.AddAtivo2Portfolio(
            self.add_nome_ativo_text.text(),
        ))
        confirm_button_layout.addStretch()
        confirm_button_layout.addWidget(confirm_button)
        main_layout.addLayout(confirm_button_layout)

        return main_layout
    
    def ShowEstrategia2Portfolio(self, estrategiaData):
        main_layout = QVBoxLayout()

        return main_layout
    
    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Delete:
                selected_items = source.selectedItems()
                if selected_items:
                    row = selected_items[0].row()
                    source.removeRow(row)
                return True
        return super().eventFilter(source, event)