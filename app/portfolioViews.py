import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel
)
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


class PortFolioWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.userPortfolio = None

        # Layout principal
        main_layout = QHBoxLayout()

        # Layout da ribbon
        controls_layout = QVBoxLayout()
        ribbon = QToolBar()
        ribbon.setOrientation(Qt.Vertical)
        ribbon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ribbon.setStyleSheet("""
            QToolButton {
                font-size: 20px;  /* Tamanho da fonte */
            }
        """)

        # Botões da ribbon
        overview_toolbutton = createQToolButton("Overview", QSizePolicy.Expanding)
        estrategy_toolbutton = createQToolButton("Estrategia", QSizePolicy.Expanding)
        active_toolbutton = createQToolButton("Ativos", QSizePolicy.Expanding)
        metas_toolbutton = createQToolButton("Metas", QSizePolicy.Expanding)
        destaque_toolbutton = createQToolButton("Destaques", QSizePolicy.Expanding)

        # Conectar botões aos métodos
        overview_toolbutton.clicked.connect(self.on_overview)
        estrategy_toolbutton.clicked.connect(self.on_estrategy)
        active_toolbutton.clicked.connect(self.on_active)
        metas_toolbutton.clicked.connect(self.on_metas)
        destaque_toolbutton.clicked.connect(self.on_destaque)

        # Adicionar botões à ribbon
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

        # Widget de conteúdo dinâmico
        self.dynamic_content = QWidget()
        self.dynamic_content_layout = QVBoxLayout()
        self.dynamic_content.setLayout(self.dynamic_content_layout)

        main_layout.addWidget(self.dynamic_content, stretch=18)

        self.on_overview()

        # Configuração final
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

    # Funções associadas às ações
    def on_overview(self):
        overview = QWidget()
        overview_layout = QHBoxLayout()
        canvas_layout = QVBoxLayout()
        canvas = MatplotlibCanvas(self, width=8, height=6, dpi=100) 
        canvas_layout.addWidget(canvas)
        if self.userPortfolio is None:
            self.getUserPortfolio("GAP")
        labels,data = self.userPortfolio.getAtivosValueLabel()
        canvas.plot_pie_chart(data, labels)
        canvas.plot_concentric_donuts(
            data=[data],
            labels=labels,
            radiusOut = 1.5,
            sizeOut= 0.5
        )
        
        info_layout = QVBoxLayout()

        overview_layout.addLayout(canvas_layout, stretch = 15)
        overview_layout.addLayout(info_layout, stretch= 3)
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
