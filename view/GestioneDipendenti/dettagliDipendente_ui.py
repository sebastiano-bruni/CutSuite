import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from controller.DipendenteController import DipendenteController
from view.GestioneDipendenti.modificaDipendente_ui import ModificaDipendente


class DettagliDipendente(QMainWindow):
    dipendente_modificato = pyqtSignal()

    def __init__(self, dipendente):
        super().__init__()
        self.dipendente = dipendente
        self.setWindowTitle("CutSuite - Dettagli Dipendente")
        self.resize(600, 500)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.controller = DipendenteController()
        self.controller.reload()

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Dettagli dipendente")
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
                   "Username", "Ruolo", "Stipendio"]

        values = [
            str(self.dipendente.id),
            self.dipendente.nome,
            self.dipendente.cognome,
            self.dipendente.email,
            self.dipendente.telefono,
            self.dipendente.username,
            self.dipendente.ruolo if hasattr(self.dipendente, 'ruolo') else 'Proprietario',
            # Corretto il valore del ruolo
            str(self.dipendente.stipendio) if hasattr(self.dipendente, 'stipendio') else "N/A"  # Corretto lo stipendio
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

        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        edit_button = QPushButton("Modifica dipendente")
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

        delete_button = QPushButton("Elimina dipendente")
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

    def handle_edit(self):
        print(f"Apertura modifica per dipendente: {self.dipendente.nome} {self.dipendente.cognome}")
        self.modifica_dipendente()

    def handle_delete(self):
        reply = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare il dipendente {self.dipendente.nome} {self.dipendente.cognome}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.rimuovi_dipendente(self.dipendente.id)
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Dipendente {self.dipendente.nome} {self.dipendente.cognome} eliminato con successo!"
                )
                self.close()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Errore",
                    f"Errore durante l'eliminazione: {str(e)}"
                )

    def modifica_dipendente(self):
        self.dip_window = ModificaDipendente(self.dipendente)
        self.dip_window.dipendente_modificato.connect(self.dipendente_modificato.emit)
        self.dip_window.show()
        self.dip_window.raise_()
        self.dip_window.activateWindow()