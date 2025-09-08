from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem
)

class StatisticheServiziDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Statistiche Servizi")
        self.resize(700, 500)
        self.controller = controller

        layout = QVBoxLayout(self)

        filter_layout = QHBoxLayout()
        self.filter_label = QLabel("Filtra per attributo:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Nome", "Prezzo", "Durata"])  # Attributi reali dei servizi
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Inserisci valore per il filtro")
        self.btn_filtra = QPushButton("Applica Filtro")

        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(self.filter_input)
        filter_layout.addWidget(self.btn_filtra)
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nome", "Prezzo (€)", "Durata (minuti)"])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.servizi = self.controller.get_tutti_servizi()
        self.show_data(self.servizi)

        self.btn_filtra.clicked.connect(self.apply_filter)

    def show_data(self, data):
        self.table.setRowCount(len(data))
        for row, servizio in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(servizio.nome))
            self.table.setItem(row, 1, QTableWidgetItem(str(servizio.prezzo)))
            self.table.setItem(row, 2, QTableWidgetItem(str(servizio.durata_minuti)))

    def apply_filter(self):
        filtro_colonna = self.filter_combo.currentText()
        filtro_valore = self.filter_input.text().lower()

        if not filtro_valore:
            self.show_data(self.servizi)
            return

        if filtro_colonna == "Nome":
            filtrati = [s for s in self.servizi if filtro_valore in s.nome.lower()]
        elif filtro_colonna == "Prezzo":
            try:
                prezzo_val = float(filtro_valore)
                filtrati = [s for s in self.servizi if s.prezzo == prezzo_val]
            except ValueError:
                filtrati = []
        elif filtro_colonna == "Durata":
            try:
                durata_val = int(filtro_valore)
                filtrati = [s for s in self.servizi if s.durata_minuti == durata_val]
            except ValueError:
                filtrati = []
        else:
            filtrati = self.servizi

        self.show_data(filtrati)
