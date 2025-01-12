import os
import sys
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QButtonGroup, QCheckBox, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout
)
from PyQt5.QtGui import QPainter, QFont
from app.graphics import MatplotlibCanvas
from app.portfolio import Portfolio
from app.investments import Investment


def createQToolButton(name=None, sizePolicy=QSizePolicy.Expanding):
    toolButton = QToolButton()
    if name is not None:
        toolButton.setText(name)
    else:
        toolButton.setEnabled(False)
    toolButton.setSizePolicy(sizePolicy, sizePolicy)
    return toolButton

def centralizedText(scene,graphicsView, text, x = 0,y = 0):
    text_item = QGraphicsTextItem(text)
    text_item.setDefaultTextColor(Qt.black)
    text_item.setFont(QFont("Arial", 24, QFont.Bold))
    scene.addItem(text_item)
    rect = graphicsView.viewport().rect()
    center_x = rect.width() / 2
    center_y = rect.height() / 2

    text_rect = text_item.boundingRect()

    text_item.setPos(
        center_x - (text_rect.width())/2 + x,
        center_y - (text_rect.height())/2 + y
    )

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
        overview = QWidget()
        overview_layout = QHBoxLayout()
        canvas_layout = canvas_layout or self.OverviewCanvasConfig()

        info_layout = info_layout or self.OverviewInfoConfig()

        overview_layout.addLayout(canvas_layout, stretch=14)
        overview_layout.addLayout(info_layout, stretch=4)
        overview.setLayout(overview_layout)

        self.load_scene(overview)

    def on_estrategy(self):
        print("Estrategia clicked")
        content = QLabel("Cena de Estratégia")
        self.load_scene(content)

    def on_active(self):
        print("Ativos clicked")
        content = QLabel("Cena de Ativos")
        self.load_scene(content)

    def on_metas(self):
        print("Metas clicked")
        content = QLabel("Cena de Metas")
        self.load_scene(content)

    def on_destaque(self):
        print("Destaques clicked")
        content = QLabel("Cena de Destaques")
        self.load_scene(content)

    def OverviewCanvasConfig(self, type = "categoria"):
        canvas_layout = QVBoxLayout()
        canvas = MatplotlibCanvas(self, width=8, height=6, dpi=100)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        if self.userPortfolio is None:
            self.getUserPortfolio("GAP")
        dicInfo = self.userPortfolio.getAtivosValueBy(type = type)
        data = list(dicInfo.values())
        labels = list(dicInfo.keys())
        canvas.plot_concentric_donuts(
            data=[data],
            labels=labels,
            radiusOut=1.5,
            sizeOut=0.5
        )

        scene = QGraphicsScene()
        scene.addWidget(canvas)
        graphics_view = QGraphicsView(scene)
        graphics_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        rect = graphics_view.viewport().rect()
        centralizedText(scene,graphics_view,"Carteira:",rect.width()/8,rect.height()/16)
        patrimonio = "R$ " + f"{sum(data):.2f}"
        centralizedText(scene,graphics_view,patrimonio,rect.width()/8,rect.height()*2/12)

        canvas_layout.addWidget(graphics_view)
        return canvas_layout
    
    def OverviewInfoConfig(self, text = "categoria"):
        info_layout = QVBoxLayout()
        data_layout = QGridLayout()
        # categoria = self.userPortfolio.getAtivosValueBy(type = "categoria")
        # custodia = self.userPortfolio.getAtivosValueBy(type = "custodia")
        # ativos = self.userPortfolio.getAtivosValueBy(type = "name")

        if self.userPortfolio is None:
            self.getUserPortfolio("GAP")

        self.categoria_checkbox = QCheckBox("Categoria")
        self.categoria_checkbox.setChecked(text == "categoria")

        self.custodia_checkbox = QCheckBox("Custódia")
        self.custodia_checkbox.setChecked(text == "custodia")

        self.ativos_checkbox = QCheckBox("Ativos")
        self.ativos_checkbox.setChecked(text == "name")

        button_group = QButtonGroup(self)
        button_group.setExclusive(True)

        button_group.addButton(self.categoria_checkbox)
        button_group.addButton(self.custodia_checkbox)
        button_group.addButton(self.ativos_checkbox)

        self.categoria_checkbox.toggled.connect(self.on_checkbox_toggled)
        self.custodia_checkbox.toggled.connect(self.on_checkbox_toggled)
        self.ativos_checkbox.toggled.connect(self.on_checkbox_toggled)

        info_layout.setSpacing(0)
        info_layout.setContentsMargins(0, 0, 0, 0)

        data_layout.addWidget(self.categoria_checkbox, 0, 0)
        data_layout.addWidget(self.custodia_checkbox, 1, 0)
        data_layout.addWidget(self.ativos_checkbox, 2, 0)

        info_layout.addLayout(data_layout)

        emptyWidget = QWidget()
        emptyWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        info_layout.addWidget(emptyWidget)

        return info_layout

    def on_checkbox_toggled(self):
    # Garantir que pelo menos um checkbox está selecionado
        if not self.categoria_checkbox.isChecked() and not self.custodia_checkbox.isChecked() and not self.ativos_checkbox.isChecked():
            self.sender().setChecked(True)  # Forçar a seleção de um checkbox
        
        # Quando um checkbox for selecionado
        if self.sender().isChecked():
            checkbox = self.sender()
            checkboxText = checkbox.text().lower()
            checkboxText = unidecode.unidecode(checkboxText)
            if checkboxText == "ativos":
                checkboxText = "name"
            self.on_overview(canvas_layout=self.OverviewCanvasConfig(type=checkboxText), info_layout=self.OverviewInfoConfig(text=checkboxText))