import os
import sys
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QButtonGroup, QCheckBox, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QPushButton, QSpacerItem
)
from app.QtCreateFunc.helper import getValorMilharVirgula, create_custom_button

class AtivosWindow(QWidget):
    def __init__(self, portfolio_window):
        super().__init__()
        self.portfolio_window = portfolio_window

    def AtivosSetUp(self):
        grid_layout = QGridLayout()
        
        listAllAtivo = self.portfolio_window.userPortfolio.getAllAtivoBy()
        listAllAtivo.sort(key=lambda p: (p.getNome(), p.getCustodia()))
        
        num_cols = 4 
        row, col = 0, 0 

        patrimonio = sum(ativo.getPrecoAtual() for ativo in listAllAtivo)
        
        for ativo in listAllAtivo:
            value = ativo.getPrecoAtual()
            button_info =  f"""
                <div style="text-align: left; font-size: 12px;">
                    <b>{ativo.getNome()} :</b><br>
                    <div style="text-align: left">
                        <span><b>R$ {getValorMilharVirgula(value)}</b></span>
                    </div>
                    <div style="text-align: right">
                        <span><b>{100*value/patrimonio:.2f}%</b></span>
                    </div>
                </div>
            """
            style = """
                QPushButton {
                    text-align: left;
                    background-color: #3498db;
                    color: black;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """
            #f"{ativo.getNome()}:\nR$ {getValorMilharVirgula(value)}" {value/patrimonio:.2f}%
            button = create_custom_button(button_info,style=style)
            #QPushButton()
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            grid_layout.addWidget(button, row, col)
            col += 1
            if col >= num_cols:
                col = 0
                row += 1

        while col < num_cols:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum)
            grid_layout.addWidget(spacer, row, col)
            col += 1

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(spacer)

        return main_layout

    def AddAtivo(self):
        AddAtivo = QHBoxLayout()
        return AddAtivo

    def ChangeAtivoData(self, name, custody):
        ChangeAtivo = QHBoxLayout()
        return ChangeAtivo