import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class DettagliCliente(QMainWindow):
    def __init__(self, client_id=1):
        super().__init__()
        self.client_id = client_id
        self.setWindowTitle("CutSuite - Dettagli cliente")
        self.resize(600, 600)

        # Dati del cliente (esempio)
        self.client_data = {
            "id": 1,
            "nome": "Martina",
            "cognome": "Rossi",
            "email": "martina.rossi@gmail.com",
            "telefono": "3456789123",
            "codice_fiscale": "RSSMRT95A41H501K",
            "numero_appuntamenti": 5,
            "stato_fedelta": "attivo"
        }

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
        title_label = QLabel("CutSuite - Dettagli cliente")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                padding: 10px 0;
            }
        """)
        main_layout.addWidget(title_label)

        # Tabella dettagli cliente
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

        # Intestazioni e dati
        headers = ["ID", "Nome", "Cognome", "Email", "Telefono",
                   "Codice Fiscale", "Numero Appuntamenti", "Stato Fedeltà"]

        values = [
            str(self.client_data["id"]),
            self.client_data["nome"],
            self.client_data["cognome"],
            self.client_data["email"],
            self.client_data["telefono"],
            self.client_data["codice_fiscale"],
            str(self.client_data["numero_appuntamenti"]),
            self.client_data["stato_fedelta"]
        ]

        # Crea le righe della tabella
        for i, (header, value) in enumerate(zip(headers, values)):
            # Intestazione
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

            # Valore
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

        # Imposta il rapporto delle colonne
        details_layout.setColumnStretch(0, 1)
        details_layout.setColumnStretch(1, 2)

        main_layout.addWidget(details_frame)

        # Separatore
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #cccccc; margin: 10px 0;")
        main_layout.addWidget(separator)

        # Sezione modifica
        edit_section_label = QLabel("Modifica cliente")
        edit_section_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333333;
                padding: 5px 0;
            }
        """)
        main_layout.addWidget(edit_section_label)

        # Form modifica
        edit_frame = QFrame()
        edit_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
            }
        """)

        edit_layout = QGridLayout(edit_frame)
        edit_layout.setSpacing(15)
        edit_layout.setContentsMargins(15, 15, 15, 15)

        # Campi di modifica
        fields = [
            ("Nome:", "nome", self.client_data["nome"]),
            ("Cognome:", "cognome", self.client_data["cognome"]),
            ("Email:", "email", self.client_data["email"]),
            ("Telefono:", "telefono", self.client_data["telefono"]),
            ("Codice Fiscale:", "codice_fiscale", self.client_data["codice_fiscale"])
        ]

        self.edit_inputs = {}

        for i, (label_text, field_name, current_value) in enumerate(fields):
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold;")

            input_field = QLineEdit(current_value)
            input_field.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    background-color: white;
                }
                QLineEdit:focus {
                    border-color: #4a90e2;
                }
            """)
            input_field.setMinimumHeight(35)

            self.edit_inputs[field_name] = input_field

            edit_layout.addWidget(label, i, 0)
            edit_layout.addWidget(input_field, i, 1)

        # Pulsanti modifica
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton("Salva Modifiche")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        save_button.clicked.connect(self.handle_save)

        cancel_button = QPushButton("Annulla")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        cancel_button.clicked.connect(self.handle_cancel)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        edit_layout.addLayout(button_layout, len(fields), 0, 1, 2)

        main_layout.addWidget(edit_frame)

        # Pulsante Elimina cliente
        delete_button = QPushButton("Elimina cliente")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: bold;
                margin: 10px 0;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        delete_button.clicked.connect(self.handle_delete)

        # Centra il pulsante di eliminazione
        delete_container = QWidget()
        delete_layout = QHBoxLayout(delete_container)
        delete_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        delete_layout.addWidget(delete_button)

        main_layout.addWidget(delete_container)

    def handle_save(self):
        # Recupera i dati modificati
        modified_data = {}
        for field_name, input_field in self.edit_inputs.items():
            modified_data[field_name] = input_field.text().strip()

        # Validazione base
        if not all(modified_data.values()):
            QMessageBox.warning(self, "Errore", "Tutti i campi sono obbligatori!")
            return

        # Qui implementerai il salvataggio nel database
        print("Dati modificati:", modified_data)
        QMessageBox.information(self, "Successo", "Modifiche salvate con successo!")

        # Aggiorna i dati locali
        self.client_data.update(modified_data)
        self.update_display()

    def handle_cancel(self):
        # Ripristina i valori originali
        for field_name, input_field in self.edit_inputs.items():
            input_field.setText(self.client_data[field_name])

        print("Modifiche annullate")

    def handle_delete(self):
        # Conferma eliminazione
        reply = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare il cliente {self.client_data['nome']} {self.client_data['cognome']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Qui implementerai l'eliminazione dal database
            print(f"Cliente {self.client_data['id']} eliminato")
            QMessageBox.information(self, "Successo", "Cliente eliminato con successo!")
            self.close()

    def update_display(self):
        # Qui implementerai l'aggiornamento della visualizzazione
        # dopo le modifiche (se necessario)
        print("Display aggiornato con i nuovi dati")
