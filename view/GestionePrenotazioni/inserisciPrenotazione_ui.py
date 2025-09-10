import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QSpinBox,
    QDoubleSpinBox, QTextEdit, QComboBox, QDateEdit, QTimeEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt6.QtGui import QFont

from controller.PrenotazioneController import PrenotazioneController
from controller.ClienteController import ClienteController
from controller.ServizioController import ServizioController
from controller.DipendenteController import DipendenteController
from model.Prenotazione import Prenotazione
from datetime import datetime


class InserisciPrenotazione(QMainWindow):
    prenotazione_inserita = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Inserisci prenotazione")
        self.resize(500, 700)

        self.prenotazione_controller = PrenotazioneController()
        self.cliente_controller = ClienteController()
        self.servizio_controller = ServizioController()
        self.dipendente_controller = DipendenteController()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Inserisci prenotazione")
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

        # Campi di input
        self.cliente_combo = self.create_cliente_combo("Cliente:")
        self.servizio_combo = self.create_servizio_combo("Servizio:")
        self.dipendente_combo = self.create_dipendente_combo("Dipendente:")
        self.data_input = self.create_date_input("Data:")
        self.ora_input = self.create_time_input("Ora:")
        self.note_input = self.create_textedit("Note:")

        form_layout.addLayout(self.cliente_combo)
        form_layout.addLayout(self.servizio_combo)
        form_layout.addLayout(self.dipendente_combo)
        form_layout.addLayout(self.data_input)
        form_layout.addLayout(self.ora_input)
        form_layout.addLayout(self.note_input)

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

    def create_cliente_combo(self, label_text):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")

        combo_box = QComboBox()
        combo_box.addItem("Seleziona cliente", None)
        clienti = self.cliente_controller.get_tutti_clienti()
        for c in clienti:
            combo_box.addItem(f"{c.nome} {c.cognome}", c)

        combo_box.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        combo_box.setMinimumHeight(35)
        v_layout.addWidget(label)
        v_layout.addWidget(combo_box)
        self.input_fields['cliente'] = combo_box
        return v_layout

    def create_servizio_combo(self, label_text):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")

        combo_box = QComboBox()
        combo_box.addItem("Seleziona servizio", None)
        servizi = self.servizio_controller.get_tutti_servizi()
        for s in servizi:
            combo_box.addItem(f"{s.nome} ({s.prezzo} €)", s)

        combo_box.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        combo_box.setMinimumHeight(35)
        v_layout.addWidget(label)
        v_layout.addWidget(combo_box)
        self.input_fields['servizio'] = combo_box
        return v_layout

    def create_dipendente_combo(self, label_text):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")

        combo_box = QComboBox()
        combo_box.addItem("Seleziona dipendente", None)
        dipendenti = self.dipendente_controller.get_tutti_dipendenti()
        for d in dipendenti:
            combo_box.addItem(f"{d.nome} {d.cognome} ({d.ruolo})", d)

        combo_box.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        combo_box.setMinimumHeight(35)
        v_layout.addWidget(label)
        v_layout.addWidget(combo_box)
        self.input_fields['dipendente'] = combo_box
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
        self.input_fields['data'] = date_edit
        return v_layout

    def create_time_input(self, label_text):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        time_edit = QTimeEdit()
        time_edit.setMinimumTime(QTime(9, 0))
        time_edit.setMaximumTime(QTime(19, 0))
        time_edit.setTime(QTime(9, 0))
        time_edit.setStyleSheet("""
            QTimeEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        time_edit.setMinimumHeight(35)
        v_layout.addWidget(label)
        v_layout.addWidget(time_edit)
        self.input_fields['ora'] = time_edit
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
        self.input_fields['note'] = text_edit
        return v_layout

    def validate_data(self, cliente, servizio, dipendente, data_qdate):
        errors = []
        today = QDate.currentDate()

        if cliente is None:
            errors.append("• Devi selezionare un cliente.")
        if servizio is None:
            errors.append("• Devi selezionare un servizio.")
        if dipendente is None:
            errors.append("• Devi selezionare un dipendente.")

        if data_qdate < today:
            errors.append("• La data della prenotazione non può essere nel passato.")

        return errors

    def handle_confirm(self):
        cliente = self.input_fields['cliente'].currentData()
        servizio = self.input_fields['servizio'].currentData()
        dipendente = self.input_fields['dipendente'].currentData()
        data_qdate = self.input_fields['data'].date()
        ora_qtime = self.input_fields['ora'].time()
        note = self.input_fields['note'].toPlainText().strip()

        errors = self.validate_data(cliente, servizio, dipendente, data_qdate)
        if errors:
            error_message = "Si sono verificati i seguenti errori:\n\n" + "\n".join(errors)
            QMessageBox.critical(self, "Errori di validazione", error_message)
            return

        # Converti QDate e QTime in oggetti datetime
        data = datetime(data_qdate.year(), data_qdate.month(), data_qdate.day())
        ora = datetime(data_qdate.year(), data_qdate.month(), data_qdate.day(),
                       ora_qtime.hour(), ora_qtime.minute())

        try:
            nuova_prenotazione = Prenotazione(
                cliente=cliente,
                servizio=servizio,
                dipendente=dipendente,
                data=data,
                ora=ora,
                durata_minuti=servizio.durata_minuti,
                prezzo=servizio.prezzo,
                email_cliente=cliente.email,
                note=note
            )
            self.prenotazione_controller.aggiungi_prenotazione(nuova_prenotazione)
            QMessageBox.information(
                self,
                "Successo",
                f"Prenotazione inserita per {cliente.nome} {cliente.cognome} il {data.strftime('%d/%m/%Y')}."
            )
            self.prenotazione_inserita.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
