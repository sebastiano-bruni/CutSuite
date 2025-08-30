import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QComboBox,
    QDateEdit, QTimeEdit, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QTime
from PyQt6.QtGui import QFont

from controller.PrenotazioneController import PrenotazioneController
from controller.ClienteController import ClienteController
from controller.ServizioController import ServizioController
from controller.DipendenteController import DipendenteController
from model.Prenotazione import Prenotazione
from datetime import datetime


class ModificaPrenotazione(QMainWindow):
    prenotazione_modificata = pyqtSignal()

    def __init__(self, prenotazione):
        super().__init__()
        self.prenotazione = prenotazione
        self.setWindowTitle("CutSuite - Modifica prenotazione")
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

        title_label = QLabel("CutSuite - Modifica prenotazione")
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

        # Campi di input pre-popolati
        self.cliente_combo = self.create_cliente_combo("Cliente:", self.prenotazione.cliente)
        self.servizio_combo = self.create_servizio_combo("Servizio:", self.prenotazione.servizio)
        self.dipendente_combo = self.create_dipendente_combo("Dipendente:", self.prenotazione.dipendente)
        self.data_input = self.create_date_input("Data:", self.prenotazione.data.date())
        self.ora_input = self.create_time_input("Ora:", self.prenotazione.ora.time())
        self.note_input = self.create_textedit("Note:", self.prenotazione.note)

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

    def create_cliente_combo(self, label_text, selected_cliente):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")

        combo_box = QComboBox()
        clienti = self.cliente_controller.get_tutti_clienti()
        for i, c in enumerate(clienti):
            combo_box.addItem(f"{c.nome} {c.cognome}", c)
            if c.id == selected_cliente.id:
                combo_box.setCurrentIndex(i)

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

    def create_servizio_combo(self, label_text, selected_servizio):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")

        combo_box = QComboBox()
        servizi = self.servizio_controller.get_tutti_servizi()
        for i, s in enumerate(servizi):
            combo_box.addItem(f"{s.nome} ({s.prezzo} €)", s)
            if s.id == selected_servizio.id:
                combo_box.setCurrentIndex(i)

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

    def create_dipendente_combo(self, label_text, selected_dipendente):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")

        combo_box = QComboBox()
        dipendenti = self.dipendente_controller.get_tutti_dipendenti()
        for i, d in enumerate(dipendenti):
            combo_box.addItem(f"{d.nome} {d.cognome} ({d.ruolo})", d)
            if d.id == selected_dipendente.id:
                combo_box.setCurrentIndex(i)

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

    def create_date_input(self, label_text, selected_date):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate(selected_date))
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

    def create_time_input(self, label_text, selected_time):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        time_edit = QTimeEdit()
        time_edit.setMinimumTime(QTime(9, 0))
        time_edit.setMaximumTime(QTime(19, 0))
        time_edit.setTime(QTime(selected_time))
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

    def create_textedit(self, label_text, value=""):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        text_edit = QTextEdit(value)
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

    def handle_confirm(self):
        cliente = self.input_fields['cliente'].currentData()
        servizio = self.input_fields['servizio'].currentData()
        dipendente = self.input_fields['dipendente'].currentData()
        data_qdate = self.input_fields['data'].date()
        ora_qtime = self.input_fields['ora'].time()
        note = self.input_fields['note'].toPlainText().strip()

        if not cliente or not servizio or not dipendente:
            QMessageBox.critical(self, "Errore", "Seleziona cliente, servizio e dipendente.")
            return

        data_obj = datetime(data_qdate.year(), data_qdate.month(), data_qdate.day())
        ora_obj = datetime(data_qdate.year(), data_qdate.month(), data_qdate.day(),
                           ora_qtime.hour(), ora_qtime.minute())

        modified_data = {
            "cliente": cliente,
            "servizio": servizio,
            "dipendente": dipendente,
            "data": data_obj,
            "ora": ora_obj,
            "durata_minuti": servizio.durata_minuti,
            "prezzo": servizio.prezzo,
            "stato": self.prenotazione.stato,
            "email_cliente": cliente.email,
            "note": note
        }

        try:
            self.prenotazione_controller.aggiorna_prenotazione(self.prenotazione.id, **modified_data)
            QMessageBox.information(self, "Successo", "Prenotazione modificata con successo.")
            self.prenotazione_modificata.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
