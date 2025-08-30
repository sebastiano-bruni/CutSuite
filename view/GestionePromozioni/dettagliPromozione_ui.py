import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from controller.PromozioneController import PromozioneController
from view.GestionePromozioni.modificaPromozione_ui import ModificaPromozione


class DettagliPromozione(QMainWindow):
    promozione_modificata = pyqtSignal()

    def __init__(self, promozione):
        super().__init__()
        self.promozione = promozione
        self.setWindowTitle("CutSuite - Dettagli promozione")
        self.resize(600, 500)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.controller = PromozioneController()
        self.controller.reload()

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Dettagli promozione")
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

        headers = ["ID", "Nome", "Descrizione", "Soglia", "Sconto"]

        values = [
            str(self.promozione.id),
            self.promozione.nome,
            self.promozione.descrizione,
            str(self.promozione.soglia_promozione),
            f"{self.promozione.sconto_percentuale}%"
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

        edit_button = QPushButton("Modifica promozione")
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

        delete_button = QPushButton("Elimina promozione")
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
        print(f"Apertura modifica per promozione: {self.promozione.nome}")
        self.modifica_promozione()

    def handle_delete(self):
        reply = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare la promozione {self.promozione.nome}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.controller.rimuovi_promozione(self.promozione.id)
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Promozione {self.promozione.nome} eliminata con successo!"
                )
                self.promozione_modificata.emit()
                self.close()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Errore",
                    f"Errore durante l'eliminazione: {str(e)}"
                )

    def modifica_promozione(self):
        from view.GestionePromozioni.modificaPromozione_ui import ModificaPromozione
        self.modifica_window = ModificaPromozione(self.promozione)
        self.modifica_window.promozione_modificata.connect(self.promozione_modificata.emit)
        self.modifica_window.show()
        self.modifica_window.raise_()
        self.modifica_window.activateWindow()
