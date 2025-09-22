import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from controller.ClienteController import ClienteController
from view.GestioneClienti.modificaCliente_ui import ModificaCliente
from signals import app_signals


class DettagliCliente(QMainWindow):
    cliente_modificato = pyqtSignal()

    def __init__(self, cliente, parent_window=None):
        super().__init__()
        self.cliente = cliente
        self.parent_window = parent_window
        self.setWindowTitle("CutSuite - Dettagli cliente")
        self.resize(600, 500)
        self.value_labels = {}  # Dizionario per memorizzare le etichette
        self.init_ui()

        app_signals.cliente_modificato.connect(self.handle_aggiornamento_esterno)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.controller = ClienteController()
        self.controller.reload()

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Dettagli cliente")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                padding: 10px 0;
            }
        """)
        main_layout.addWidget(title_label)

        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 0px;
            }
        """)
        details_layout = QGridLayout(details_frame)
        details_layout.setSpacing(0)
        details_layout.setContentsMargins(0, 0, 0, 0)

        headers = ["ID", "Nome", "Cognome", "Email", "Telefono",
                   "Codice Fiscale", "Numero Appuntamenti"]

        values = [
            str(self.cliente.id),
            self.cliente.nome,
            self.cliente.cognome,
            self.cliente.email,
            self.cliente.telefono,
            self.cliente.cf,
            str(self.cliente.numVisite),
        ]

        for i, (header, value) in enumerate(zip(headers, values)):
            header_label = QLabel(header)
            header_label.setStyleSheet("""
                QLabel {
                    background-color: #f8f9fa;
                    padding: 12px;
                    border: 1px solid #e0e0e0;
                    font-weight: bold;
                    color: #333333;
                }
            """)
            header_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            value_label = QLabel(value)
            value_label.setStyleSheet("""
                QLabel {
                    background-color: white;
                    padding: 12px;
                    border: 1px solid #e0e0e0;
                    color: #555555;
                }
            """)
            value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            details_layout.addWidget(header_label, i, 0)
            details_layout.addWidget(value_label, i, 1)

            # Aggiungi l'etichetta al dizionario per poterla aggiornare
            self.value_labels[header] = value_label

        details_layout.setColumnStretch(0, 1)
        details_layout.setColumnStretch(1, 2)
        main_layout.addWidget(details_frame)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #cccccc; margin: 10px 0;")
        main_layout.addWidget(separator)

        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        edit_button = QPushButton("Modifica")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        edit_button.clicked.connect(self.handle_edit)

        delete_button = QPushButton("Elimina")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_button.clicked.connect(self.handle_delete)

        buttons_layout.addStretch()
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch()

        main_layout.addWidget(buttons_container)
        main_layout.addStretch()

    def handle_aggiornamento_esterno(self, cliente_id):
        """ Questo metodo viene chiamato quando il segnale globale viene emesso. """
        # Controlla se l'aggiornamento riguarda proprio il cliente visualizzato
        if self.cliente and self.cliente.id == cliente_id:
            print(f"La finestra dettagli del cliente {self.cliente.id} ha ricevuto un aggiornamento!")
            self.aggiorna_dettagli_cliente()

    def aggiorna_dettagli_cliente(self):
        """Ricarica i dati del cliente e aggiorna la UI."""
        print("Aggiornamento dettagli cliente...")
        self.controller.reload()
        self.cliente = self.controller.get_cliente_by_id(self.cliente.id)

        # Aggiorna il testo delle etichette con i nuovi dati
        self.value_labels["ID"].setText(str(self.cliente.id))
        self.value_labels["Nome"].setText(self.cliente.nome)
        self.value_labels["Cognome"].setText(self.cliente.cognome)
        self.value_labels["Email"].setText(self.cliente.email)
        self.value_labels["Telefono"].setText(self.cliente.telefono)
        self.value_labels["Codice Fiscale"].setText(self.cliente.cf)
        self.value_labels["Numero Appuntamenti"].setText(str(self.cliente.numVisite))

    def handle_edit(self):
        print(f"Apertura modifica per cliente: {self.cliente.nome} {self.cliente.cognome}")
        self.modifica_cliente()

    def handle_delete(self):
        reply = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare il cliente {self.cliente.nome} {self.cliente.cognome}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.rimuovi_cliente(self.cliente.id)
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Cliente {self.cliente.nome} {self.cliente.cognome} eliminato con successo!"
                )

                if self.parent_window and hasattr(self.parent_window, 'aggiorna_lista_clienti'):
                    self.parent_window.aggiorna_lista_clienti()

                self.close()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Errore",
                    f"Errore durante l'eliminazione: {str(e)}"
                )

    def modifica_cliente(self):
        self.client_window = ModificaCliente(self.cliente)
        self.client_window.cliente_modificato.connect(self.cliente_modificato.emit)
        self.client_window.show()
        self.client_window.raise_()
        self.client_window.activateWindow()

