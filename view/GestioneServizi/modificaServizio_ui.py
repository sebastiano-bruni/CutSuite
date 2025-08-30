import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QSpinBox,
    QDoubleSpinBox, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from controller.ServizioController import ServizioController


class ModificaServizio(QMainWindow):
    servizio_modificato = pyqtSignal()

    def __init__(self, servizio):
        super().__init__()
        self.servizio = servizio
        self.setWindowTitle("CutSuite - Modifica servizio")
        self.resize(500, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Modifica servizio")
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

        self.nome_input = self.create_input("Nome:", self.servizio.nome)
        self.durata_spinbox = self.create_spinbox("Durata (minuti):", value=self.servizio.durata_minuti, min_val=0,
                                                  max_val=240, step=5)
        self.prezzo_doublespinbox = self.create_doublespinbox("Prezzo:", value=self.servizio.prezzo, min_val=0.00,
                                                              max_val=1000.00, step=0.50)
        self.descrizione_input = self.create_textedit("Descrizione:", self.servizio.descrizione)

        # Campi aggiuntivi per il materiale (non presenti nel mockup, ma utili)
        # self.materiale_necessario_input = self.create_input("Materiale necessario:", self.servizio.materiale_necessario)
        # self.quantita_materiale_spinbox = self.create_spinbox("Quantità materiale:", value=self.servizio.quantita_materiale, min_val=0, max_val=100)

        form_layout.addLayout(self.nome_input)
        form_layout.addLayout(self.durata_spinbox)
        form_layout.addLayout(self.prezzo_doublespinbox)
        form_layout.addLayout(self.descrizione_input)
        # form_layout.addLayout(self.materiale_necessario_input)
        # form_layout.addLayout(self.quantita_materiale_spinbox)

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
        spinbox.setRange(int(min_val), int(max_val))
        spinbox.setValue(int(value))
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
        modified_data = {
            "nome": self.input_fields['nome'].text().strip(),
            "durata_minuti": self.input_fields['durata (minuti)'].value(),
            "prezzo": self.input_fields['prezzo'].value(),
            "descrizione": self.input_fields['descrizione'].toPlainText().strip()
            # "materiale_necessario": self.input_fields['materiale necessario'].text().strip(),
            # "quantita_materiale": self.input_fields['quantità materiale'].value()
        }

        if not modified_data["nome"] or not modified_data["descrizione"]:
            QMessageBox.critical(self, "Errore", "Nome e descrizione non possono essere vuoti.")
            return

        controller = ServizioController()

        try:
            success = controller.aggiorna_servizio(self.servizio.id, **modified_data)
            if success:
                QMessageBox.information(self, "Successo",
                                        f"Servizio '{modified_data['nome']}' modificato con successo.")
                self.servizio_modificato.emit()
                self.close()
            else:
                QMessageBox.critical(self, "Errore", "Impossibile aggiornare il servizio.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
