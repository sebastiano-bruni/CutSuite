import re
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QMessageBox,
    QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from controller.DipendenteController import DipendenteController
from model.Dipendente import Proprietario, Parrucchiere


class ModificaDipendente(QMainWindow):
    dipendente_modificato = pyqtSignal()

    def __init__(self, dipendente):
        super().__init__()
        self.dipendente = dipendente
        self.setWindowTitle("CutSuite - Modifica dipendente")
        self.resize(500, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("CutSuite - Modifica dipendente")
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
        form_layout.setSpacing(5)
        form_layout.setContentsMargins(10, 10, 10, 10)

        fields_data = [
            ("Nome:", "nome", self.dipendente.nome, QLineEdit()),
            ("Cognome:", "cognome", self.dipendente.cognome, QLineEdit()),
            ("Email:", "email", self.dipendente.email, QLineEdit()),
            ("Telefono:", "telefono", self.dipendente.telefono, QLineEdit()),
            ("Codice Fiscale:", "cf", getattr(self.dipendente, 'cf', ''), QLineEdit()),
            ("Ruolo:", "ruolo", getattr(self.dipendente, 'ruolo', 'Proprietario'), QLineEdit()),
            ("Stipendio:", "stipendio", str(getattr(self.dipendente, 'stipendio', 0)), QSpinBox()),
            ("Username:", "username", self.dipendente.username, QLineEdit()),
            ("Password:", "password", self.dipendente.password, QLineEdit()),
        ]

        self.input_fields = {}

        for label_text, field_name, current_value, widget in fields_data:
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)

            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
            field_layout.addWidget(label)

            if isinstance(widget, QLineEdit):
                widget.setText(current_value)
                widget.setStyleSheet("""
                    QLineEdit {
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }
                """)
                if field_name == "password":
                    widget.setEchoMode(QLineEdit.EchoMode.Password)
            elif isinstance(widget, QSpinBox):
                widget.setRange(0, 100000)
                widget.setValue(int(current_value) if str(current_value).isdigit() else 0)
                widget.setStyleSheet("""
                    QSpinBox {
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }
                """)

            # Nascondi campo stipendio per Proprietario
            if field_name == "stipendio" and getattr(self.dipendente, 'ruolo', 'Proprietario') == 'Proprietario':
                label.hide()
                widget.hide()

            field_layout.addWidget(widget)
            form_layout.addLayout(field_layout)
            self.input_fields[field_name] = widget

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

    def validate_data(self, data):
        errors = []
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not (data['nome'] and len(data['nome']) >= 2):
            errors.append("• Il nome deve contenere almeno 2 caratteri.")
        if not (data['cognome'] and len(data['cognome']) >= 2):
            errors.append("• Il cognome deve contenere almeno 2 caratteri.")
        if not (data['cf'] and len(data['cf']) == 16):
            errors.append("• Il codice fiscale deve essere di 16 caratteri.")
        if not (data['email'] and re.match(email_regex, data['email'])):
            errors.append("• L'indirizzo email non ha un formato valido (es. nome@dominio.com).")
        if not (data['telefono'] and len(data['telefono']) == 10 and data['telefono'].isdigit()):
            errors.append("• Il numero di telefono deve essere di 10 cifre.")
        if not (data['username'] and len(data['username']) >= 3):
            errors.append("• L'username deve contenere almeno 3 caratteri.")
        if not (data['password'] and len(data['password']) >= 4):
            errors.append("• La password deve contenere almeno 4 caratteri.")
        if data['ruolo'] == "Parrucchiere" and data['stipendio'] <= 0:
            errors.append("• Lo stipendio per un parrucchiere deve essere maggiore di zero.")

        return errors

    def handle_confirm(self):
        modified_data = {}
        modified_data['nome'] = self.input_fields['nome'].text()
        modified_data['cognome'] = self.input_fields['cognome'].text()
        modified_data['email'] = self.input_fields['email'].text()
        modified_data['telefono'] = self.input_fields['telefono'].text()
        modified_data['cf'] = self.input_fields['cf'].text()
        modified_data['ruolo'] = self.input_fields['ruolo'].text()
        modified_data['stipendio'] = self.input_fields['stipendio'].value()
        modified_data['username'] = self.input_fields['username'].text()
        modified_data['password'] = self.input_fields['password'].text()

        errors = self.validate_data(modified_data)
        if errors:
            error_message = "Si sono verificati i seguenti errori:\n\n" + "\n".join(errors)
            QMessageBox.critical(self, "Errori di validazione", error_message)
            return

        controller = DipendenteController()

        try:
            success = controller.aggiorna_dipendente(self.dipendente.id, **modified_data)
            if success:
                QMessageBox.information(self, "Successo", "Dipendente modificato con successo.")
                self.dipendente_modificato.emit()
                self.close()
            else:
                QMessageBox.critical(self, "Errore", "Impossibile aggiornare il dipendente.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
