import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QSpinBox,
    QDoubleSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QDoubleValidator

from controller.MaterialeController import MaterialeController
from model.Materiale import Materiale


class InserisciMateriale(QMainWindow):
    materiale_inserito = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Inserisci materiale")
        self.resize(500, 500)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Inserisci materiale")
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

        self.nome_input = self.create_input("Nome:", placeholder="Inserisci nome")
        self.categoria_input = self.create_input("Categoria:", placeholder="Es. Shampoo, Tinta, etc.")
        self.prezzo_spinbox = self.create_doublespinbox("Prezzo:", min_val=0.00, max_val=1000.00, step=0.50)
        self.quantita_spinbox = self.create_spinbox("Quantità:", min_val=0, max_val=10000)
        self.soglia_scorte_spinbox = self.create_spinbox("Soglia scorte:", min_val=0, max_val=1000)

        form_layout.addLayout(self.nome_input)
        form_layout.addLayout(self.categoria_input)
        form_layout.addLayout(self.prezzo_spinbox)
        form_layout.addLayout(self.quantita_spinbox)
        form_layout.addLayout(self.soglia_scorte_spinbox)

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

    def handle_confirm(self):
        nome = self.input_fields['nome'].text().strip()
        categoria = self.input_fields['categoria'].text().strip()
        prezzo = self.input_fields['prezzo'].value()
        quantita = self.input_fields['quantità'].value()
        soglia_scorte = self.input_fields['soglia scorte'].value()

        if not nome or not categoria:
            QMessageBox.critical(self, "Errore", "Nome e categoria sono obbligatori.")
            return

        controller = MaterialeController()

        try:
            nuovo_materiale = Materiale(
                nome=nome,
                categoria=categoria,
                prezzo=prezzo,
                quantita=quantita,
                soglia_scorte=soglia_scorte
            )
            controller.aggiungi_materiale(nuovo_materiale)
            QMessageBox.information(self, "Successo", f"Materiale '{nome}' inserito con successo.")
            self.materiale_inserito.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
