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

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #cccccc; margin: 10px 0;")
        form_layout.addWidget(separator)

        stato_fedelta_layout = QVBoxLayout()
        stato_fedelta_layout.setSpacing(5)

        stato_label = QLabel("Stato Fedeltà:")
        stato_label.setStyleSheet("font-weight: bold; color: #333333; font-size: 14px;")
        stato_fedelta_layout.addWidget(stato_label)

        self.stato_fedelta_combo = QComboBox()
        self.stato_fedelta_combo.addItems(["Attivo", "Inattivo", "Premium", "VIP", "Standard"])

        current_text = self.cliente.statoFedelta
        if current_text:
            for i in range(self.stato_fedelta_combo.count()):
                if self.stato_fedelta_combo.itemText(i).lower() == current_text.lower():
                    self.stato_fedelta_combo.setCurrentIndex(i)
                    break
            else:
                self.stato_fedelta_combo.addItem(current_text)
                self.stato_fedelta_combo.setCurrentText(current_text)

        self.stato_fedelta_combo.setStyleSheet("""
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
        self.stato_fedelta_combo.setMinimumHeight(40)
        stato_fedelta_layout.addWidget(self.stato_fedelta_combo)
        form_layout.addLayout(stato_fedelta_layout)
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

        modified_data["statoFedelta"] = self.stato_fedelta_combo.currentText()

        errors = self.validate_data(modified_data)
        if errors:
            error_message = "Si sono verificati i seguenti errori:\n\n" + "\n".join(errors)
            QMessageBox.critical(self, "Errori di validazione", error_message)
            return

        controller = ClienteController()
        try:
            success = controller.aggiorna_cliente(
                id=self.cliente.id,
                nome=modified_data['nome'],
                cognome=modified_data['cognome'],
                email=modified_data['email'],
                telefono=modified_data['telefono'],
                cf=modified_data['codice_fiscale'],
                numVisite=int(modified_data['numero_appuntamenti']),
                statoFedelta=modified_data['statoFedelta']
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
        if not data['nome']:
            errors.append("• Il campo Nome è obbligatorio")
        elif len(data['nome']) < 2:
            errors.append("• Il nome deve essere di almeno 2 caratteri")
        if not data['cognome']:
            errors.append("• Il campo Cognome è obbligatorio")
        elif len(data['cognome']) < 2:
            errors.append("• Il cognome deve essere di almeno 2 caratteri")
        if not data['email']:
            errors.append("• Il campo Email è obbligatorio")
        elif '@' not in data['email'] or '.' not in data['email']:
            errors.append("• Inserisci un'email valida")
        if not data['telefono']:
            errors.append("• Il campo Telefono è obbligatorio")
        elif len(data['telefono']) != 10 or not data['telefono'].isdigit():
            errors.append("• Il telefono deve essere di 10 cifre")
        if not data['codice_fiscale']:
            errors.append("• Il campo Codice Fiscale è obbligatorio")
        elif len(data['codice_fiscale']) != 16:
            errors.append("• Il codice fiscale deve essere di 16 caratteri")
        if not data['numero_appuntamenti']:
            errors.append("• Il campo Numero Appuntamenti è obbligatorio")
        elif not data['numero_appuntamenti'].isdigit():
            errors.append("• Il numero di appuntamenti deve essere un numero")
        if not data.get('statoFedelta'):
            errors.append("• Il campo Stato Fedeltà è obbligatorio")
        return errors