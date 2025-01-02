from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QLineEdit, QPushButton, QWidget
from output import Ui_MainWindow  # Importar o código gerado pelo Qt Designer

class MainWindow(QMainWindow, Ui_MainWindow):  # Herda de Ui_MainWindow
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Chama o método setupUi da classe Ui_MainWindow
        self.setWindowTitle("Consolidador de Investimentos")
        self.showFullScreen()

        # Se precisar adicionar funcionalidades adicionais, como conectar botões, faça aqui
        self.pushButton_4.clicked.connect(self.handle_login)
        self.pushButton_5.clicked.connect(self.handle_create_login)

    def handle_login(self):
        # Lógica para login
        print("Login clicado!")

    def handle_create_login(self):
        # Lógica para criar login
        print("Criar login clicado!")


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login - Consolidador de Investimentos")
        self.setGeometry(100, 100, 1600, 1200)

        # Criar layout de login
        layout = QVBoxLayout()
        label = QLabel("Login", self)
        username_label = QLabel("Usuário:")
        self.username_input = QLineEdit(self)
        password_label = QLabel("Senha:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Entrar", self)
        login_button.clicked.connect(self.handle_login)

        # Adicionar widgets ao layout
        layout.addWidget(label)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        # Definir o layout central
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        layout.setContentsMargins(100, 100, 100, 100)
        self.setCentralWidget(central_widget)
        self.showFullScreen()

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Adicione a lógica de autenticação aqui
        if username == "admin" and password == "password":
            print("Login bem-sucedido!")
        else:
            print("Usuário ou senha incorretos!")
