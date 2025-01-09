from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QSizePolicy
from portfolioViews import PortFolioWindow
from loginViews import StartWindow, LoginWindow, CreateLoginWindow

class WindowManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicativo de Investimentos")

        # Configurar o QStackedWidget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        # Criar e adicionar as janelas ao QStackedWidget
        self.start_window = StartWindow(self.central_widget)
        self.create_login_window = CreateLoginWindow(self.central_widget)
        self.login_window = LoginWindow(self.central_widget)
        self.portfolio_window = PortFolioWindow()

        self.central_widget.addWidget(self.start_window)
        self.central_widget.addWidget(self.create_login_window)
        self.central_widget.addWidget(self.login_window)
        self.central_widget.addWidget(self.portfolio_window)

        # Mostrar a janela de login inicialmente
        self.central_widget.setCurrentWidget(self.start_window)

        self.showMaximized()