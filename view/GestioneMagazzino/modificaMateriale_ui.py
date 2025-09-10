import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QMessageBox, QSpinBox,
    QDoubleSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from controller.MaterialeController import MaterialeController


class ModificaMateriale(QMainWindow):
    materiale_modificato = pyqtSignal()

    def __init__(self, materiale):
        super().__init__()
        self.materiale = materiale
        self.setWindowTitle("CutSuite - Modifica materiale")
        self.resize(500, 500)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("CutSuite - Modifica materiale")
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

        self.nome_input = self.create_input("Nome:", self.materiale.nome)
        self.categoria_input = self.create_input("Categoria:", self.materiale.categoria)
        self.prezzo_spinbox = self.create_doublespinbox("Prezzo:", value=self.materiale.prezzo, min_val=0.00,
                                                        max_val=1000.00, step=0.50)
        self.quantita_spinbox = self.create_spinbox("Quantità:", value=self.materiale.quantita, min_val=0,
                                                    max_val=10000)
        self.soglia_scorte_spinbox = self.create_spinbox("Soglia scorte:", value=self.materiale.soglia_scorte,
                                                         min_val=0, max_val=1000)

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

    def validate_data(self, nome, categoria, prezzo):
        errors = []
        if not nome or len(nome) < 2:
            errors.append("• Il nome deve contenere almeno 2 caratteri.")
        if not categoria or len(categoria) < 2:
            errors.append("• La categoria deve contenere almeno 2 caratteri.")
        if prezzo <= 0:
            errors.append("• Il prezzo deve essere maggiore di zero.")
        return errors

    def handle_confirm(self):
        modified_data = {
            "nome": self.input_fields['nome'].text().strip(),
            "categoria": self.input_fields['categoria'].text().strip(),
            "prezzo": self.input_fields['prezzo'].value(),
            "quantita": self.input_fields['quantità'].value(),
            "soglia_scorte": self.input_fields['soglia scorte'].value()
        }

        errors = self.validate_data(modified_data["nome"], modified_data["categoria"], modified_data["prezzo"])
        if errors:
            error_message = "Si sono verificati i seguenti errori:\n\n" + "\n".join(errors)
            QMessageBox.critical(self, "Errori di validazione", error_message)
            return

        controller = MaterialeController()

        try:
            success = controller.aggiorna_materiale(self.materiale.id, **modified_data)
            if success:
                QMessageBox.information(self, "Successo",
                                        f"Materiale '{modified_data['nome']}' modificato con successo.")
                self.materiale_modificato.emit()
                self.close()
            else:
                QMessageBox.critical(self, "Errore", "Impossibile aggiornare il materiale.")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Si è verificato un errore: {e}")
