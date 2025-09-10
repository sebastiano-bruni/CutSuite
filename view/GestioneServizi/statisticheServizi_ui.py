from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QWidget
)

class StatisticheServiziDialog(QDialog):
    def __init__(self, servizio_controller, prenotazione_controller, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Statistiche Servizi")
        self.resize(800, 500)
        self.servizio_controller = servizio_controller
        self.prenotazione_controller = prenotazione_controller

        layout = QVBoxLayout(self)

        # Layout filtri
        filter_layout = QHBoxLayout()
        self.filter_label = QLabel("Filtra per attributo:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Nome", "Prezzo", "Durata"])
        self.filter_combo.currentTextChanged.connect(self.toggle_filter_input)

        # Campo di input in contenitore fisso
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Inserisci valore per il filtro")
        self.input_container = QWidget()
        input_layout = QVBoxLayout(self.input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.addWidget(self.filter_input)
        self.input_container.setFixedWidth(200)  # larghezza fissa

        self.btn_filtra = QPushButton("Applica Filtro")

        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(self.input_container)
        filter_layout.addWidget(self.btn_filtra)
        layout.addLayout(filter_layout)

        # Tabella
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Nome", "Prezzo (€)", "Durata (minuti)",
            "Totale Servizi", "Prenotazioni Pagate"
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # Dati iniziali
        self.servizi = self.servizio_controller.get_tutti_servizi()
        self.show_data(self.servizi)

        self.btn_filtra.clicked.connect(self.apply_filter)

    def show_data(self, data):
        self.table.setRowCount(len(data))
        for row, servizio in enumerate(data):
            prenotazioni = [
                p for p in self.prenotazione_controller.get_tutte_prenotazioni()
                if p.servizio.id == servizio.id
            ]
            pagate_count = sum(1 for p in prenotazioni if p.stato.lower() == "pagata")

            self.table.setItem(row, 0, QTableWidgetItem(servizio.nome))
            self.table.setItem(row, 1, QTableWidgetItem(str(servizio.prezzo)))
            self.table.setItem(row, 2, QTableWidgetItem(str(servizio.durata_minuti)))
            self.table.setItem(row, 3, QTableWidgetItem(str(len(prenotazioni))))
            self.table.setItem(row, 4, QTableWidgetItem(str(pagate_count)))

    def apply_filter(self):
        filtro_colonna = self.filter_combo.currentText()
        filtro_valore = self.filter_input.text().lower()

        if filtro_colonna == "Nome":
            filtrati = [s for s in self.servizi if filtro_valore in s.nome.lower()]
        elif filtro_colonna == "Prezzo":
            filtrati = sorted(self.servizi, key=lambda s: s.prezzo, reverse=True)
        elif filtro_colonna == "Durata":
            filtrati = sorted(self.servizi, key=lambda s: s.durata_minuti, reverse=True)
        else:
            filtrati = self.servizi

        self.show_data(filtrati)

    def toggle_filter_input(self, text):
        if text == "Nome":
            self.filter_input.show()
        else:
            self.filter_input.hide()
