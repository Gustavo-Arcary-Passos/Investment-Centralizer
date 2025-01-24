import os
import ast
import sys
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt, QDate, QLocale, QSize
from PyQt5.QtWidgets import (
    QButtonGroup, QRadioButton, QCheckBox, QDateEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QPushButton, QSpacerItem, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QDoubleValidator
from app.QtCreateFunc.helper import NonInteractiveLabel
from app.estrategia import Estrategia

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

        tags_filtro_list = QListWidget()
        tags_filtro_name = QLabel("Tags para filtro:")
        tags_comparacao_list = QListWidget()
        tags_comparacao_name = QLabel("Tags para comparar:")
       

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