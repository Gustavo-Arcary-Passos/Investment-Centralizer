import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.login import Login

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QSizePolicy, QSpacerItem, QLineEdit
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

        left_space = QWidget()
        hlayout.addWidget(left_space, stretch=2)

        midlayout = QVBoxLayout()

        self.login_button = QPushButton("Login")
        self.create_login_button = QPushButton("Create Login")
        midlayout.addWidget(QWidget())
    
        midlayout.addWidget(self.login_button)
        midlayout.addWidget(self.create_login_button)
        midlayout.addWidget(QWidget())
    
        mid_widget = QWidget()
        mid_widget.setLayout(midlayout)

        hlayout.addWidget(mid_widget, stretch=1)

        right_space = QWidget()
        hlayout.addWidget(right_space, stretch=2)

        self.setLayout(hlayout)

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

        hlayout = QHBoxLayout()

        left_space = QWidget()
        hlayout.addWidget(left_space, stretch=2)

        midlayout = QVBoxLayout()
        
        self.name_login = QLineEdit()
        self.name_login.setPlaceholderText("Nome")
        
        self.password_login = QLineEdit()
        self.password_login.setEchoMode(QLineEdit.Password)
        self.password_login.setPlaceholderText("Senha")
        
        self.login_button = QPushButton("Login")
        
        centerlayout = QVBoxLayout()
        centerlayout.setContentsMargins(0, 0, 0, 0)
        centerlayout.addWidget(self.name_login)
        centerlayout.addWidget(self.password_login)
        centerlayout.addWidget(self.login_button)

        midlayout.addWidget(QWidget())
        midlayout.addLayout(centerlayout)
        midlayout.addWidget(QWidget())

        mid_widget = QWidget()
        mid_widget.setLayout(midlayout)

        hlayout.addWidget(mid_widget, stretch=1)

        right_space = QWidget()
        hlayout.addWidget(right_space, stretch=2)

        self.setLayout(hlayout)

        self.login_button.clicked.connect(self.open_portfolio_window)

    def open_portfolio_window(self):
        if Login.checkLogin(self.name_login.text(), self.password_login.text()):
            parent = self.parentWidget()
            parent.parent().portfolio_window.getUserPortfolio(self.name_login.text())
            parent.setCurrentWidget(parent.parent().portfolio_window)

class CreateLoginWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        hlayout = QHBoxLayout()

        left_space = QWidget()
        hlayout.addWidget(left_space, stretch=2)

        midlayout = QVBoxLayout()
        
        self.name_creation = QLineEdit()
        self.name_creation.setPlaceholderText("Nome")
        
        self.password_creation = QLineEdit()
        self.password_creation.setEchoMode(QLineEdit.Password)
        self.password_creation.setPlaceholderText("Senha")

        self.finish_create_login_button = QPushButton("Create Login")
        
        centerlayout = QVBoxLayout()
        centerlayout.setContentsMargins(0, 0, 0, 0)
        centerlayout.addWidget(self.name_creation)
        centerlayout.addWidget(self.password_creation)
        centerlayout.addWidget(self.finish_create_login_button)

        midlayout.addWidget(QWidget())
        midlayout.addLayout(centerlayout)
        midlayout.addWidget(QWidget())

        mid_widget = QWidget()
        mid_widget.setLayout(midlayout)

        hlayout.addWidget(mid_widget, stretch=1)

        right_space = QWidget()
        hlayout.addWidget(right_space, stretch=2)

        self.setLayout(hlayout)

        self.finish_create_login_button.clicked.connect(self.open_start_window)

    def open_start_window(self):
        if Login.createLogin(self.name_creation.text(),self.password_creation.text()):
            parent = self.parentWidget()
            parent.setCurrentWidget(parent.parent().start_window)
