import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QComboBox,
    QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIntValidator

from controller.DipendenteController import DipendenteController
from model.Dipendente import Parrucchiere, Proprietario, Dipendente


class InserisciDipendente(QMainWindow):
    dipendente_inserito = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Inserisci dipendente")
        self.resize(500, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Inserisci dipendente")
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

        # Campi per l'inserimento
        input_fields_data = [
            ("Nome:", "nome"),
            ("Cognome:", "cognome"),
            ("Codice Fiscale:", "cf"),
            ("Email:", "email"),
            ("Telefono:", "telefono"),
            ("Username:", "username"),
            ("Password:", "password"),
        ]

        for label_text, field_name in input_fields_data:
            field_layout = QVBoxLayout()
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
            field_layout.addWidget(label)

            input_widget = QLineEdit()
            input_widget.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)
            if field_name == "password":
                input_widget.setEchoMode(QLineEdit.EchoMode.Password)
            elif field_name == "cf":
                input_widget.setMaxLength(16)

            field_layout.addWidget(input_widget)
            form_layout.addLayout(field_layout)
            self.input_fields[field_name] = input_widget

        # Campo per il ruolo
        self.ruolo_combo = QComboBox()
        self.ruolo_combo.addItems(["Parrucchiere", "Proprietario"])
        self.ruolo_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        ruolo_label = QLabel("Ruolo:")
        ruolo_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        ruolo_layout = QVBoxLayout()
        ruolo_layout.addWidget(ruolo_label)
        ruolo_layout.addWidget(self.ruolo_combo)
        form_layout.addLayout(ruolo_layout)

        # Campo Stipendio (visibile solo per Parrucchiere)
        self.stipendio_layout = QVBoxLayout()
        stipendio_label = QLabel("Stipendio:")
        stipendio_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.stipendio_spinbox = QSpinBox()
        self.stipendio_spinbox.setRange(0, 10000)
        self.stipendio_spinbox.setStyleSheet("""
            QSpinBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        self.stipendio_layout.addWidget(stipendio_label)
        self.stipendio_layout.addWidget(self.stipendio_spinbox)
        form_layout.addLayout(self.stipendio_layout)

        self.ruolo_combo.currentTextChanged.connect(self.toggle_stipendio)
        self.toggle_stipendio(self.ruolo_combo.currentText())

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

    def toggle_stipendio(self, role):
        is_parrucchiere = (role == "Parrucchiere")
        self.stipendio_layout.itemAt(0).widget().setVisible(is_parrucchiere)
        self.stipendio_layout.itemAt(1).widget().setVisible(is_parrucchiere)

    def handle_confirm(self):
        nome = self.input_fields['nome'].text().strip()
        cognome = self.input_fields['cognome'].text().strip()
        cf = self.input_fields['cf'].text().strip()  # Raccogli il valore del codice fiscale
        email = self.input_fields['email'].text().strip()
        telefono = self.input_fields['telefono'].text().strip()
        username = self.input_fields['username'].text().strip()
        password = self.input_fields['password'].text().strip()
        ruolo = self.ruolo_combo.currentText()
        stipendio = self.stipendio_spinbox.value()

        controller = DipendenteController()

        try:
            if ruolo == "Parrucchiere":
                nuovo_dipendente = Parrucchiere(nome=nome, cognome=cognome, cf=cf, email=email, telefono=telefono,
                                                username=username, password=password, stipendio=stipendio)
            else:  # Proprietario
                nuovo_dipendente = Proprietario(nome=nome, cognome=cognome, cf=cf, email=email, telefono=telefono,
                                                username=username, password=password, permessi=1)

            controller.aggiungi_dipendente(nuovo_dipendente)
            QMessageBox.information(self, "Successo",
                                    f"Dipendente {nuovo_dipendente.nome} {nuovo_dipendente.cognome} inserito con successo.")
            self.dipendente_inserito.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
