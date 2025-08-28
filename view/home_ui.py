from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout
)

from view.GestioneClienti.gestioneClienti_ui import GestioneClienti


class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite")
        self.resize(1000, 700)  # Aumentata le dimensioni della finestra
        self.client_window = None

        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Barra superiore
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_bar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #d0d0d0;")

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        title_label = QLabel("CutSuite")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        user_label = QLabel("Username: seba.staff")
        user_label.setStyleSheet("font-size: 14px;")

        logout_button = QPushButton("Logout")
        logout_button.setFixedSize(80, 30)
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)

        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(user_label)
        top_layout.addSpacing(10)
        top_layout.addWidget(logout_button)

        main_layout.addWidget(top_bar)

        # Area dei pulsanti
        buttons_frame = QFrame()
        buttons_layout = QGridLayout(buttons_frame)
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(40, 40, 40, 40)

        # Creazione dei pulsanti con dimensioni diverse
        buttons_data = [
            ("Gestione Clienti", "Gestione Prenotazioni"),
            ("Gestione Servizi", "Gestione Dipendenti"),
            ("Gestione Magazzino", "Gestione Promozioni")
        ]

        # Stile per i primi 4 bottoni (più grandi)
        large_button_style = """
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #d0d0d0;
                border-radius: 8px;
                padding: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f8f8f8;
                border-color: #a0a0a0;
            }
        """

        # Stile per gli altri bottoni (più piccoli)
        small_button_style = """
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #d0d0d0;
                border-radius: 8px;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f8f8f8;
                border-color: #a0a0a0;
            }
        """

        # Primi 4 bottoni (più grandi) - prime due righe
        for row, (left_text, right_text) in enumerate(buttons_data[:2]):
            left_button = QPushButton(left_text)
            left_button.setStyleSheet(large_button_style)
            left_button.setMinimumSize(350, 120)  # Dimensioni maggiori

            right_button = QPushButton(right_text)
            right_button.setStyleSheet(large_button_style)
            right_button.setMinimumSize(350, 120)  # Dimensioni maggiori

            buttons_layout.addWidget(left_button, row, 0)
            buttons_layout.addWidget(right_button, row, 1)

        # Ultimi 2 bottoni (più piccoli) - terza riga
        row = 2
        left_text, right_text = buttons_data[2]

        # Bottone sinistro
        left_button = QPushButton(left_text)
        left_button.setStyleSheet(small_button_style)
        left_button.setMinimumSize(300, 100)  # Più piccolo

        # Bottone destro
        right_button = QPushButton(right_text)
        right_button.setStyleSheet(small_button_style)
        right_button.setMinimumSize(300, 100)  # Più piccolo

        buttons_layout.addWidget(left_button, row, 0)
        buttons_layout.addWidget(right_button, row, 1)

        # Configurazione dello stretching per centrare i pulsanti
        buttons_layout.setColumnStretch(0, 1)
        buttons_layout.setColumnStretch(1, 1)
        buttons_layout.setRowStretch(0, 1)
        buttons_layout.setRowStretch(1, 1)
        buttons_layout.setRowStretch(2, 1)

        main_layout.addWidget(buttons_frame, 1)

        # Collega il pulsante di logout a una funzione
        logout_button.clicked.connect(self.logout)

        # Collega i pulsanti di gestione a funzioni (da implementare)
        self.connect_buttons(buttons_frame)

    def logout(self):
        print("Logout effettuato")
        # Qui andrebbe implementata la logica di logout

    def connect_buttons(self, buttons_frame):
        # Trova tutti i pulsanti e collega i segnali
        for button in buttons_frame.findChildren(QPushButton):
            if button.text() != "Logout":
                button.clicked.connect(lambda checked, text=button.text(): self.handle_button_click(text))

    def handle_button_click(self, button_text):
        print(f"Clicked: {button_text}")
        # Qui andrebbe implementata la logica per aprire la sezione corrispondente
        if button_text == "Gestione Clienti":
            self.open_client_management()

            # Qui potrai aggiungere gli altri bottoni:
            # elif button_text == "Gestione Prenotazioni":
            #     self.open_booking_management()
            # etc.

    def open_client_management(self):
            if self.client_window is None:
                self.client_window = GestioneClienti()
            self.client_window.show()
            self.client_window.raise_()  # porta davanti la finestra
            self.client_window.activateWindow()


