from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPalette, QColor

class ColoredWidget(QWidget):
    """Widget auxiliar para mostrar áreas com cores diferentes."""
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(color))
        self.setPalette(palette)

class StartWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        hlayout = QHBoxLayout()

        # Espaço à esquerda
        left_space = QWidget()
        hlayout.addWidget(left_space, stretch=2)

        # Layout para os botões (usando QVBoxLayout)
        midlayout = QVBoxLayout()

        self.login_button = QPushButton("Login")
        self.create_login_button = QPushButton("Create Login")
        midlayout.addWidget(QWidget())
        # Adicionando os botões ao layout
        midlayout.addWidget(self.login_button)
        midlayout.addWidget(self.create_login_button)
        midlayout.addWidget(QWidget())
        # Criando um QWidget para embutir o QVBoxLayout
        mid_widget = QWidget()
        mid_widget.setLayout(midlayout)

        # Adicionando o QWidget que contém o layout de botões ao QHBoxLayout
        hlayout.addWidget(mid_widget, stretch=1)

        # Espaço à direita
        right_space = QWidget()
        hlayout.addWidget(right_space, stretch=2)

        # Definir o layout principal da janela
        self.setLayout(hlayout)

        # Conectar os botões aos métodos
        self.login_button.clicked.connect(self.open_login_window)
        self.create_login_button.clicked.connect(self.open_create_login_window)

    def open_login_window(self):
        parent = self.parentWidget()
        parent.setCurrentWidget(parent.parent().login_window)

    def open_create_login_window(self):
        parent = self.parentWidget()
        parent.setCurrentWidget(parent.parent().create_login_window)

class LoginWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.login_button = QPushButton("Entrar")
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.login_button.clicked.connect(self.open_portfolio_window)

    def open_portfolio_window(self):
        parent = self.parentWidget()
        parent.setCurrentWidget(parent.parent().portfolio_window)

class CreateLoginWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.finish_create_login_button = QPushButton("Entrar")
        layout.addWidget(self.finish_create_login_button)

        self.setLayout(layout)

        self.finish_create_login_button.clicked.connect(self.open_start_window)

    def open_start_window(self):
        parent = self.parentWidget()
        parent.setCurrentWidget(parent.parent().start_window)
