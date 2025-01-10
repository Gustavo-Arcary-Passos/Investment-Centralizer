import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.investments import Investment

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QSizePolicy, QToolBar, QAction
from graphics import MatplotlibCanvas

class PortFolioWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.userPortfolio = None
        
        main_layout = QHBoxLayout()

        canvas_layout = QVBoxLayout()
        self.canvas = MatplotlibCanvas(self, width=8, height=6, dpi=100)  # Adiciona o canvas
        canvas_layout.addWidget(self.canvas)

        data = [30, 40, 30]
        labels = ['Ação 1', 'Ação 2', 'Ação 3']
        self.canvas.plot_pie_chart(data, labels)

        controls_layout = QVBoxLayout()
        
        ribbon = QToolBar()
        ribbon.setOrientation(Qt.Vertical)

        # Criar ações e associar a funções (ou slots)
        overview_action = QAction("Overview", self)
        estrategy_action = QAction("Estrategia", self)
        active_action = QAction("Ativos", self)
        metas_action = QAction("Metas", self)
        destaque_action = QAction("Destaques", self)

        # Adicionar ações ao QToolBar
        ribbon.addAction(overview_action)
        ribbon.addAction(estrategy_action)
        ribbon.addAction(active_action)
        ribbon.addAction(metas_action)
        ribbon.addAction(destaque_action)

        # Conectar as ações a funções (opcional)
        overview_action.triggered.connect(self.on_overview)
        estrategy_action.triggered.connect(self.on_estrategy)
        active_action.triggered.connect(self.on_active)
        metas_action.triggered.connect(self.on_metas)
        destaque_action.triggered.connect(self.on_destaque)

        controls_layout.addWidget(ribbon)

        main_layout.addLayout(controls_layout, stretch=1)
        main_layout.addLayout(canvas_layout, stretch=3)

        self.setLayout(main_layout)

    def getUserPortfolio(self, portfolioName):
        self.userPortfolio = Investment.getUserInvestment(portfolioName)

    # Funções associadas às ações
    def on_overview(self):
        print("Overview clicked")

    def on_estrategy(self):
        print("Estrategia clicked")

    def on_active(self):
        print("Ativos clicked")

    def on_metas(self):
        print("Metas clicked")

    def on_destaque(self):
        print("Destaques clicked")
