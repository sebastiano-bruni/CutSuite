import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator

from controller.ClienteController import ClienteController
from model.Cliente import Cliente


class InserisciCliente(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Inserisci cliente")
        self.resize(500, 600)
        self.controller = ClienteController()
        self.init_ui()

    def init_ui(self):
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Titolo
        title_label = QLabel("CutSuite - Inserisci cliente")
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

        # Form di inserimento
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
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Campi del form
        fields = [
            ("Nome:", "nome", QLineEdit(), "Inserisci il nome"),
            ("Cognome:", "cognome", QLineEdit(), "Inserisci il cognome"),
            ("Email:", "email", QLineEdit(), "Inserisci l'email"),
            ("Telefono:", "telefono", QLineEdit(), "Inserisci il telefono"),
            ("Codice Fiscale:", "codice_fiscale", QLineEdit(), "Inserisci il codice fiscale"),
            ("Numero Appuntamenti:", "numero_appuntamenti", QLineEdit(), "0"),
            ("Stato Fedeltà:", "stato_fedelta", QComboBox(), "")
        ]

        self.input_fields = {}

        for label_text, field_name, input_widget, placeholder in fields:
            # Layout per ogni campo
            field_layout = QVBoxLayout()
            field_layout.setSpacing(5)

            # Label
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; color: #333333; font-size: 14px;")
            field_layout.addWidget(label)

            # Input field
            if isinstance(input_widget, QLineEdit):
                input_widget.setPlaceholderText(placeholder)
                input_widget.setStyleSheet("""
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
                input_widget.setMinimumHeight(40)

                # Validazione specifica per alcuni campi
                if field_name == "telefono":
                    input_widget.setMaxLength(10)
                elif field_name == "codice_fiscale":
                    input_widget.setMaxLength(16)
                elif field_name == "numero_appuntamenti":
                    input_widget.setValidator(QIntValidator(0, 999))

            elif isinstance(input_widget, QComboBox):
                input_widget.addItems(["attivo", "inattivo", "premium"])
                input_widget.setStyleSheet("""
                    QComboBox {
                        padding: 12px;
                        border: 2px solid #dddddd;
                        border-radius: 6px;
                        font-size: 14px;
                        background-color: #fafafa;
                    }
                    QComboBox:focus {
                        border-color: #4a90e2;
                    }
                    QComboBox::drop-down {
                        border: none;
                    }
                """)
                input_widget.setMinimumHeight(40)

            field_layout.addWidget(input_widget)
            form_layout.addLayout(field_layout)

            self.input_fields[field_name] = input_widget

        main_layout.addWidget(form_frame)

        # Pulsante Conferma
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
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        confirm_button.setMinimumHeight(50)
        confirm_button.clicked.connect(self.handle_confirm)

        # Centra il pulsante
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(confirm_button)

        main_layout.addWidget(button_container)
        main_layout.addStretch()

    def handle_confirm(self):
        # Recupera i dati dal form
        client_data = {}
        for field_name, input_widget in self.input_fields.items():
            if isinstance(input_widget, QLineEdit):
                client_data[field_name] = input_widget.text().strip()
            elif isinstance(input_widget, QComboBox):
                client_data[field_name] = input_widget.currentText()

        # Validazione
        errors = self.validate_data(client_data)
        if errors:
            error_message = "Si sono verificati i seguenti errori:\n\n" + "\n".join(errors)
            QMessageBox.critical(self, "Errori di validazione", error_message)
            return

        # Crea l'oggetto Cliente
        nuovo_cliente = Cliente(
            nome=client_data['nome'],
            cognome=client_data['cognome'],
            email=client_data['email'],
            telefono=client_data['telefono'],
            cf=client_data['codice_fiscale'],
            numVisite=int(client_data['numero_appuntamenti']),
            statoFedelta=client_data['stato_fedelta']
        )

        # Chiama il controller per salvare
        self.controller.crea_cliente(nuovo_cliente)

        # Mostra conferma
        QMessageBox.information(
            self,
            "Successo",
            f"Cliente {nuovo_cliente.nome} {nuovo_cliente.cognome} inserito con successo!"
        )

        # Resetta il form
        self.reset_form()

    def validate_data(self, data):
        errors = []

        # Validazione nome
        if not data['nome']:
            errors.append("• Il campo Nome è obbligatorio")
        elif len(data['nome']) < 2:
            errors.append("• Il nome deve essere di almeno 2 caratteri")

        # Validazione cognome
        if not data['cognome']:
            errors.append("• Il campo Cognome è obbligatorio")
        elif len(data['cognome']) < 2:
            errors.append("• Il cognome deve essere di almeno 2 caratteri")

        # Validazione email
        if not data['email']:
            errors.append("• Il campo Email è obbligatorio")
        elif '@' not in data['email'] or '.' not in data['email']:
            errors.append("• Inserisci un'email valida")

        # Validazione telefono
        if not data['telefono']:
            errors.append("• Il campo Telefono è obbligatorio")
        elif len(data['telefono']) != 10 or not data['telefono'].isdigit():
            errors.append("• Il telefono deve essere di 10 cifre")

        # Validazione codice fiscale
        if not data['codice_fiscale']:
            errors.append("• Il campo Codice Fiscale è obbligatorio")
        elif len(data['codice_fiscale']) != 16:
            errors.append("• Il codice fiscale deve essere di 16 caratteri")

        # Validazione numero appuntamenti
        if not data['numero_appuntamenti']:
            data['numero_appuntamenti'] = '0'
        elif not data['numero_appuntamenti'].isdigit():
            errors.append("• Il numero di appuntamenti deve essere un numero")

        return errors

    def reset_form(self):
        # Resetta tutti i campi
        for field_name, input_widget in self.input_fields.items():
            if isinstance(input_widget, QLineEdit):
                input_widget.clear()
            elif isinstance(input_widget, QComboBox):
                input_widget.setCurrentIndex(0)

        # Rimuovi eventuali messaggi di errore
        for input_widget in self.input_fields.values():
            input_widget.setStyleSheet("""
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
                QComboBox {
                    padding: 12px;
                    border: 2px solid #dddddd;
                    border-radius: 6px;
                    font-size: 14px;
                    background-color: #fafafa;
                }
                QComboBox:focus {
                    border-color: #4a90e2;
                }
            """)


