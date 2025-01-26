from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton

app = QApplication([])

# Configuração inicial da tabela
window = QWidget()
layout = QVBoxLayout()
table = QTableWidget(3, 3)  # 3 linhas, 3 colunas
layout.addWidget(table)

# Preencher a tabela inicialmente
for row in range(3):
    for col in range(3):
        table.setItem(row, col, QTableWidgetItem(f"Item {row+1}, {col+1}"))

# Botão para adicionar uma nova linha
def add_row():
    row = table.rowCount()
    table.insertRow(row)  # Adiciona uma nova linha
    for col in range(table.columnCount()):
        table.setItem(row, col, QTableWidgetItem(f"Novo {row+1}, {col+1}"))

button = QPushButton("Adicionar Linha")
button.clicked.connect(add_row)
layout.addWidget(button)

window.setLayout(layout)
window.show()
app.exec_()
