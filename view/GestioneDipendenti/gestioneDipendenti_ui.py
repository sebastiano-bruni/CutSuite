import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QGroupBox,
    QScrollArea, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from controller.DipendenteController import DipendenteController
from view.GestioneDipendenti.dettagliDipendente_ui import DettagliDipendente
from view.GestioneDipendenti.inserisciDipendente_ui import InserisciDipendente


class GestioneDipendenti(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Gestione Dipendenti")
        self.resize(1000, 700)
        self.inserisci_window = None
        self.dettagli_window = None
        self.controller = DipendenteController()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("CutSuite - Gestione Dipendenti")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                padding: 10px 0;
            }
        """)
        main_layout.addWidget(title_label)

        search_group = QGroupBox("Ricerca:")
        search_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

        search_layout = QVBoxLayout(search_group)

        sort_layout = QHBoxLayout()
        sort_label = QLabel("Ordina per:")
        sort_label.setStyleSheet("font-weight: bold;")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Nome A-Z", "Nome Z-A"])
        self.sort_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                min-width: 150px;
            }
        """)
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addStretch()
        search_layout.addLayout(sort_layout)

        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        separator1.setStyleSheet("color: #cccccc;")
        search_layout.addWidget(separator1)

        search_fields_layout = QHBoxLayout()
        name_layout = QVBoxLayout()
        name_label = QLabel("Ricerca per nome")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Inserisci nome")
        self.name_input.setStyleSheet("padding: 8px; border: 1px solid #cccccc; border-radius: 4px;")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)

        surname_layout = QVBoxLayout()
        surname_label = QLabel("Ricerca per cognome")
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Inserisci cognome")
        self.surname_input.setStyleSheet("padding: 8px; border: 1px solid #cccccc; border-radius: 4px;")
        surname_layout.addWidget(surname_label)
        surname_layout.addWidget(self.surname_input)

        role_layout = QVBoxLayout()
        role_label = QLabel("Filtro ruolo")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Tutti", "Parrucchiere", "Proprietario"])
        self.role_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                min-width: 150px;
            }
        """)
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)

        search_fields_layout.addLayout(name_layout)
        search_fields_layout.addLayout(surname_layout)
        search_fields_layout.addLayout(role_layout)
        search_layout.addLayout(search_fields_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        search_button = QPushButton("Cerca")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        search_button.clicked.connect(self.handle_search)

        reset_button = QPushButton("Reset")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #cccccc;
                color: #333333;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #bbbbbb;
            }
        """)
        reset_button.clicked.connect(self.handle_reset)

        buttons_layout.addWidget(search_button)
        buttons_layout.addWidget(reset_button)
        search_layout.addLayout(buttons_layout)
        main_layout.addWidget(search_group)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        separator2.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator2)

        employees_label = QLabel("Lista dipendenti")
        employees_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(employees_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #cccccc;
                border-radius: 6px;
                background-color: white;
            }
        """)
        scroll_widget = QWidget()
        self.employees_layout = QVBoxLayout(scroll_widget)
        self.employees_layout.setSpacing(10)
        self.employees_layout.setContentsMargins(15, 15, 15, 15)

        self.display_employees(self.controller.get_tutti_dipendenti())

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, 1)

        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.HLine)
        separator3.setFrameShadow(QFrame.Shadow.Sunken)
        separator3.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator3)

        add_button = QPushButton("Inserisci dipendente")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_button.clicked.connect(self.handle_add)
        main_layout.addWidget(add_button)

    def display_employees(self, employees):
        for i in reversed(range(self.employees_layout.count())):
            item = self.employees_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        for dip in employees:
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 6px;
                    padding: 10px;
                }
            """)
            layout = QHBoxLayout(frame)

            data_layout = QVBoxLayout()
            name_layout = QHBoxLayout()
            name_label = QLabel(dip.nome)
            name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            surname_label = QLabel(dip.cognome)
            surname_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            name_layout.addWidget(name_label)
            name_layout.addWidget(surname_label)
            name_layout.addStretch()
            data_layout.addLayout(name_layout)

            email_label = QLabel(dip.email)
            email_label.setStyleSheet("color: #666666; font-size: 13px;")
            data_layout.addWidget(email_label)
            data_layout.addStretch()

            layout.addLayout(data_layout, 1)

            details_btn = QPushButton("Dettagli")
            details_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 12px;
                    font-size: 12px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #5a6268;
                }
            """)
            details_btn.clicked.connect(lambda checked, d=dip: self.handle_details(d))
            layout.addWidget(details_btn)

            self.employees_layout.addWidget(frame)

        self.employees_layout.addStretch()

    def handle_search(self):
        self.controller.reload()
        name = self.name_input.text().strip().lower()
        surname = self.surname_input.text().strip().lower()
        role = self.role_combo.currentText()
        sort_order = self.sort_combo.currentText()

        all_employees = self.controller.get_tutti_dipendenti()
        filtered = [
            d for d in all_employees
            if (name in d.nome.lower() if name else True)
               and (surname in d.cognome.lower() if surname else True)
               and (role == "Tutti" or getattr(d, "ruolo", "").lower() == role.lower())
        ]

        reverse = (sort_order == "Nome Z-A")
        filtered.sort(key=lambda d: (d.nome or "").lower(), reverse=reverse)

        self.display_employees(filtered)

    def handle_reset(self):
        self.name_input.clear()
        self.surname_input.clear()
        self.role_combo.setCurrentIndex(0)
        self.sort_combo.setCurrentIndex(0)
        self.display_employees(self.controller.get_tutti_dipendenti())

    def handle_add(self):
        print("Apri form inserimento dipendente")
        self.inserisci_dipendente()

    def handle_details(self, dip):
        print(f"Apertura dettagli per dipendente: {dip.nome} {dip.cognome}")
        self.dettagli_dipendente(dip)

    def inserisci_dipendente(self):
        self.inserisci_window = InserisciDipendente()
        # Connetti il segnale della finestra di inserimento
        self.inserisci_window.dipendente_inserito.connect(self.aggiorna_lista_dipendenti)
        self.inserisci_window.show()
        self.inserisci_window.raise_()
        self.inserisci_window.activateWindow()

    def dettagli_dipendente(self, dip):
        self.dettagli_window = DettagliDipendente(dip)
        # Connetti il segnale della finestra dei dettagli
        self.dettagli_window.dipendente_modificato.connect(self.aggiorna_lista_dipendenti)
        self.dettagli_window.show()
        self.dettagli_window.raise_()
        self.dettagli_window.activateWindow()

    def aggiorna_lista_dipendenti(self):
        print("Aggiorno lista dipendenti...")
        self.controller.reload()
        self.display_employees(self.controller.get_tutti_dipendenti())
