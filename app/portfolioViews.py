from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QListWidget
from graphics import MatplotlibCanvas  # Importe a classe MatplotlibCanvas

class PortFolioWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar título da janela
        self.setWindowTitle("Consolidador de Investimentos")

        # Criar widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal (horizontal)
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
        main_layout.addLayout(controls_layout, stretch=1)  # Menor espaço para controles
        main_layout.addLayout(canvas_layout, stretch=3)  # Maior espaço para o Canvas
        

        # Configurar o layout no widget central
        central_widget.setLayout(main_layout)

        # Configurações da janela
        self.setWindowFlags(Qt.Window)  # Habilita botões de fechar, minimizar e maximizar
        self.showMaximized()  # Mostra a janela maximizada com os botões