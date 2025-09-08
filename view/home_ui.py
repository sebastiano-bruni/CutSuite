import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

# Importa le classi delle view
from view.GestioneClienti.gestioneClienti_ui import GestioneClienti
from view.GestioneDipendenti.gestioneDipendenti_ui import GestioneDipendenti
from view.GestioneMagazzino.gestioneMagazzino_ui import GestioneMagazzino
from view.GestionePrenotazioni.gestionePrenotazioni_ui import GestionePrenotazioni
from view.GestionePromozioni.gestionePromozioni_ui import GestionePromozioni
from view.GestioneServizi.gestioneServizi_ui import GestioneServizi
from controller.MaterialeController import MaterialeController
from auth.permission import role_of
from auth.permission import is_allowed


class HomeWindow(QMainWindow):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("CutSuite - Dashboard")
        self.resize(1200, 800)
        self.setMinimumSize(800, 600)

        self.client_window = None
        self.dipendenti_window = None
        self.prenotazioni_window = None
        self.servizi_window = None
        self.magazzino_window = None
        self.promozioni_window = None

        self.init_ui()
        self.check_scorte_basse()

    def check_scorte_basse(self):

        materiale_controller = MaterialeController()
        sotto_soglia = materiale_controller.get_materiali_sotto_soglia()

        if sotto_soglia:
            nomi = "\n".join(f"- {m.nome}" for m in sotto_soglia)

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attenzione: Scorte basse")
            msg.setText("I seguenti materiali hanno scorte sotto la soglia minima (20):")
            msg.setInformativeText(nomi)
            msg.exec()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Barra superiore (Top Bar)
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #d0d0d0;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        title_label = QLabel("CutSuite")
        title_font = QFont("Arial", 22, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #333333;")

        #user_label = QLabel("Username: seba.staff")
        display_name = f"{getattr(self.user, 'nome', '')} {getattr(self.user, 'cognome', '')}".strip() or self.user.username
        user_label = QLabel(f"Utente: {display_name} ({role_of(self.user)})")
        user_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        user_font = QFont("Arial", 14)
        user_label.setFont(user_font)
        user_label.setStyleSheet("color: #555555;")

        logout_button = QPushButton("Logout")
        logout_button.setFixedSize(90, 35)
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(user_label)
        top_layout.addSpacing(15)
        top_layout.addWidget(logout_button)
        main_layout.addWidget(top_bar)

        # Area dei pulsanti
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("background-color: #f8f8f8;")
        buttons_layout = QGridLayout(buttons_frame)
        buttons_layout.setSpacing(30)
        buttons_layout.setContentsMargins(50, 50, 50, 50)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons_data = [
            ("Gestione Clienti", 0, 0),
            ("Gestione Prenotazioni", 0, 1),
            ("Gestione Servizi", 1, 0),
            ("Gestione Dipendenti", 1, 1),
            ("Gestione Magazzino", 2, 0),
            ("Gestione Promozioni", 2, 1)
        ]

        button_style_base = """
            QPushButton {
                background-color: #ffffff;
                color: #2c3e50;
                border: 2px solid #bdc3c7;
                border-radius: 12px;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #ecf0f1;
                border-color: #95a5a6;
            }
        """

        for text, row, col in buttons_data:
            button = QPushButton(text)
            button.setStyleSheet(button_style_base)
            button.setMinimumSize(250, 100)

            allowed = is_allowed(self.user, text)
            if allowed:
                buttons_layout.addWidget(button, row, col)
                button.clicked.connect(lambda checked, t=text: self.handle_button_click(t))
            # se non è allowed, non aggiungo il bottone → quindi sparisce dalla dashboard

        main_layout.addWidget(buttons_frame)
        main_layout.setStretchFactor(buttons_frame, 1)

        logout_button.clicked.connect(self.logout)

    def logout(self):
        from view.accesso_ui import LoginWindow  # import locale per evitare cicli
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def handle_button_click(self, button_text):
        if button_text == "Gestione Clienti":
            self.open_client_management()
        elif button_text == "Gestione Dipendenti":
            self.open_dipendenti_management()
        elif button_text == "Gestione Prenotazioni":
            self.open_prenotazioni_management()
        elif button_text == "Gestione Servizi":
            self.open_servizi_management()
        elif button_text == "Gestione Magazzino":
            self.open_magazzino_management()
        elif button_text == "Gestione Promozioni":
            self.open_promozioni_management()

    def open_client_management(self):
        if self.client_window is None:
            self.client_window = GestioneClienti()
        self.client_window.show()
        self.client_window.raise_()
        self.client_window.activateWindow()

    def open_dipendenti_management(self):
        if self.dipendenti_window is None:
            self.dipendenti_window = GestioneDipendenti()
        self.dipendenti_window.show()
        self.dipendenti_window.raise_()
        self.dipendenti_window.activateWindow()

    def open_magazzino_management(self):
        if self.magazzino_window is None:
            self.magazzino_window = GestioneMagazzino()
        self.magazzino_window.show()
        self.magazzino_window.raise_()
        self.magazzino_window.activateWindow()

    def open_servizi_management(self):
        if self.servizi_window is None:
            self.servizi_window = GestioneServizi()
        self.servizi_window.show()
        self.servizi_window.raise_()
        self.servizi_window.activateWindow()

    def open_promozioni_management(self):
        if self.promozioni_window is None:
            self.promozioni_window = GestionePromozioni()
        self.promozioni_window.show()
        self.promozioni_window.raise_()
        self.promozioni_window.activateWindow()

    def open_prenotazioni_management(self):
        if self.prenotazioni_window is None:
            self.prenotazioni_window = GestionePrenotazioni()
        self.prenotazioni_window.show()
        self.prenotazioni_window.raise_()
        self.prenotazioni_window.activateWindow()
