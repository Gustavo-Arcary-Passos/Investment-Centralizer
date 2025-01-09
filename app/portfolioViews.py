from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QListWidget, QSizePolicy
from graphics import MatplotlibCanvas

class PortFolioWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        main_layout = QHBoxLayout()

        # Espaço do Canvas à esquerda
        canvas_layout = QVBoxLayout()
        self.canvas = MatplotlibCanvas(self, width=8, height=6, dpi=100)  # Adiciona o canvas
        canvas_layout.addWidget(self.canvas)

        # Exemplo de gráfico
        data = [30, 40, 30]
        labels = ['Ação 1', 'Ação 2', 'Ação 3']
        self.canvas.plot_pie_chart(data, labels)

        # Espaço para filtros e controles à direita
        controls_layout = QVBoxLayout()
        filter_label = QLabel("Filtros")
        filter_list = QListWidget()
        filter_list.addItems(["Filtro 1", "Filtro 2", "Filtro 3"])
        apply_button = QPushButton("Aplicar Filtro")

        controls_layout.addWidget(filter_label)
        controls_layout.addWidget(filter_list)
        controls_layout.addWidget(apply_button)

        # Adicionar os layouts ao layout principal
        main_layout.addLayout(controls_layout, stretch=1)
        main_layout.addLayout(canvas_layout, stretch=3)

        # Configurar o layout no widget
        self.setLayout(main_layout)
