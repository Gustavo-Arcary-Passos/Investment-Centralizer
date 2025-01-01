import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

# Importar o módulo de views
from views import MainWindow  # Suponha que você tenha uma classe MainWindow em views.py

def main():
    # Criar a instância do QApplication
    app = QApplication(sys.argv)

    # Criar a janela principal
    window = MainWindow()

    # Exibir a janela
    window.show()

    # Iniciar o loop de eventos do PyQt
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

# Importar o módulo de views
from app.views import MainWindow  # Suponha que você tenha uma classe MainWindow em views.py

def main():
    # Criar a instância do QApplication
    app = QApplication(sys.argv)

    # Criar a janela principal
    window = MainWindow()

    # Exibir a janela
    window.show()

    # Iniciar o loop de eventos do PyQt
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
