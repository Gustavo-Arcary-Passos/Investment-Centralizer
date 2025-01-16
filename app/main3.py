from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Itens em 4 Colunas")

        # Layout principal
        layout = QVBoxLayout(self)

        # Criação do QListWidget
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Configuração para exibir itens em 4 colunas
        self.list_widget.setFlow(QListWidget.LeftToRight)  # Modo de layout horizontal
        self.list_widget.setWrapping(True)  # Permitir quebra de linha
        self.list_widget.setSpacing(10)  # Espaçamento entre itens
        self.list_widget.setResizeMode(QListWidget.Adjust)

        # Ajuste do tamanho de cada item
        item_width = 100
        item_height = 50
        self.list_widget.setGridSize(QSize(item_width + 10, item_height + 10))

        # Adicionar itens
        for i in range(20):  # Exemplo com 20 itens
            item = QListWidgetItem(f"Item {i + 1}")
            item.setSizeHint(QSize(item_width, item_height))
            self.list_widget.addItem(item)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
