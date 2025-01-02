import sys
from PyQt5.QtWidgets import QApplication
from views import MainWindow, LoginWindow  # Importar as janelas do arquivo views.py


def main():
    # Criar a instância do QApplication
    app = QApplication(sys.argv)

    # Criar a janela de login
    login_window = MainWindow()

    # Exibir a janela de login
    login_window.show()

    # Iniciar o loop de eventos do PyQt
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
