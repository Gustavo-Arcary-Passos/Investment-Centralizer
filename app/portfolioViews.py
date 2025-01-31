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
from app.portfolioTab.tag import TagsWindow
from app.portfolioTab.estrategias import EstrategiaWindow
from app.ativo import Ativo

class PortFolioWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.userPortfolio = None
        self.current_scene = None

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
        active_toolbutton = createQToolButton("Ativos", QSizePolicy.Expanding)
        estrategy_toolbutton = createQToolButton("Estrategia", QSizePolicy.Expanding)
        metas_toolbutton = createQToolButton("Metas", QSizePolicy.Expanding)
        destaque_toolbutton = createQToolButton("Destaques", QSizePolicy.Expanding)

        overview_toolbutton.clicked.connect(self.on_overview)
        active_toolbutton.clicked.connect(self.on_active)
        estrategy_toolbutton.clicked.connect(self.on_estrategy)
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

    def save_data(self):
        print("save_data")
        Investment.updateUserInvestment(self.username,self.userPortfolio) #  userTagList = self.tagsWindow.generateNewTagsDic()
    
    def getUserPortfolio(self, portfolioName):
        self.username = portfolioName
        self.userPortfolio = Portfolio(Investment.getUserInvestment(portfolioName))
        return True

    def persistyData(self):
        print("persistyData")
        if self.current_scene == "active":
            self.userPortfolio.setTag(self.tagsWindow.generateNewTagsDic())

    def clear_dynamic_content(self):
        """Limpa o conteúdo do layout dinâmico."""
        print("clear_dynamic_content")
        self.current_scene = None
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
        self.current_scene = "overview"

    def on_active(self, add = False, edit = False, ativoData = None):
        print("on_active")
        if not hasattr(self, 'ativosWindow') or self.ativosWindow is None:
            self.ativosWindow = AtivosWindow(self)

        if not hasattr(self, 'tagsWindow') or self.tagsWindow is None:
            self.tagsWindow = TagsWindow(self)
        
        ativo = QWidget() 
        ativo_layout = QHBoxLayout()
        
        tagList = QHBoxLayout()

        if not add and not edit:
            listAtivos_layout = self.ativosWindow.AtivosSetUp()
            tagList = self.tagsWindow.ListTags(dicTags = self.userPortfolio.getTags())
        elif add:
            listAtivos_layout = self.ativosWindow.AddAtivo()
        elif edit:
            listAtivos_layout = self.ativosWindow.ChangeAtivoData(ativoData)
            tagList = self.tagsWindow.ListTags(dicTags = ativoData.getTags(), dragAble = False, should = False)

        ativo_layout.addLayout(listAtivos_layout, stretch=14)
        ativo_layout.addLayout(tagList, stretch=4)

        ativo.setLayout(ativo_layout)

        self.load_scene(ativo)
        self.current_scene = "active"

    def on_estrategy(self, add = False, show = False, estrategiaData = None):
        print("on_estrategy")
        if not hasattr(self, 'estrategiaWindow') or self.estrategiaWindow is None:
            self.estrategiaWindow = EstrategiaWindow(self)

        if not hasattr(self, 'tagsWindow') or self.tagsWindow is None:
            self.tagsWindow = TagsWindow(self)

        estrategia = QWidget() 

        estrategia_layout = QVBoxLayout()

        estrategia_data_layout = QHBoxLayout()

        if not add and not show:
            estrategia_layout_view = self.estrategiaWindow.EstrategiaSetUp()
            tagList = self.tagsWindow.ListTags(dicTags = self.userPortfolio.getTags(),dragAble = False, should = False)
        elif add:
            backButton = self.estrategiaWindow.back2Estrategy()
            estrategia_layout.addLayout(backButton)
            estrategia_layout_view = self.estrategiaWindow.AddEstrategia()
            tagList = self.tagsWindow.ListTags(dicTags = self.userPortfolio.getTags(), should = False)
        elif show:
            backButton = self.estrategiaWindow.back2Estrategy()
            estrategia_layout.addLayout(backButton)
            estrategia_layout_view = self.estrategiaWindow.ShowEstrategia2Portfolio(estrategiaData)
            tagList = self.estrategiaWindow.ShowEstrategiaInfoConfig()

        estrategia_data_layout.addLayout(estrategia_layout_view, stretch=14)
        estrategia_data_layout.addLayout(tagList, stretch=4)

        estrategia_layout.addLayout(estrategia_data_layout)

        estrategia.setLayout(estrategia_layout)

        self.load_scene(estrategia)
        self.current_scene = "estrategy"

    def on_metas(self):
        content = QLabel("Cena de Metas")
        self.load_scene(content)
        self.current_scene = "metas"

    def on_destaque(self):
        content = QLabel("Cena de Destaques")
        self.load_scene(content)
        self.current_scene = "destaque"