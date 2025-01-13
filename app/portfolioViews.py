import os
import sys
import unidecode
import locale
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QButtonGroup, QCheckBox, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QSpacerItem
)
from PyQt5.QtGui import QColor, QPainter, QPixmap, QFont
from app.graphics import MatplotlibCanvas
from app.portfolio import Portfolio
from app.investments import Investment
from app.QtCreateFunc.helper import createQToolButton
from app.portfolioTab.overview import OverviewWindow
from app.portfolioTab.ativos import AtivosWindow

class PortFolioWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.userPortfolio = None

        main_layout = QHBoxLayout()

        controls_layout = QVBoxLayout()
        ribbon = QToolBar()
        ribbon.setOrientation(Qt.Vertical)
        ribbon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ribbon.setStyleSheet("""
            QToolButton {
                font-size: 20px;  /* Tamanho da fonte */
            }
        """)

        overview_toolbutton = createQToolButton("Overview", QSizePolicy.Expanding)
        estrategy_toolbutton = createQToolButton("Estrategia", QSizePolicy.Expanding)
        active_toolbutton = createQToolButton("Ativos", QSizePolicy.Expanding)
        metas_toolbutton = createQToolButton("Metas", QSizePolicy.Expanding)
        destaque_toolbutton = createQToolButton("Destaques", QSizePolicy.Expanding)

        overview_toolbutton.clicked.connect(self.on_overview)
        estrategy_toolbutton.clicked.connect(self.on_estrategy)
        active_toolbutton.clicked.connect(self.on_active)
        metas_toolbutton.clicked.connect(self.on_metas)
        destaque_toolbutton.clicked.connect(self.on_destaque)

        ribbon.addWidget(overview_toolbutton)
        ribbon.addWidget(active_toolbutton)
        ribbon.addWidget(estrategy_toolbutton)
        ribbon.addWidget(metas_toolbutton)
        ribbon.addWidget(destaque_toolbutton)
        ribbon.addWidget(createQToolButton())
        ribbon.addWidget(createQToolButton())
        ribbon.addWidget(createQToolButton())

        controls_layout.addWidget(ribbon)
        main_layout.addLayout(controls_layout, stretch=3)

        self.dynamic_content = QWidget()
        self.dynamic_content_layout = QVBoxLayout()
        self.dynamic_content.setLayout(self.dynamic_content_layout)

        main_layout.addWidget(self.dynamic_content, stretch=18)

        self.on_overview()

        self.setLayout(main_layout)
    
    def getUserPortfolio(self, portfolioName):
        self.userPortfolio = Portfolio(Investment.getUserInvestment(portfolioName))

    def clear_dynamic_content(self):
        """Limpa o conteúdo do layout dinâmico."""
        while self.dynamic_content_layout.count():
            child = self.dynamic_content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_scene(self, content_widget):
        """Carrega uma nova cena no layout dinâmico."""
        self.clear_dynamic_content()
        self.dynamic_content_layout.addWidget(content_widget)

    def on_overview(self,canvas_layout = None, info_layout = None):
        if not hasattr(self, 'overviewWindow') or self.overviewWindow is None:
            self.overviewWindow = OverviewWindow(self)
        overview = QWidget()
        overview_layout = QHBoxLayout()
        canvas_layout = canvas_layout or self.overviewWindow.OverviewCanvasConfig()

        info_layout = info_layout or self.overviewWindow.OverviewInfoConfig()

        overview_layout.addLayout(canvas_layout, stretch=14)
        overview_layout.addLayout(info_layout, stretch=4)
        overview.setLayout(overview_layout)

        self.load_scene(overview)

    def on_active(self):
        if not hasattr(self, 'ativosWindow') or self.ativosWindow is None:
            self.ativosWindow = AtivosWindow(self)
        print("Ativos clicked")
        ativo = QWidget() 
        ativo_layout = QHBoxLayout()

        listAtivos_layout = self.ativosWindow.AtivosSetUp()

        spacer_layout = QHBoxLayout()
        spacerWidget = QWidget()
        spacerWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        spacer_layout.addWidget(spacerWidget)

        ativo_layout.addLayout(listAtivos_layout, stretch=14)
        ativo_layout.addLayout(spacer_layout, stretch=4)

        ativo.setLayout(ativo_layout)

        self.load_scene(ativo)

    def on_estrategy(self):
        print("Estrategia clicked")
        content = QLabel("Cena de Estratégia")
        self.load_scene(content)

    def on_metas(self):
        print("Metas clicked")
        content = QLabel("Cena de Metas")
        self.load_scene(content)

    def on_destaque(self):
        print("Destaques clicked")
        content = QLabel("Cena de Destaques")
        self.load_scene(content)