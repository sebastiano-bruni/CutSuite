import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QSpinBox,
    QDoubleSpinBox, QTextEdit, QDateEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont

from controller.PromozioneController import PromozioneController
from model.Promozione import Promozione
from datetime import datetime


class InserisciPromozione(QMainWindow):
    promozione_inserita = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Inserisci promozione")
        self.resize(500, 600)
        self.controller = PromozioneController()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Inserisci promozione")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                padding: 10px 0;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 0px;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(25, 25, 25, 25)

        self.input_fields = {}

        self.nome_input = self.create_input("Nome:", placeholder="Es. Sconto 20%")
        self.descrizione_input = self.create_textedit("Descrizione:", placeholder="Descrizione della promozione")
        self.soglia_spinbox = self.create_spinbox("Soglia:", min_val=0, max_val=100)
        self.sconto_spinbox = self.create_spinbox("Sconto (%):", min_val=0, max_val=100)
        self.data_inizio_input = self.create_date_input("Data Inizio:")
        self.data_fine_input = self.create_date_input("Data Fine:")

        form_layout.addLayout(self.nome_input)
        form_layout.addLayout(self.descrizione_input)
        form_layout.addLayout(self.soglia_spinbox)
        form_layout.addLayout(self.sconto_spinbox)
        form_layout.addLayout(self.data_inizio_input)
        form_layout.addLayout(self.data_fine_input)

        main_layout.addWidget(form_frame)

        confirm_button = QPushButton("Conferma")
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        confirm_button.clicked.connect(self.handle_confirm)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(confirm_button)
        main_layout.addWidget(button_container)
        main_layout.addStretch()

    def create_input(self, label_text, placeholder=""):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        line_edit.setMinimumHeight(35)
        v_layout.addWidget(label)
        v_layout.addWidget(line_edit)
        self.input_fields[label_text.replace(":", "").strip().lower()] = line_edit
        return v_layout

    def create_textedit(self, label_text, placeholder=""):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder)
        text_edit.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        text_edit.setMinimumHeight(80)
        v_layout.addWidget(label)
        v_layout.addWidget(text_edit)
        self.input_fields[label_text.replace(":", "").strip().lower()] = text_edit
        return v_layout

    def create_spinbox(self, label_text, value=0, min_val=0, max_val=100):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(value)
        spinbox.setStyleSheet("""
            QSpinBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        spinbox.setMinimumHeight(35)
        v_layout.addWidget(label)
        v_layout.addWidget(spinbox)
        self.input_fields[label_text.replace(":", "").strip().lower()] = spinbox
        return v_layout

    def create_date_input(self, label_text):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_edit.setStyleSheet("""
            QDateEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        date_edit.setMinimumHeight(35)
        v_layout.addWidget(label)
        v_layout.addWidget(date_edit)
        self.input_fields[label_text.replace(":", "").strip().lower()] = date_edit
        return v_layout

    def validate_data(self, nome, descrizione, sconto, data_inizio, data_fine):
        errors = []
        if not nome or len(nome) < 3:
            errors.append("• Il nome della promozione deve contenere almeno 3 caratteri.")
        if not descrizione:
            errors.append("• La descrizione non può essere vuota.")
        if sconto <= 0:
            errors.append("• Lo sconto deve essere maggiore di zero.")
        if data_fine < data_inizio:
            errors.append("• La data di fine non può essere precedente alla data di inizio.")
        return errors

    def handle_confirm(self):
        nome = self.input_fields['nome'].text().strip()
        descrizione = self.input_fields['descrizione'].toPlainText().strip()
        soglia = self.input_fields['soglia'].value()
        sconto = self.input_fields['sconto (%)'].value()
        data_inizio_qdate = self.input_fields['data inizio'].date()
        data_fine_qdate = self.input_fields['data fine'].date()

        data_inizio = datetime(data_inizio_qdate.year(), data_inizio_qdate.month(), data_inizio_qdate.day())
        data_fine = datetime(data_fine_qdate.year(), data_fine_qdate.month(), data_fine_qdate.day())

        errors = self.validate_data(nome, descrizione, sconto, data_inizio, data_fine)
        if errors:
            error_message = "Si sono verificati i seguenti errori:\n\n" + "\n".join(errors)
            QMessageBox.critical(self, "Errori di validazione", error_message)
            return

        controller = PromozioneController()

        try:
            nuova_promozione = Promozione(
                nome=nome,
                descrizione=descrizione,
                soglia_promozione=soglia,
                sconto_percentuale=sconto,
                data_inizio=data_inizio,
                data_fine=data_fine
            )
            controller.aggiungi_promozione(nuova_promozione)
            QMessageBox.information(self, "Successo", f"Promozione '{nome}' inserita con successo.")
            self.promozione_inserita.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
