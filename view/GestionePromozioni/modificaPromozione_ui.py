import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QSpinBox,
    QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont

from controller.PromozioneController import PromozioneController


class ModificaPromozione(QMainWindow):
    promozione_modificata = pyqtSignal()

    def __init__(self, promozione):
        super().__init__()
        self.promozione = promozione
        self.setWindowTitle("CutSuite - Modifica promozione")
        self.resize(500, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Modifica promozione")
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

        self.nome_input = self.create_input("Nome:", self.promozione.nome)
        self.descrizione_input = self.create_textedit("Descrizione:", self.promozione.descrizione)
        self.soglia_spinbox = self.create_spinbox("Soglia:", value=self.promozione.soglia_promozione, min_val=0,
                                                  max_val=100)
        self.sconto_spinbox = self.create_spinbox("Sconto (%):", value=self.promozione.sconto_percentuale, min_val=0,
                                                  max_val=100)

        form_layout.addLayout(self.nome_input)
        form_layout.addLayout(self.descrizione_input)
        form_layout.addLayout(self.soglia_spinbox)
        form_layout.addLayout(self.sconto_spinbox)

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

    def create_input(self, label_text, value=""):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        line_edit = QLineEdit(value)
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
        self.input_fields[label_text.replace(":", "").strip().lower()] = text_edit
        return v_layout

    def create_spinbox(self, label_text, value=0, min_val=0, max_val=100):
        v_layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(value)
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
        modified_data = {
            "nome": self.input_fields['nome'].text().strip(),
            "descrizione": self.input_fields['descrizione'].toPlainText().strip(),
            "soglia_promozione": self.input_fields['soglia'].value(),
            "sconto_percentuale": self.input_fields['sconto (%)'].value()
        }

        if not modified_data["nome"] or not modified_data["descrizione"]:
            QMessageBox.critical(self, "Errore", "Nome e descrizione non possono essere vuoti.")
            return

        controller = PromozioneController()

        try:
            success = controller.aggiorna_promozione(self.promozione.id, **modified_data)
            if success:
                QMessageBox.information(self, "Successo",
                                        f"Promozione '{modified_data['nome']}' modificata con successo.")
                self.promozione_modificata.emit()
                self.close()
            else:
                QMessageBox.critical(self, "Errore", "Impossibile aggiornare la promozione.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
