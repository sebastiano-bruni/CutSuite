import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accesso")
        self.resize(500, 400)
        self.setStyleSheet("background-color: #f5f5f5;")

        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # Titolo
        title_label = QLabel("Accesso")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
            }
        """)
        main_layout.addWidget(title_label)

        # Istruzione
        instruction_label = QLabel("Inserisci le credenziali di accesso:")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #666666;
                padding: 5px;
            }
        """)
        main_layout.addWidget(instruction_label)

        # Form di login
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #dddddd;
            }
        """)
        form_frame.setFixedWidth(400)

        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # Username
        username_layout = QVBoxLayout()
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Inserisci username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #dddddd;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
        """)
        self.username_input.setMinimumHeight(40)

        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        form_layout.addLayout(username_layout)

        # Password
        password_layout = QVBoxLayout()
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333333;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Inserisci password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #dddddd;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
            }
        """)
        self.password_input.setMinimumHeight(40)

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)

        main_layout.addWidget(form_frame)

        # Bottone Login
        login_button = QPushButton("Login")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a6496;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        login_button.setMinimumHeight(50)
        login_button.clicked.connect(self.handle_login)

        # Centra il bottone
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(login_button)

        main_layout.addWidget(button_container)
        main_layout.addStretch()

        # Collega il tasto Enter al login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username:
            self.show_error("Inserisci un username")
            return

        if not password:
            self.show_error("Inserisci una password")
            return

        # Qui implementerai la logica di autenticazione
        print(f"Tentativo di login: Username={username}, Password={password}")

        # Esempio di login riuscito (da sostituire con la tua logica)
        if username == "admin" and password == "admin":
            self.show_success("Login riuscito!")
            self.open_home_window(username)
        else:
            self.show_error("Credenziali non valide")

    def show_error(self, message):
        # Qui puoi implementare la visualizzazione degli errori
        print(f"ERRORE: {message}")
        # Esempio: potresti usare QMessageBox o una label di errore

    def show_success(self, message):
        # Qui puoi implementare la visualizzazione del successo
        print(f"SUCCESSO: {message}")

    def open_home_window(self, username):
        # Qui aprirai la finestra principale
        print(f"Apertura home window per: {username}")
        # Esempio:
        # self.home_window = HomeWindow(username)
        # self.home_window.show()
        # self.hide()