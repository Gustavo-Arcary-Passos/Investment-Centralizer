import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from graphics import MatplotlibCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfólio de Investimentos")

        # Canvas de Gráficos
        self.canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        # Dados de exemplo
        outer_data = [50, 30, 20]  # Gráfico externo
        inner_data = [70, 30]      # Gráfico interno
        labels = ["Ações", "Renda Fixa", "Fundos"]
        inner_labels = ["Alta Renda", "Baixa Renda"]

        # Gerar Gráfico
        self.canvas.plot_concentric_donuts(
            data=[outer_data],
            labels=labels,
            radiusOut = 1.5,
            sizeOut= 0.5
            # inner_labels=inner_labels
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
