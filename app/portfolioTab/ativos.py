import os
import sys
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ativo import Ativo
from PyQt5.QtCore import Qt, QDate, QLocale, QSize
from PyQt5.QtWidgets import (
    QButtonGroup, QRadioButton, QCheckBox, QDateEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QPushButton, QSpacerItem, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QDoubleValidator
from app.QtCreateFunc.helper import getValorMilharVirgula, create_custom_button
from functools import partial

def create_ListWidget():
    listWidget = QListWidget()
    listWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    listWidget.setStyleSheet("""
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
    listWidget.setSpacing(2)
    return listWidget

class NonInteractiveLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

class AtivosWindow(QWidget):
    def __init__(self, portfolio_window):
        super().__init__()
        self.portfolio_window = portfolio_window

    def create_button_action(self,ativo):
        print(f"clicado {ativo.getNome()}")
        self.portfolio_window.on_active(edit = True,ativoData=ativo)

    def AtivosSetUp(self):
        item_widht = 100
        item_height = 80
        grid_layout = QGridLayout()

        self.listAtivoCollumnOne = create_ListWidget()
        self.listAtivoCollumnTwo = create_ListWidget()
        self.listAtivoCollumnThree = create_ListWidget()
        self.listAtivoCollumnFour = create_ListWidget()
        listaAtivoList = []
        listaAtivoList.append(self.listAtivoCollumnOne)
        listaAtivoList.append(self.listAtivoCollumnTwo)
        listaAtivoList.append(self.listAtivoCollumnThree)
        listaAtivoList.append(self.listAtivoCollumnFour)

        grid_layout.addWidget(self.listAtivoCollumnOne,0,0)
        grid_layout.addWidget(self.listAtivoCollumnTwo,0,1)
        grid_layout.addWidget(self.listAtivoCollumnThree,0,2)
        grid_layout.addWidget(self.listAtivoCollumnFour,0,3)

        listAllAtivo = self.portfolio_window.userPortfolio.getAllAtivoBy()
        listAllAtivo.sort(key=lambda p: (p.getNome(), p.getCustodia()))

        patrimonio = sum(ativo.getPrecoAtual() for ativo in listAllAtivo)
        count = 0
        for ativo in listAllAtivo:
            list_item = QListWidgetItem()

            list_item.setData(Qt.UserRole, ativo)

            value = ativo.getPrecoAtual()
            label_info = f"""
                <div style="text-align: left; font-size: 12px;">
                    <b>{ativo.getNome()} :</b><br>
                    <div style="text-align: left">
                        <span><b>R$ {getValorMilharVirgula(value)}</b></span>
                    </div>
                    <div style="text-align: right">
                        <span><b>{100 * value / patrimonio:.2f}%</b></span>
                    </div>
                </div>
            """
            label = NonInteractiveLabel(label_info) 
            label.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            list_item.setData(Qt.UserRole, ativo)
            list_item.setSizeHint(QSize(item_widht, item_height))
            listaAtivoList[count].addItem(list_item)
            listaAtivoList[count].setItemWidget(list_item, label)

            count += 1
            if count == 4:
                count = 0
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
            
        list_item.setSizeHint(QSize(item_widht, item_height))
        listaAtivoList[count].addItem(list_item)
        listaAtivoList[count].setItemWidget(list_item, label)
        
        self.listAtivoCollumnOne.itemClicked.connect(self.on_item_clicked)
        self.listAtivoCollumnTwo.itemClicked.connect(self.on_item_clicked)
        self.listAtivoCollumnThree.itemClicked.connect(self.on_item_clicked)
        self.listAtivoCollumnFour.itemClicked.connect(self.on_item_clicked)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)

        return main_layout
    
    def on_item_clicked(self, item):
        ativo = item.data(Qt.UserRole)
        if ativo is not None:
            print(f"{ativo.getNome()}")
            self.portfolio_window.on_active(
                edit = True,
                ativoData = ativo
            )
        else:
            print("None")
            self.portfolio_window.on_active(
                add = True
            )

        if ativo:
            print(f"Ativo selecionado: {ativo.getNome()}")
    
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
        self.add_nome_ativo_text = QLineEdit()
        self.add_nome_ativo_text.setPlaceholderText("Nome")
        nome_layout = QHBoxLayout()
        nome_layout.addWidget(nome_ativo_label)
        nome_layout.addWidget(self.add_nome_ativo_text)
        main_layout.addLayout(nome_layout)

        codigo_ativo_label = QLabel("Código:")
        self.add_codigo_ativo_text = QLineEdit()
        self.add_codigo_ativo_text.setPlaceholderText("Código")
        codigo_layout = QHBoxLayout()
        codigo_layout.addWidget(codigo_ativo_label)
        codigo_layout.addWidget(self.add_codigo_ativo_text)
        main_layout.addLayout(codigo_layout)

        # Categoria do ativo
        categoria_ativo_label = QLabel("Categoria:")
        self.add_categoria_ativo_text = QLineEdit()
        self.add_categoria_ativo_text.setPlaceholderText("Categoria")
        categoria_layout = QHBoxLayout()
        categoria_layout.addWidget(categoria_ativo_label)
        categoria_layout.addWidget(self.add_categoria_ativo_text)
        main_layout.addLayout(categoria_layout)

        # Custódia do ativo
        custodia_ativo_label = QLabel("Custódia:")
        self.add_custodia_ativo_text = QLineEdit()
        self.add_custodia_ativo_text.setPlaceholderText("Custódia")
        custodia_layout = QHBoxLayout()
        custodia_layout.addWidget(custodia_ativo_label)
        custodia_layout.addWidget(self.add_custodia_ativo_text)
        main_layout.addLayout(custodia_layout)

        # Data de compra do ativo
        data_compra_ativo_label = QLabel("Data de compra:")
        self.add_data_compra_ativo_text = QDateEdit()
        self.add_data_compra_ativo_text.setDisplayFormat("dd/MM/yyyy")
        self.add_data_compra_ativo_text.setMinimumDate(QDate(1950, 1, 1))
        self.add_data_compra_ativo_text.setMaximumDate(QDate(2100, 12, 31))
        data_layout = QHBoxLayout()
        data_layout.addWidget(data_compra_ativo_label)
        data_layout.addWidget(self.add_data_compra_ativo_text)
        main_layout.addLayout(data_layout)

        # Quantidade
        quantidade_compra_ativo_label = QLabel("Quantidade:")
        self.add_quantidade_compra_ativo_text = QLineEdit()
        quantidade_compra_validador = QDoubleValidator(0.0, 1000.0, 5)
        quantidade_compra_validador.setNotation(QDoubleValidator.StandardNotation)
        locale = QLocale(QLocale.system().name())
        quantidade_compra_validador.setLocale(locale)
        self.add_quantidade_compra_ativo_text.setValidator(quantidade_compra_validador)
        quantidade_layout = QHBoxLayout()
        quantidade_layout.addWidget(quantidade_compra_ativo_label)
        quantidade_layout.addWidget(self.add_quantidade_compra_ativo_text)
        main_layout.addLayout(quantidade_layout)

        # Valor unitário
        valor_unitario_compra_ativo_label = QLabel("Valor unitário:")
        self.add_valor_unitario_compra_ativo_text = QLineEdit()
        valor_unitario_compra_validador = QDoubleValidator(0.0, 1000000.0, 5)
        valor_unitario_compra_validador.setNotation(QDoubleValidator.StandardNotation)
        valor_unitario_compra_validador.setLocale(locale)
        self.add_valor_unitario_compra_ativo_text.setValidator(valor_unitario_compra_validador)
        valor_unitario_layout = QHBoxLayout()
        valor_unitario_layout.addWidget(valor_unitario_compra_ativo_label)
        valor_unitario_layout.addWidget(self.add_valor_unitario_compra_ativo_text)
        main_layout.addLayout(valor_unitario_layout)

        confirm_button_layout = QHBoxLayout()
        
        # Botão de confirmação
        confirm_button = QPushButton("Confirmar")
        confirm_button.clicked.connect(lambda: self.AddAtivo2Portfolio(
            self.add_nome_ativo_text.text(),
            self.add_codigo_ativo_text.text(),
            self.add_categoria_ativo_text.text(),
            self.add_custodia_ativo_text.text(),
            self.add_data_compra_ativo_text.date().toString("yyyy-MM-dd"),
            self.add_quantidade_compra_ativo_text.text(),
            self.add_valor_unitario_compra_ativo_text.text()
        ))
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        confirm_button_layout.addWidget(spacer)
        confirm_button_layout.addWidget(confirm_button)
        main_layout.addLayout(confirm_button_layout)

        return main_layout
    
    def ChangeAtivo2Portfolio(self, old_name, old_custody,nome, codigo, categoria, custodia, data_compra, quantidade_compra, valor_unitario, sell = False):
        if not nome.strip() or not codigo.strip() or not categoria.strip() or not custodia.strip() or not quantidade_compra.strip() or not valor_unitario.strip():
            print("Erro: Todos os campos devem ser preenchidos.")
            return

        try:
            quantidade_compra = float(quantidade_compra)
            valor_unitario = float(valor_unitario)
            ativo = Ativo(ativo = nome,categoria= categoria,custodia = custodia, codigo = codigo, quantidade = quantidade_compra, data = data_compra, valor = valor_unitario, sell = sell)
            self.portfolio_window.userPortfolio.editAtivoPortfolio(old_name,old_custody,ativo)
            self.portfolio_window.on_active()
            
        except ValueError:
            print("Erro: Quantidade e Valor Unitário devem ser números válidos.")
        pass
    
    def ChangeAtivoData(self, ativo):
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
        data_compra_label = QLabel("É data de venda?")
        radio_group = QButtonGroup(self)  # Grupo de botões de rádio

        radio_sim = QRadioButton("Sim")
        radio_nao = QRadioButton("Não")
        radio_group.addButton(radio_sim)
        radio_group.addButton(radio_nao)
        radio_nao.setChecked(True)
        
        data_layout = QHBoxLayout()
        data_layout.addWidget(data_compra_ativo_label)
        data_layout.addWidget(self.data_compra_ativo_text)
        data_layout.addWidget(data_compra_label)
        data_layout.addWidget(radio_sim)
        data_layout.addWidget(radio_nao)
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
        confirm_button.clicked.connect(lambda: self.ChangeAtivo2Portfolio(
            ativo.getNome(),
            ativo.getCustodia(),
            self.nome_ativo_text.text(),
            self.codigo_ativo_text.text(),
            self.categoria_ativo_text.text(),
            self.custodia_ativo_text.text(),
            self.data_compra_ativo_text.date().toString("yyyy-MM-dd"),
            self.quantidade_compra_ativo_text.text(),
            valor_unitario_compra_ativo_text.text(),
            sell = not radio_nao.isChecked()
        ))
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        confirm_button_layout.addWidget(spacer)
        confirm_button_layout.addWidget(confirm_button)
        ChangeAtivo.addLayout(confirm_button_layout)

        self.editChangeAtivoData(ativo)

        return ChangeAtivo

    def editChangeAtivoData(self, ativo):
        self.nome_ativo_text.setText(ativo.getNome())
        self.codigo_ativo_text.setText(ativo.getCodigo())
        self.categoria_ativo_text.setText(ativo.getCategoria())
        self.custodia_ativo_text.setText(ativo.getCustodia())