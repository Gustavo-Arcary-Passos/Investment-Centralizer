import os
import sys
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ativo import Ativo
from PyQt5.QtCore import Qt, QDate, QLocale
from PyQt5.QtWidgets import (
    QButtonGroup, QCheckBox, QDateEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QPushButton, QSpacerItem
)
from PyQt5.QtGui import QDoubleValidator
from app.QtCreateFunc.helper import getValorMilharVirgula, create_custom_button
from functools import partial

def addButton():
    button = QPushButton("+")
    style = """
                QPushButton {
                    text-align: center;
                    background-color: #3498db;
                    color: #38ADFC;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 32px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                    color: #2778AE;
                }
            """
    button.setStyleSheet(style)
    return button

class AtivosWindow(QWidget):
    def __init__(self, portfolio_window):
        super().__init__()
        self.portfolio_window = portfolio_window
        self.editAtivo = self.ChangeAtivoData()
        self.listAllAtivo = []
        self.listbutton = []

    def create_button_action(self,ativo):
        print(f"clicado {ativo.getNome()}")
        self.portfolio_window.on_active(edit = True,ativoData=ativo )

    def AtivosSetUp(self):
        grid_layout = QGridLayout()
        
        self.listAllAtivo = self.portfolio_window.userPortfolio.getAllAtivoBy()
        self.listAllAtivo.sort(key=lambda p: (p.getNome(), p.getCustodia()))
        
        num_cols = 4 
        row, col = 0, 0 

        patrimonio = sum(ativo.getPrecoAtual() for ativo in self.listAllAtivo)
        pos = 0
        for ativo in self.listAllAtivo:
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
            self.listbutton.append(button)
            self.listbutton[pos].clicked.connect(lambda checked, ativo=ativo: self.create_button_action(ativo))
            grid_layout.addWidget(button, row, col)
            col += 1
            pos += 1
            if col >= num_cols:
                col = 0
                row += 1
        addbutton = addButton()
        addbutton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        addbutton.clicked.connect(lambda: self.portfolio_window.on_active(add=True))
        grid_layout.addWidget(addbutton, row, col)
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
    
    def AddAtivo2Portfolio(self, nome, codigo, categoria, custodia, data_compra, quantidade_compra, valor_unitario):
        if not nome.strip() or not codigo.strip() or not categoria.strip() or not custodia.strip() or not quantidade_compra.strip() or not valor_unitario.strip():
            print("Erro: Todos os campos devem ser preenchidos.")
            return

        try:
            quantidade_compra = float(quantidade_compra)
            valor_unitario = float(valor_unitario)
            ativo = Ativo(ativo = nome,categoria= categoria,custodia = custodia, codigo = codigo, quantidade = quantidade_compra, data = data_compra, valor = valor_unitario)
            self.portfolio_window.userPortfolio.addAtivoPortfolio(ativo)
            self.portfolio_window.on_active()
            
        except ValueError:
            print("Erro: Quantidade e Valor Unitário devem ser números válidos.")
        pass

    def AddAtivo(self):
        main_layout = QVBoxLayout()

        # Nome do ativo
        nome_ativo_label = QLabel("Nome:")
        nome_ativo_text = QLineEdit()
        nome_ativo_text.setPlaceholderText("Nome")
        nome_layout = QHBoxLayout()
        nome_layout.addWidget(nome_ativo_label)
        nome_layout.addWidget(nome_ativo_text)
        main_layout.addLayout(nome_layout)

        codigo_ativo_label = QLabel("Código:")
        codigo_ativo_text = QLineEdit()
        codigo_ativo_text.setPlaceholderText("Código")
        codigo_layout = QHBoxLayout()
        codigo_layout.addWidget(codigo_ativo_label)
        codigo_layout.addWidget(codigo_ativo_text)
        main_layout.addLayout(codigo_layout)

        # Categoria do ativo
        categoria_ativo_label = QLabel("Categoria:")
        categoria_ativo_text = QLineEdit()
        categoria_ativo_text.setPlaceholderText("Categoria")
        categoria_layout = QHBoxLayout()
        categoria_layout.addWidget(categoria_ativo_label)
        categoria_layout.addWidget(categoria_ativo_text)
        main_layout.addLayout(categoria_layout)

        # Custódia do ativo
        custodia_ativo_label = QLabel("Custódia:")
        custodia_ativo_text = QLineEdit()
        custodia_ativo_text.setPlaceholderText("Custódia")
        custodia_layout = QHBoxLayout()
        custodia_layout.addWidget(custodia_ativo_label)
        custodia_layout.addWidget(custodia_ativo_text)
        main_layout.addLayout(custodia_layout)

        # Data de compra do ativo
        data_compra_ativo_label = QLabel("Data de compra:")
        data_compra_ativo_text = QDateEdit()
        data_compra_ativo_text.setDisplayFormat("yyyy-MM-dd")
        data_compra_ativo_text.setMinimumDate(QDate(1950, 1, 1))
        data_compra_ativo_text.setMaximumDate(QDate(2100, 12, 31))
        data_layout = QHBoxLayout()
        data_layout.addWidget(data_compra_ativo_label)
        data_layout.addWidget(data_compra_ativo_text)
        main_layout.addLayout(data_layout)

        # Quantidade
        quantidade_compra_ativo_label = QLabel("Quantidade:")
        quantidade_compra_ativo_text = QLineEdit()
        quantidade_compra_validador = QDoubleValidator(0.0, 1000.0, 5)
        quantidade_compra_validador.setNotation(QDoubleValidator.StandardNotation)
        locale = QLocale(QLocale.system().name())
        quantidade_compra_validador.setLocale(locale)
        quantidade_compra_ativo_text.setValidator(quantidade_compra_validador)
        quantidade_layout = QHBoxLayout()
        quantidade_layout.addWidget(quantidade_compra_ativo_label)
        quantidade_layout.addWidget(quantidade_compra_ativo_text)
        main_layout.addLayout(quantidade_layout)

        # Valor unitário
        valor_unitario_compra_ativo_label = QLabel("Valor unitário:")
        valor_unitario_compra_ativo_text = QLineEdit()
        valor_unitario_compra_validador = QDoubleValidator(0.0, 1000000.0, 5)
        valor_unitario_compra_validador.setNotation(QDoubleValidator.StandardNotation)
        valor_unitario_compra_validador.setLocale(locale)
        valor_unitario_compra_ativo_text.setValidator(valor_unitario_compra_validador)
        valor_unitario_layout = QHBoxLayout()
        valor_unitario_layout.addWidget(valor_unitario_compra_ativo_label)
        valor_unitario_layout.addWidget(valor_unitario_compra_ativo_text)
        main_layout.addLayout(valor_unitario_layout)

        confirm_button_layout = QHBoxLayout()
        
        # Botão de confirmação
        confirm_button = QPushButton("Confirmar")
        confirm_button.clicked.connect(lambda: self.AddAtivo2Portfolio(
            nome_ativo_text.text(),
            codigo_ativo_text.text(),
            categoria_ativo_text.text(),
            custodia_ativo_text.text(),
            data_compra_ativo_text.date().toString("dd/MM/yyyy"),
            quantidade_compra_ativo_text.text(),
            valor_unitario_compra_ativo_text.text()
        ))
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        confirm_button_layout.addWidget(spacer)
        confirm_button_layout.addWidget(confirm_button)
        main_layout.addLayout(confirm_button_layout)

        return main_layout
    
    def go2ChangeAtivoData(self,ativo):
        self.editChangeAtivoData(ativo)
        return self.editAtivo
    
    def ChangeAtivoData(self):
        ChangeAtivo = QVBoxLayout()

        nome_ativo_label = QLabel("Nome:")
        self.nome_ativo_text = QLineEdit()
        nome_layout = QHBoxLayout()
        nome_layout.addWidget(nome_ativo_label)
        nome_layout.addWidget(self.nome_ativo_text)
        ChangeAtivo.addLayout(nome_layout)

        codigo_ativo_label = QLabel("Código:")
        self.codigo_ativo_text = QLineEdit()
        codigo_layout = QHBoxLayout()
        codigo_layout.addWidget(codigo_ativo_label)
        codigo_layout.addWidget(self.codigo_ativo_text)
        ChangeAtivo.addLayout(codigo_layout)

        categoria_ativo_label = QLabel("Categoria:")
        self.categoria_ativo_text = QLineEdit()
        categoria_layout = QHBoxLayout()
        categoria_layout.addWidget(categoria_ativo_label)
        categoria_layout.addWidget(self.categoria_ativo_text)
        ChangeAtivo.addLayout(categoria_layout)

        custodia_ativo_label = QLabel("Custódia:")
        self.custodia_ativo_text = QLineEdit()
        custodia_layout = QHBoxLayout()
        custodia_layout.addWidget(custodia_ativo_label)
        custodia_layout.addWidget(self.custodia_ativo_text)
        ChangeAtivo.addLayout(custodia_layout)

        data_compra_ativo_label = QLabel("Data:")
        self.data_compra_ativo_text = QDateEdit()
        self.data_compra_ativo_text.setDisplayFormat("dd/MM/yyyy")
        self.data_compra_ativo_text.setMinimumDate(QDate(1950, 1, 1))
        self.data_compra_ativo_text.setMaximumDate(QDate(2100, 12, 31))
        data_compra_checkbox = QCheckBox("É data de venda?")
        data_compra_checkbox.setChecked(False)
        data_layout = QHBoxLayout()
        data_layout.addWidget(data_compra_ativo_label)
        data_layout.addWidget(self.data_compra_ativo_text)
        data_layout.addWidget(data_compra_checkbox)
        ChangeAtivo.addLayout(data_layout)

        quantidade_compra_ativo_label = QLabel("Quantidade:")
        self.quantidade_compra_ativo_text = QLineEdit()
        quantidade_compra_validador = QDoubleValidator(0.0, 1000.0, 5)
        quantidade_compra_validador.setNotation(QDoubleValidator.StandardNotation)
        locale = QLocale(QLocale.system().name())
        quantidade_compra_validador.setLocale(locale)
        self.quantidade_compra_ativo_text.setValidator(quantidade_compra_validador)
        quantidade_layout = QHBoxLayout()
        quantidade_layout.addWidget(quantidade_compra_ativo_label)
        quantidade_layout.addWidget(self.quantidade_compra_ativo_text)
        ChangeAtivo.addLayout(quantidade_layout)

        valor_unitario_compra_ativo_label = QLabel("Valor unitário:")
        valor_unitario_compra_ativo_text = QLineEdit()
        valor_unitario_compra_validador = QDoubleValidator(0.0, 1000000.0, 5)
        valor_unitario_compra_validador.setNotation(QDoubleValidator.StandardNotation)
        valor_unitario_compra_validador.setLocale(locale)
        valor_unitario_compra_ativo_text.setValidator(valor_unitario_compra_validador)
        valor_unitario_layout = QHBoxLayout()
        valor_unitario_layout.addWidget(valor_unitario_compra_ativo_label)
        valor_unitario_layout.addWidget(valor_unitario_compra_ativo_text)
        ChangeAtivo.addLayout(valor_unitario_layout)

        confirm_button_layout = QHBoxLayout()
        
        confirm_button = QPushButton("Confirmar")
        # confirm_button.clicked.connect(lambda: self.AddAtivo2Portfolio(
        #     self.nome_ativo_text.text(),
        #     self.codigo_ativo_text.text(),
        #     self.categoria_ativo_text.text(),
        #     self.custodia_ativo_text.text(),
        #     self.data_compra_ativo_text.date().toString("yyyy-MM-dd"),
        #     self.quantidade_compra_ativo_text.text(),
        #     valor_unitario_compra_ativo_text.text()
        # ))
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        confirm_button_layout.addWidget(spacer)
        confirm_button_layout.addWidget(confirm_button)
        ChangeAtivo.addLayout(confirm_button_layout)

        return ChangeAtivo

    def editChangeAtivoData(self, ativo):
        self.nome_ativo_text.setText(ativo.getNome())
        self.codigo_ativo_text.setText(ativo.getCodigo())
        self.categoria_ativo_text.setText(ativo.getCategoria())
        self.custodia_ativo_text.setText(ativo.getCustodia())