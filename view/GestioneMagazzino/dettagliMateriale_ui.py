import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from controller.MaterialeController import MaterialeController
from view.GestioneMagazzino.modificaMateriale_ui import ModificaMateriale


class DettagliMateriale(QMainWindow):
    materiale_modificato = pyqtSignal()

    def __init__(self, materiale):
        super().__init__()
        self.materiale = materiale
        self.setWindowTitle("CutSuite - Dettagli materiale")
        self.resize(600, 500)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.controller = MaterialeController()
        self.controller.reload()  # Assicurati che i dati siano aggiornati

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Dettagli materiale")
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

        headers = ["ID", "Nome", "Categoria", "Prezzo", "Quantità", "Soglia scorte"]

        values = [
            str(self.materiale.id),
            self.materiale.nome,
            self.materiale.categoria,
            f"{self.materiale.prezzo} €",
            str(self.materiale.quantita),
            str(self.materiale.soglia_scorte)
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

        self.edit_button = QPushButton("Modifica materiale")
        self.edit_button.setStyleSheet("""
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
        self.edit_button.clicked.connect(self.handle_edit)

        delete_button = QPushButton("Elimina materiale")
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
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch()

        main_layout.addWidget(buttons_container)
        main_layout.addStretch()

    def handle_edit(self):
        print(f"Apertura modifica per materiale: {self.materiale.nome}")
        self.modifica_materiale()

    def handle_delete(self):
        reply = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare il materiale {self.materiale.nome}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.rimuovi_materiale(self.materiale.id)
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Materiale {self.materiale.nome} eliminato con successo!"
                )
                self.close()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Errore",
                    f"Errore durante l'eliminazione: {str(e)}"
                )

    def modifica_materiale(self):
        self.modifica_window = ModificaMateriale(self.materiale)
        self.modifica_window.materiale_modificato.connect(self.materiale_modificato.emit)
        self.modifica_window.show()
        self.modifica_window.raise_()
        self.modifica_window.activateWindow()
