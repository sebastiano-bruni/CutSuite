import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator

from controller.ClienteController import ClienteController


class InserisciCliente(QMainWindow):
    cliente_inserito = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Inserisci cliente")
        self.resize(500, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Inserisci cliente")
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

        fields = [
            ("Nome:", "nome", ""),
            ("Cognome:", "cognome", ""),
            ("Email:", "email", ""),
            ("Telefono:", "telefono", ""),
            ("Codice Fiscale:", "cf", ""),
        ]

        self.input_fields = {}

        for label_text, field_name, default_value in fields:
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)

            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; color: #333333; font-size: 14px;")
            field_layout.addWidget(label)

            input_field = QLineEdit(default_value)
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
            elif field_name == "cf":
                input_field.setMaxLength(16)

            field_layout.addWidget(input_field)
            form_layout.addLayout(field_layout)
            self.input_fields[field_name] = input_field

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #cccccc; margin: 10px 0;")
        form_layout.addWidget(separator)

        main_layout.addWidget(form_frame)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        confirm_button = QPushButton("Inserisci")
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        confirm_button.setMinimumHeight(50)
        confirm_button.clicked.connect(self.handle_confirm)

        button_layout.addWidget(confirm_button)
        main_layout.addWidget(button_container)
        main_layout.addStretch()

    def handle_confirm(self):
        nome = self.input_fields['nome'].text().strip()
        cognome = self.input_fields['cognome'].text().strip()
        email = self.input_fields['email'].text().strip()
        telefono = self.input_fields['telefono'].text().strip()
        cf = self.input_fields['cf'].text().strip()

        errors = self.validate_data(nome, cognome, email, telefono, cf)
        if errors:
            error_message = "Si sono verificati i seguenti errori:\n\n" + "\n".join(errors)
            QMessageBox.critical(self, "Errori di validazione", error_message)
            return

        controller = ClienteController()
        try:
            nuovo_cliente = controller.aggiungi_cliente(nome, cognome, email, telefono, cf)
            if nuovo_cliente:
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Cliente {nuovo_cliente.nome} {nuovo_cliente.cognome} inserito con successo!"
                )
                self.cliente_inserito.emit()
                self.close()
            else:
                QMessageBox.critical(
                    self,
                    "Errore",
                    "Impossibile inserire il cliente."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Errore",
                f"Si è verificato un errore: {str(e)}"
            )

    def validate_data(self, nome, cognome, email, telefono, cf):
        errors = []
        if not nome:
            errors.append("• Il campo Nome è obbligatorio.")
        elif len(nome) < 2:
            errors.append("• Il nome deve essere di almeno 2 caratteri.")
        if not cognome:
            errors.append("• Il campo Cognome è obbligatorio.")
        elif len(cognome) < 2:
            errors.append("• Il cognome deve essere di almeno 2 caratteri.")
        if not email:
            errors.append("• Il campo Email è obbligatorio.")
        elif '@' not in email or '.' not in email:
            errors.append("• Inserisci un'email valida.")
        if not telefono:
            errors.append("• Il campo Telefono è obbligatorio.")
        elif len(telefono) != 10 or not telefono.isdigit():
            errors.append("• Il telefono deve essere di 10 cifre.")
        if not cf:
            errors.append("• Il campo Codice Fiscale è obbligatorio.")
        elif len(cf) != 16:
            errors.append("• Il codice fiscale deve essere di 16 caratteri.")
        return errors