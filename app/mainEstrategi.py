from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QLabel, QListWidget, QListWidgetItem,
    QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QSpinBox
)


class CustomCell(QWidget):
    """Widget personalizado que combina QListWidget e QGridLayout."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Criação do QListWidget para receber drops
        self.list_widget = QListWidget()
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setDefaultDropAction(Qt.MoveAction)

        # Conectar os eventos de drag and drop
        self.list_widget.dragEnterEvent = self.dragEnterEvent
        self.list_widget.dropEvent = self.dropEvent
        self.main_layout.addWidget(self.list_widget)

        # Criação do QGridLayout para valores inteiros e percentuais
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 1)
        self.main_layout.addWidget(self.grid_widget)

        # Adicionar cabeçalhos no QGridLayout
        self.add_grid_headers()

    def add_grid_headers(self):
        """Adiciona cabeçalhos às colunas do QGridLayout."""
        self.grid_layout.addWidget(QLabel("Valor Inteiro"), 0, 0, Qt.AlignCenter)
        self.grid_layout.addWidget(QLabel("Percentual"), 0, 1, Qt.AlignCenter)

    def dragEnterEvent(self, event):
        """Aceita o evento de drag se for texto."""
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Adiciona item ao QListWidget e gera uma linha no QGridLayout."""
        if event.mimeData().hasText():
            # Adiciona item ao QListWidget
            item_text = event.mimeData().text()
            self.list_widget.addItem(item_text)

            # Adiciona uma nova linha ao QGridLayout
            row_count = self.grid_layout.rowCount()
            int_input = QSpinBox()  # Campo para valores inteiros
            percent_input = QLineEdit("0%")  # Campo para percentuais
            percent_input.setAlignment(Qt.AlignCenter)

            self.grid_layout.addWidget(int_input, row_count, 0)
            self.grid_layout.addWidget(percent_input, row_count, 1)
            event.accept()
        else:
            event.ignore()


class MainWindow(QWidget):
    """Janela principal com QGridLayout."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop with Custom QGridLayout Cell")
        self.setMinimumSize(800, 600)

        # Layout principal
        main_layout = QGridLayout(self)

        # Adicionar uma célula personalizada ao layout
        custom_cell = CustomCell()
        main_layout.addWidget(custom_cell, 0, 0)

        # Adicionar um QListWidget de exemplo para arrastar
        source_list = QListWidget()
        source_list.setDragEnabled(True)
        for i in range(5):
            source_list.addItem(QListWidgetItem(f"Item {i + 1}"))
        main_layout.addWidget(source_list, 0, 1)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()
