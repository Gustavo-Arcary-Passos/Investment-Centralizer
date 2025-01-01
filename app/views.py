from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Consolidador de Investimentos")
        self.setGeometry(100, 100, 600, 400)

        # Criar o layout e adicionar widgets
        layout = QVBoxLayout()
        label = QLabel("Bem-vindo ao Consolidador de Investimentos!", self)
        layout.addWidget(label)

        # Criar um widget central para a janela
        central_widget = QWidget(self)
        central_widget.setLayout(layout)

        # Definir o widget central da janela principal
        self.setCentralWidget(central_widget)
