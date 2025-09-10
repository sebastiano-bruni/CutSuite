import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout, QMessageBox,
    QTextEdit, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from controller.PrenotazioneController import PrenotazioneController
from controller.RicevutaController import RicevutaController
from model.Ricevuta import Ricevuta


class DettagliPrenotazione(QMainWindow):
    prenotazione_modificata = pyqtSignal()

    def __init__(self, prenotazione, parent_window=None):
        super().__init__()
        self.prenotazione = prenotazione
        self.parent_window = parent_window
        self.setWindowTitle("CutSuite - Dettagli prenotazione")
        self.resize(700, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.prenotazione_controller = PrenotazioneController()
        self.ricevuta_controller = RicevutaController()

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Dettagli prenotazione")
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

        headers = ["ID", "Cliente", "Data", "Ora", "Servizio", "Dipendente", "Durata",
                   "Prezzo", "Stato", "Email Cliente", "Note"]

        cliente_nome = f"{self.prenotazione.cliente.nome} {self.prenotazione.cliente.cognome}" if self.prenotazione.cliente else "N/A"
        servizio_nome = self.prenotazione.servizio.nome if self.prenotazione.servizio else "N/A"
        dipendente_nome = f"{self.prenotazione.dipendente.nome} {self.prenotazione.dipendente.cognome}" if self.prenotazione.dipendente else "N/A"

        values = [
            str(self.prenotazione.id),
            cliente_nome,
            self.prenotazione.data.strftime('%d/%m/%Y'),
            self.prenotazione.ora.strftime('%H:%M'),
            servizio_nome,
            dipendente_nome,
            f"{self.prenotazione.durata_minuti} minuti",
            f"{self.prenotazione.prezzo} €",
            self.prenotazione.stato,
            self.prenotazione.email_cliente,
            self.prenotazione.note
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

        details_layout.setColumnStretch(0, 1)
        details_layout.setColumnStretch(1, 2)
        main_layout.addWidget(details_frame)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #cccccc; margin: 10px 0;")
        main_layout.addWidget(separator)

        # Pulsanti Azioni
        buttons_layout = QVBoxLayout()

        # Pulsante Emetti ricevuta
        self.receipt_button = QPushButton("Emetti ricevuta")
        self.receipt_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.receipt_button.clicked.connect(self.handle_receipt_emission)
        buttons_layout.addWidget(self.receipt_button)

        # Pulsante Modifica
        self.edit_button = QPushButton("Modifica prenotazione")
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #f1c40f;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f39c12; }
        """)
        self.edit_button.clicked.connect(self.handle_edit)
        buttons_layout.addWidget(self.edit_button)

        # Pulsante Elimina
        self.delete_button = QPushButton("Elimina prenotazione")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c82333; }
        """)
        self.delete_button.clicked.connect(self.handle_delete)
        buttons_layout.addWidget(self.delete_button)

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

    def handle_receipt_emission(self):
        try:
            # Creazione di un oggetto Ricevuta e stampa
            nuova_ricevuta = Ricevuta(
                prenotazione=self.prenotazione,
                importo_totale=self.prenotazione.prezzo,
                dettagli=self.prenotazione.servizio.descrizione
            )
            self.ricevuta_controller.aggiungi_ricevuta(nuova_ricevuta)

            self.prenotazione_controller.aggiorna_prenotazione(
                self.prenotazione.id,
                stato="pagata"
            )
            self.prenotazione.stato = "pagata"
            self.prenotazione_modificata.emit()

            # Genera il file PDF e lo salva
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Salva ricevuta",
                f"ricevuta_{nuova_ricevuta.id}.pdf",
                "PDF Files (*.pdf)"
            )
            if filename:
                nuova_ricevuta.genera_pdf(filename)
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Ricevuta #{nuova_ricevuta.id} emessa e salvata come '{filename}'."
                )
            else:
                QMessageBox.warning(self, "Annullato", "Operazione annullata.")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Errore",
                f"Si è verificato un errore nell'emissione della ricevuta: {str(e)}"
            )

    def handle_edit(self):
        print(f"Apertura modifica per prenotazione: {self.prenotazione.id}")
        self.modifica_prenotazione()

    def handle_delete(self):
        reply = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare la prenotazione #{self.prenotazione.id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.prenotazione_controller.rimuovi_prenotazione(self.prenotazione.id)
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Prenotazione #{self.prenotazione.id} eliminata con successo!"
                )

                if self.parent_window and hasattr(self.parent_window, 'aggiorna_lista_prenotazioni'):
                    self.parent_window.aggiorna_lista_prenotazioni()

                self.close()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Errore",
                    f"Errore durante l'eliminazione: {str(e)}"
                )

    def modifica_prenotazione(self):
        from view.GestionePrenotazioni.modificaPrenotazione_ui import ModificaPrenotazione
        self.modifica_window = ModificaPrenotazione(self.prenotazione)
        self.modifica_window.prenotazione_modificata.connect(self.prenotazione_modificata.emit)
        self.modifica_window.show()
        self.modifica_window.raise_()
        self.modifica_window.activateWindow()
