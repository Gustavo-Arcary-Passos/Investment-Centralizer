import os
import sys
import unidecode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QButtonGroup, QCheckBox, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QSpacerItem
)
from PyQt5.QtGui import QColor, QPainter, QPixmap, QFont
from app.graphics import MatplotlibCanvas
from app.portfolio import Portfolio
from app.investments import Investment
from app.QtCreateFunc.helper import centralizedText,getValorMilharVirgula,generateListDataInGrid

class OverviewWindow(QWidget):
    def __init__(self, portfolio_window):
        super().__init__()
        self.portfolio_window = portfolio_window
        self.labels = []
        self.colors = []
        self.percentage = []

    def OverviewCanvasConfig(self, type="categoria"):
        canvas_layout = QVBoxLayout()
        canvas = MatplotlibCanvas(self, width=8, height=6, dpi=100)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        if self.portfolio_window.userPortfolio is None:
            self.portfolio_window.getUserPortfolio("GAP")
        dicInfo = self.portfolio_window.userPortfolio.getAtivosValueBy(type=type)
        data = list(dicInfo.values())
        self.labels = list(dicInfo.keys())
        self.colors, _, self.percentage, _ = canvas.plot_concentric_donuts(
            data=[data],
            labels=self.labels,
            radiusOut=1.5,
            sizeOut=0.5
        )

        scene = QGraphicsScene()
        scene.addWidget(canvas)
        graphics_view = QGraphicsView(scene)
        graphics_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        rect = graphics_view.viewport().rect()
        centralizedText(scene, graphics_view, "Carteira:", rect.width() / 8, rect.height() / 16)
        patrimonio = "R$ " + getValorMilharVirgula(sum(data))
        centralizedText(scene, graphics_view, patrimonio, rect.width() / 8, rect.height() * 2 / 12)

        canvas_layout.addWidget(graphics_view)
        return canvas_layout

    def OverviewInfoConfig(self, text="categoria"):
        info_layout = QVBoxLayout()
        data_layout = QGridLayout()

        if self.portfolio_window.userPortfolio is None:
            self.portfolio_window.getUserPortfolio("GAP")

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

        pos = 0
        data_layout.addWidget(self.categoria_checkbox, pos, 0)
        pos += 1
        if text == "categoria":
            pos = generateListDataInGrid(data_layout, pos, self.labels, self.colors, self.percentage)
        data_layout.addWidget(self.custodia_checkbox, pos, 0)
        pos += 1
        if text == "custodia":
            pos = generateListDataInGrid(data_layout, pos, self.labels, self.colors, self.percentage)
        data_layout.addWidget(self.ativos_checkbox, pos, 0)
        pos += 1
        if text == "name":
            pos = generateListDataInGrid(data_layout, pos, self.labels, self.colors, self.percentage)

        info_layout.addLayout(data_layout)

        emptyWidget = QWidget()
        emptyWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        info_layout.addWidget(emptyWidget)

        return info_layout

    def on_checkbox_toggled(self):
        if not self.categoria_checkbox.isChecked() and not self.custodia_checkbox.isChecked() and not self.ativos_checkbox.isChecked():
            self.sender().setChecked(True)  # Forçar a seleção de um checkbox

        if self.sender().isChecked():
            checkbox = self.sender()
            checkboxText = checkbox.text().lower()
            checkboxText = unidecode.unidecode(checkboxText)
            if checkboxText == "ativos":
                checkboxText = "name"
            self.portfolio_window.on_overview(
                canvas_layout=self.OverviewCanvasConfig(type=checkboxText),
                info_layout=self.OverviewInfoConfig(text=checkboxText)
            )
