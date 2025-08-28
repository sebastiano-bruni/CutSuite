import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QGroupBox,
    QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from controller.ClienteController import ClienteController
from view.GestioneClienti.inserisciCliente_ui import InserisciCliente


class GestioneClienti(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Gestione Clienti")
        self.resize(1000, 700)
        self.client_window = None
        self.controller = ClienteController()

        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Titolo
        title_label = QLabel("CutSuite - Gestione Clienti")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
                padding: 10px 0;
            }
        """)
        main_layout.addWidget(title_label)

        # Sezione Ricerca
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

        # Ordina per
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

        # Separatore
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        separator1.setStyleSheet("color: #cccccc;")
        search_layout.addWidget(separator1)

        # Ricerca per nome e cognome
        search_fields_layout = QHBoxLayout()

        name_search_layout = QVBoxLayout()
        name_search_label = QLabel("Ricerca per nome")
        self.name_search_input = QLineEdit()
        self.name_search_input.setPlaceholderText("Inserisci nome")
        self.name_search_input.setStyleSheet("padding: 8px; border: 1px solid #cccccc; border-radius: 4px;")
        name_search_layout.addWidget(name_search_label)
        name_search_layout.addWidget(self.name_search_input)

        surname_search_layout = QVBoxLayout()
        surname_search_label = QLabel("Ricerca per cognome")
        self.surname_search_input = QLineEdit()
        self.surname_search_input.setPlaceholderText("Inserisci cognome")
        self.surname_search_input.setStyleSheet("padding: 8px; border: 1px solid #cccccc; border-radius: 4px;")
        surname_search_layout.addWidget(surname_search_label)
        surname_search_layout.addWidget(self.surname_search_input)

        search_fields_layout.addLayout(name_search_layout)
        search_fields_layout.addLayout(surname_search_layout)
        search_layout.addLayout(search_fields_layout)

        # Pulsanti Cerca e Reset
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

        # Separatore
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        separator2.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator2)

        # Lista Clienti
        clients_label = QLabel("Name")
        clients_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(clients_label)

        # Area scrollabile per i clienti
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #cccccc;
                border-radius: 6px;
                background-color: white;
            }
        """)

        clients_widget = QWidget()
        self.clients_layout = QVBoxLayout(clients_widget)
        self.clients_layout.setSpacing(10)
        self.clients_layout.setContentsMargins(15, 15, 15, 15)

        # Dati dei clienti
        self.display_clients(self.controller.get_tutti_clienti())

        self.display_clients(self.controller.get_tutti_clienti())

        scroll_area.setWidget(clients_widget)
        main_layout.addWidget(scroll_area, 1)  # 1 = stretch factor

        # Separatore
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.HLine)
        separator3.setFrameShadow(QFrame.Shadow.Sunken)
        separator3.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator3)

        # Pulsante Inserisci cliente
        add_client_button = QPushButton("Inserisci cliente")
        add_client_button.setStyleSheet("""
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
        add_client_button.clicked.connect(self.handle_add_client)
        main_layout.addWidget(add_client_button)

    def display_clients(self, clients):
        # Rimuovi tutti i widget esistenti
        for i in reversed(range(self.clients_layout.count())):
            item = self.clients_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        # Aggiungi i clienti
        for client in clients:
            client_frame = QFrame()
            client_frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 6px;
                    padding: 10px;
                }
            """)

            client_grid = QGridLayout(client_frame)
            client_grid.setSpacing(5)

            # Nome in grassetto
            name_label = QLabel(client.nome)  # usa l’oggetto Cliente
            name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            client_grid.addWidget(name_label, 0, 0)

            # Cognome in grassetto
            surname_label = QLabel(client.cognome)
            surname_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            client_grid.addWidget(surname_label, 0, 1)

            # Email
            email_label = QLabel(client.email)
            email_label.setStyleSheet("color: #666666; font-size: 13px;")
            client_grid.addWidget(email_label, 1, 0, 1, 2)

            self.clients_layout.addWidget(client_frame)

        # Aggiungi stretch per spingere tutto verso l'alto
        self.clients_layout.addStretch()

    def handle_search(self):
        name = self.name_search_input.text().strip().lower()
        surname = self.surname_search_input.text().strip().lower()
        sort_order = self.sort_combo.currentText()

        # filtra
        all_clients = self.controller.get_tutti_clienti()
        filtered = [
            c for c in all_clients
            if (name in c.nome.lower() if name else True)
            and (surname in c.cognome.lower() if surname else True)
        ]

        # ordina
        reverse = (sort_order == "Nome Z-A")
        filtered.sort(key=lambda c: (c.nome or "").lower(), reverse=reverse)

        self.display_clients(filtered)


    def handle_reset(self):
        self.name_search_input.clear()
        self.surname_search_input.clear()
        self.sort_combo.setCurrentIndex(0)
        self.display_clients(self.controller.get_tutti_clienti())

    def handle_add_client(self):
        print("Apertura form per inserimento nuovo cliente")
        # Qui implementerai l'apertura del form di inserimento cliente
        self.inserisci_cliente()


    def inserisci_cliente(self):
            if self.client_window is None:
                self.client_window = InserisciCliente()
            self.client_window.show()
            self.client_window.raise_()  # porta davanti la finestra
            self.client_window.activateWindow()

