from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def format_label(label, pct):
    return f"{label}\n{pct:.1f}%"

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def plot_pie_chart(self, data, labels, title="Distribuição do Portfólio"):
        """
        Gera um gráfico de pizza no canvas.

        Parameters:
        - data: Lista de valores (percentuais ou absolutos).
        - labels: Lista de rótulos correspondentes aos dados.
        - title: Título do gráfico.
        """
        if len(data) != len(labels):
            raise ValueError("Os dados e os rótulos devem ter o mesmo comprimento.")
        
        self.ax.clear()
        self.ax.pie(data, labels=labels, autopct='%1.1f%%')
        self.ax.set_title(title)
        self.draw()

    def plot_concentric_donuts(self, data, labels, inner_labels = [], title=None, colors=None, inner_colors=None, radiusIn = 2,
            radiusOut = 4, sizeIn = 1, sizeOut = 1):
        """
        Gera um gráfico de anéis concêntricos no canvas.

        Parameters:
        - data: Lista de listas. Ex.: [[10, 20], [30, 50, 20]].
        - labels: Lista de rótulos externos.
        - inner_labels: Lista de rótulos internos.
        - title: Título do gráfico.
        - colors: Cores para os anéis externos.
        - inner_colors: Cores para os anéis internos.
        """
        if len(data[0]) != len(labels):
            raise ValueError("Os dados e os rótulos devem corresponder aos níveis interno e externo.")
        if len(data) == 2:
            if len(data[1]) != len(inner_labels):
                raise ValueError("Os dados e os rótulos devem corresponder aos níveis interno e externo.")

        self.ax.clear()

        if len(inner_labels) > 0:
            # Gráfico interno
            self.ax.pie(
                data[1],
                radius=radiusIn,
                labels=[format_label(label, pct) for label, pct in zip(inner_labels, [p / sum(data[1]) * 100 for p in data[1]])],
                autopct=None,
                colors=inner_colors,
                wedgeprops=dict(width=sizeIn, edgecolor='w'),
                textprops={'fontweight': 'bold'}
            )
        
        # Gráfico externo
        self.ax.pie(
            data[0],
            radius=radiusOut,
            labels=[format_label(label, pct) for label, pct in zip(labels, [p / sum(data[0]) * 100 for p in data[0]])],
            autopct=None,
            colors=colors,
            wedgeprops=dict(width=sizeOut, edgecolor='w'),
            textprops={'fontweight': 'bold'},
            labeldistance=0.75
        )
        if title is not None:   
            self.ax.set_title(title)
        self.draw()