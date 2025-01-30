import os
import sys
import locale
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QButtonGroup, QCheckBox, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QToolBar, QToolButton, QSizePolicy, QLabel, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGridLayout, QSpacerItem, QPushButton
)
from PyQt5.QtGui import QColor, QPainter, QPixmap, QFont, QIcon

class NonInteractiveLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

def create_custom_button(html_content, style=None):
    button = QPushButton()
    
    if style is None:
        button.setStyleSheet(style)

    layout = QVBoxLayout(button)
    #layout.setContentsMargins(5, 5, 5, 5)

    label = QLabel()
    label.setText(html_content)
    label.setWordWrap(True)
    layout.addWidget(label)

    return button

def generateListDataInGrid(grid,pos,labels, colors, percentage, expected = None):
    grid.setHorizontalSpacing(5)  # Adiciona um pequeno espaço entre as linhas

    i = 0
    for label, color, pct in zip(labels, colors, percentage):
        # Converte a cor de float (0.0 a 1.0) para inteiro (0 a 255)
        r, g, b, a = (int(c * 255) for c in color[:4])

        # Cria um quadrado com a cor
        color_square = QWidget()
        color_square.setStyleSheet(
            f"""
            background-color: {QColor(r, g, b, a).name()};
            border: 1px solid black;
            padding: 3px;  /* Adiciona um padding para diminuir o quadrado interno */
            """
        )
        color_square.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Define o tamanho máximo e mínimo para o quadrado
        color_square.setMaximumSize(8, 8)  # Reduz o tamanho total do quadrado
        color_square.setMinimumSize(8, 8)

        # Cria o rótulo
        label_widget = QLabel(label)
        label_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        if expected is None:
            label_percentage = QLabel(f"{pct:.2f}%")
        else:
            label_percentage = QLabel(f"{pct:.2f}% / {expected[i]:.2f}%")
        label_percentage.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Adiciona um espaçador para ocupar o espaço restante
        spacer = QSpacerItem(20, 15, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Adiciona os widgets à grade
        grid.addWidget(color_square, pos, 1)  # Coluna 1: Quadrado
        grid.addWidget(label_widget, pos, 2)  # Coluna 2: Rótulo
        grid.addWidget(label_percentage, pos, 3)  # Coluna 3: Percentual
        grid.addItem(spacer, pos, 4)  # Coluna 4: Espaçador
        i += 1
        pos += 1

    return pos

def getValorMilharVirgula(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.format_string('%.2f', value, grouping=True)

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