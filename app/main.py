import sys
from PyQt5.QtWidgets import QApplication
from views import  WindowManager

def main():
    # Criar a instância do QApplication
    app = QApplication(sys.argv)

    # Criar a janela inicial
    start_window = WindowManager()

    # Exibir a janela inicial
    start_window.show()

    # Iniciar o loop de eventos do PyQt
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()