import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QGroupBox,
    QScrollArea, QGridLayout, QMessageBox, QDateEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont

# Importa i controller che gestiscono la logica
from controller.PrenotazioneController import PrenotazioneController
from controller.ClienteController import ClienteController

# Importa le altre view per le azioni sulle prenotazioni
from view.GestionePrenotazioni.dettagliPrenotazione_ui import DettagliPrenotazione
from view.GestionePrenotazioni.inserisciPrenotazione_ui import InserisciPrenotazione


class GestionePrenotazioni(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Gestione Prenotazioni")
        self.resize(1200, 800)

        self.inserisci_window = None
        self.dettagli_window = None
        self.controller = PrenotazioneController()

        # Controller per i filtri
        self.cliente_controller = ClienteController()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("CutSuite - Gestione Prenotazioni")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                padding: 10px 0;
            }
        """)
        main_layout.addWidget(title_label)

        search_group = QGroupBox("Ricerca:")
        search_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        search_layout = QVBoxLayout(search_group)

        # Filtri
        filter_layout = QHBoxLayout()
        client_filter_layout = QVBoxLayout()
        client_label = QLabel("Ricerca per cliente")
        self.client_combo = QComboBox()
        self.client_combo.addItem("Tutti i clienti", None)
        for cliente in self.cliente_controller.get_tutti_clienti():
            self.client_combo.addItem(f"{cliente.nome} {cliente.cognome}", cliente.id)
        client_filter_layout.addWidget(client_label)
        client_filter_layout.addWidget(self.client_combo)

        date_filter_layout = QVBoxLayout()
        date_label = QLabel("Ricerca per data")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        date_filter_layout.addWidget(date_label)
        date_filter_layout.addWidget(self.date_input)

        filter_layout.addLayout(client_filter_layout)
        filter_layout.addLayout(date_filter_layout)
        filter_layout.addStretch()
        search_layout.addLayout(filter_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        search_button = QPushButton("Cerca")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        search_button.clicked.connect(self.handle_search)

        reset_button = QPushButton("Reset")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #cccccc;
                color: #333333;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bbbbbb;
            }
        """)
        reset_button.clicked.connect(self.handle_reset)

        buttons_layout.addWidget(search_button)
        buttons_layout.addWidget(reset_button)
        search_layout.addLayout(buttons_layout)
        main_layout.addWidget(search_group)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        separator2.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator2)

        reservations_label = QLabel("Lista prenotazioni")
        reservations_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(reservations_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #cccccc;
                border-radius: 6px;
                background-color: white;
            }
        """)
        scroll_widget = QWidget()
        self.reservations_layout = QVBoxLayout(scroll_widget)
        self.reservations_layout.setSpacing(10)
        self.reservations_layout.setContentsMargins(15, 15, 15, 15)

        self.display_reservations(self.controller.get_tutte_prenotazioni())

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, 1)

        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.HLine)
        separator3.setFrameShadow(QFrame.Shadow.Sunken)
        separator3.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator3)

        add_button = QPushButton("Inserisci Prenotazione")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_button.clicked.connect(self.handle_add)
        main_layout.addWidget(add_button)

    def display_reservations(self, reservations):
        for i in reversed(range(self.reservations_layout.count())):
            item = self.reservations_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        for res in reservations:
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 6px;
                    padding: 10px;
                }
            """)
            layout = QHBoxLayout(frame)

            data_layout = QVBoxLayout()
            cliente_nome_completo = f"{res.cliente.nome} {res.cliente.cognome}" if res.cliente else "N/A"
            client_label = QLabel(f"Cliente: {cliente_nome_completo}")
            service_label = QLabel(f"Servizio: {res.servizio.nome}")
            data_label = QLabel(f"Data: {res.data.strftime('%d/%m/%Y')}")
            time_label = QLabel(f"Ora: {res.ora.strftime('%H:%M')}")

            data_layout.addWidget(client_label)
            data_layout.addWidget(service_label)
            data_layout.addWidget(data_label)
            data_layout.addWidget(time_label)
            data_layout.addStretch()

            layout.addLayout(data_layout, 1)

            details_btn = QPushButton("Dettagli")
            details_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 12px;
                    font-size: 12px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #5a6268;
                }
            """)
            details_btn.clicked.connect(lambda checked, r=res: self.handle_details(r))
            layout.addWidget(details_btn)

            self.reservations_layout.addWidget(frame)

        self.reservations_layout.addStretch()

    def handle_search(self):
        self.controller.reload()
        client_id = self.client_combo.currentData()
        date_qdate = self.date_input.date()

        filtered = self.controller.get_tutte_prenotazioni()

        if client_id:
            filtered = [r for r in filtered if r.cliente and r.cliente.id == client_id]

        search_date = date_qdate.toPyDate()
        filtered = [r for r in filtered if r.data.date() == search_date]

        self.display_reservations(filtered)

    def handle_reset(self):
        self.client_combo.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())
        self.display_reservations(self.controller.get_tutte_prenotazioni())

    def handle_add(self):
        print("Apertura form per inserimento nuova prenotazione")
        self.inserisci_prenotazione()

    def handle_details(self, res):
        print(f"Apertura dettagli per prenotazione: {res.cliente.nome} {res.cliente.cognome}")
        self.dettagli_prenotazione(res)

    def inserisci_prenotazione(self):
        self.inserisci_window = InserisciPrenotazione()
        self.inserisci_window.prenotazione_inserita.connect(self.aggiorna_lista_prenotazioni)
        self.inserisci_window.show()
        self.inserisci_window.raise_()
        self.inserisci_window.activateWindow()

    def dettagli_prenotazione(self, res):
        from view.GestionePrenotazioni.dettagliPrenotazione_ui import DettagliPrenotazione
        self.dettagli_window = DettagliPrenotazione(res)
        self.dettagli_window.prenotazione_modificata.connect(self.aggiorna_lista_prenotazioni)
        self.dettagli_window.show()
        self.dettagli_window.raise_()
        self.dettagli_window.activateWindow()

    def aggiorna_lista_prenotazioni(self):
        print("Aggiorno lista prenotazioni...")
        self.controller.reload()
        self.display_reservations(self.controller.get_tutte_prenotazioni())
