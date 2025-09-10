import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QSpinBox,
    QDoubleSpinBox, QTextEdit, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QDoubleValidator

from controller.ServizioController import ServizioController
from controller.MaterialeController import MaterialeController
from model.Servizio import Servizio
from model.Materiale import Materiale


class InserisciServizio(QMainWindow):
    servizio_inserito = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Inserisci servizio")
        self.resize(500, 600)
        self.servizio_controller = ServizioController()
        self.materiale_controller = MaterialeController()
        self.materiali_disponibili = self.materiale_controller.get_tutti_materiali()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Inserisci servizio")
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

        self.nome_input = self.create_input("Nome:", placeholder="Inserisci nome del servizio")
        self.durata_spinbox = self.create_spinbox("Durata (minuti):", min_val=5, max_val=240, step=5)
        self.prezzo_doublespinbox = self.create_doublespinbox("Prezzo:", min_val=0.00, max_val=1000.00, step=0.50)
        self.descrizione_input = self.create_textedit("Descrizione:", placeholder="Inserisci una descrizione")
        self.materiale_combo = self.create_material_combo("Materiale necessario:")
        self.quantita_materiale_spinbox = self.create_spinbox("Quantità materiale:", min_val=0, max_val=100)

        form_layout.addLayout(self.nome_input)
        form_layout.addLayout(self.durata_spinbox)
        form_layout.addLayout(self.prezzo_doublespinbox)
        form_layout.addLayout(self.descrizione_input)
        form_layout.addLayout(self.materiale_combo)
        form_layout.addLayout(self.quantita_materiale_spinbox)

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

    def create_doublespinbox(self, label_text, value=0.00, min_val=0.00, max_val=1000.00, step=0.50):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        doublespinbox = QDoubleSpinBox()
        doublespinbox.setRange(min_val, max_val)
        doublespinbox.setValue(value)
        doublespinbox.setSingleStep(step)
        doublespinbox.setDecimals(2)
        doublespinbox.setStyleSheet("""
            QDoubleSpinBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        doublespinbox.setMinimumHeight(35)
        v_layout.addWidget(label)
        v_layout.addWidget(doublespinbox)
        self.input_fields[label_text.replace(":", "").strip().lower()] = doublespinbox
        return v_layout

    def create_spinbox(self, label_text, value=0, min_val=0, max_val=10000, step=1):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(value)
        spinbox.setSingleStep(step)
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

    def create_material_combo(self, label_text):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")

        combo_box = QComboBox()
        combo_box.addItem("Nessun materiale")
        for mat in self.materiali_disponibili:
            combo_box.addItem(mat.nome, mat)

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
        self.input_fields[label_text.replace(":", "").strip().lower()] = combo_box
        return v_layout

    def validate_data(self, nome, descrizione, prezzo, durata):
        errors = []
        if not nome or len(nome) < 3:
            errors.append("• Il nome del servizio deve contenere almeno 3 caratteri.")
        if not descrizione:
            errors.append("• La descrizione non può essere vuota.")
        if prezzo <= 0:
            errors.append("• Il prezzo deve essere maggiore di zero.")
        if durata <= 0:
            errors.append("• La durata deve essere maggiore di zero.")
        return errors

    def handle_confirm(self):
        nome = self.input_fields['nome'].text().strip()
        durata_minuti = self.input_fields['durata (minuti)'].value()
        prezzo = self.input_fields['prezzo'].value()
        descrizione = self.input_fields['descrizione'].toPlainText().strip()

        selected_material_combo = self.input_fields['materiale necessario']
        selected_material = selected_material_combo.currentData()
        quantita_materiale = self.input_fields['quantità materiale'].value()

        errors = self.validate_data(nome, descrizione, prezzo, durata_minuti)
        if errors:
            error_message = "Si sono verificati i seguenti errori:\n\n" + "\n".join(errors)
            QMessageBox.critical(self, "Errori di validazione", error_message)
            return

        try:
            nuovo_servizio = Servizio(
                nome=nome,
                durata_minuti=durata_minuti,
                prezzo=prezzo,
                descrizione=descrizione,
                materiale=selected_material,
                quantita_materiale=quantita_materiale
            )
            self.servizio_controller.aggiungi_servizio(nuovo_servizio)
            QMessageBox.information(self, "Successo", f"Servizio '{nome}' inserito con successo.")
            self.servizio_inserito.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
