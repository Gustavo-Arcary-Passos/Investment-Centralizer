from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLineEdit, QPushButton

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

table = QTableWidget(3, 3)  # 3 linhas e 3 colunas

for row in range(3):
    for col in range(3):
        if col == 2:  # Última coluna, adiciona um botão
            button = QPushButton(f"Botão {row + 1}")
            table.setCellWidget(row, col, button)
        if col == 1:
            edit = QLineEdit()
            table.setCellWidget(row, col, edit)
        else:
            table.setItem(row, col, QTableWidgetItem(f"Célula {row + 1}, {col + 1}"))

layout.addWidget(table)
window.setLayout(layout)
window.show()
app.exec_()
