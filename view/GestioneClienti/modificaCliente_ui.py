import re
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIntValidator

from controller.ClienteController import ClienteController


class ModificaCliente(QMainWindow):
    cliente_modificato = pyqtSignal()

    def __init__(self, cliente):
        super().__init__()
        self.cliente = cliente
        self.setWindowTitle("CutSuite - Modifica cliente")
        self.resize(500, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Modifica cliente")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                padding: 10px 0;
                text-align: center;
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

        fields = [
            ("Nome:", "nome", self.cliente.nome),
            ("Cognome:", "cognome", self.cliente.cognome),
            ("Email:", "email", self.cliente.email),
            ("Telefono:", "telefono", self.cliente.telefono),
            ("Codice Fiscale:", "codice_fiscale", self.cliente.cf),
            ("Numero Appuntamenti:", "numero_appuntamenti", str(self.cliente.numVisite))
        ]

        self.input_fields = {}

        for label_text, field_name, current_value in fields:
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)

            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; color: #333333; font-size: 14px;")
            field_layout.addWidget(label)

            input_field = QLineEdit(current_value)
            input_field.setStyleSheet("""
                QLineEdit {
                    padding: 12px;
                    border: 2px solid #dddddd;
                    border-radius: 6px;
                    font-size: 14px;
                    background-color: #fafafa;
                }
                QLineEdit:focus {
                    border-color: #4a90e2;
                    background-color: white;
                }
            """)
            input_field.setMinimumHeight(40)

            if field_name == "telefono":
                input_field.setInputMask("9999999999")
            elif field_name == "codice_fiscale":
                input_field.setMaxLength(16)
            elif field_name == "numero_appuntamenti":
                input_field.setValidator(QIntValidator(0, 999))

            field_layout.addWidget(input_field)
            form_layout.addLayout(field_layout)
            self.input_fields[field_name] = input_field

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

    def handle_confirm(self):
        modified_data = {}
        for field_name, input_field in self.input_fields.items():
            modified_data[field_name] = input_field.text().strip()

        errors = self.validate_data(modified_data)
        if errors:
            error_message = "Si sono verificati i seguenti errori:\n\n" + "\n".join(errors)
            QMessageBox.critical(self, "Errori di validazione", error_message)
            return

        controller = ClienteController()
        try:
            # Rimosso statoFedelta dalla chiamata
            success = controller.aggiorna_cliente(
                id=self.cliente.id,
                nome=modified_data['nome'],
                cognome=modified_data['cognome'],
                email=modified_data['email'],
                telefono=modified_data['telefono'],
                cf=modified_data['codice_fiscale'],
                numVisite=int(modified_data['numero_appuntamenti'])
            )

            if success:
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Cliente {modified_data['nome']} {modified_data['cognome']} modificato con successo!"
                )
                print("Segnale modifica emesso!")
                self.cliente_modificato.emit()
                self.close()
            else:
                QMessageBox.critical(
                    self,
                    "Errore",
                    "Errore durante l'aggiornamento del cliente."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Errore",
                f"Si è verificato un errore: {str(e)}"
            )

    def validate_data(self, data):
        errors = []
        # Definiamo il pattern per una email valida
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not (data['nome'] and len(data['nome']) >= 2):
            errors.append("• Il nome deve contenere almeno 2 caratteri.")

        if not (data['cognome'] and len(data['cognome']) >= 2):
            errors.append("• Il cognome deve contenere almeno 2 caratteri.")

        if not (data['email'] and re.match(email_regex, data['email'])):
            errors.append("• L'indirizzo email non ha un formato valido.")

        if not (data['telefono'] and len(data['telefono']) == 10 and data['telefono'].isdigit()):
            errors.append("• Il numero di telefono deve essere di 10 cifre.")

        if not (data['codice_fiscale'] and len(data['codice_fiscale']) == 16):
            errors.append("• Il codice fiscale deve essere di 16 caratteri.")

        if not data['numero_appuntamenti'].isdigit():
            errors.append("• Il numero di appuntamenti deve essere un numero.")

        return errors

