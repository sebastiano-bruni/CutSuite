import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QGroupBox,
    QScrollArea, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

# Importa il controller che gestisce la logica delle promozioni
from controller.PromozioneController import PromozioneController
from view.GestionePromozioni.dettagliPromozione_ui import DettagliPromozione
from view.GestionePromozioni.inserisciPromozione_ui import InserisciPromozione


class GestionePromozioni(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Gestione Promozioni")
        self.resize(1000, 700)
        self.inserisci_window = None
        self.dettagli_window = None
        self.controller = PromozioneController()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("CutSuite - Gestione Promozioni")
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
        self.sort_combo.addItems(["Nome A-Z", "Nome Z-A", "Sconto crescente", "Sconto decrescente"])
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

        search_fields_layout.addLayout(name_layout)
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

        promotions_label = QLabel("Lista promozioni")
        promotions_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(promotions_label)

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
        self.promotions_layout = QVBoxLayout(scroll_widget)
        self.promotions_layout.setSpacing(10)
        self.promotions_layout.setContentsMargins(15, 15, 15, 15)

        self.display_promotions(self.controller.get_tutte_promozioni())

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, 1)

        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.HLine)
        separator3.setFrameShadow(QFrame.Shadow.Sunken)
        separator3.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator3)

        self.add_button = QPushButton("Inserisci promozione")
        self.add_button.setStyleSheet("""
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
        self.add_button.clicked.connect(self.handle_add)
        main_layout.addWidget(self.add_button)

    def display_promotions(self, promotions):
        for i in reversed(range(self.promotions_layout.count())):
            item = self.promotions_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        for promo in promotions:
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
            name_label = QLabel(promo.nome)
            name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            discount_label = QLabel(f"Sconto: {promo.sconto_percentuale}%")
            discount_label.setStyleSheet("color: #666666; font-size: 13px;")
            data_layout.addWidget(name_label)
            data_layout.addWidget(discount_label)
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
            details_btn.clicked.connect(lambda checked, p=promo: self.handle_details(p))
            layout.addWidget(details_btn)

            self.promotions_layout.addWidget(frame)

        self.promotions_layout.addStretch()

    def handle_search(self):
        self.controller.reload()
        name = self.name_input.text().strip().lower()
        sort_order = self.sort_combo.currentText()

        all_promotions = self.controller.get_tutte_promozioni()
        filtered = [
            p for p in all_promotions
            if (name in p.nome.lower() if name else True)
        ]

        if sort_order == "Sconto crescente":
            filtered.sort(key=lambda p: p.sconto_percentuale)
        elif sort_order == "Sconto decrescente":
            filtered.sort(key=lambda p: p.sconto_percentuale, reverse=True)
        elif sort_order == "Nome Z-A":
            filtered.sort(key=lambda p: p.nome, reverse=True)
        else:  # Nome A-Z
            filtered.sort(key=lambda p: p.nome)

        self.display_promotions(filtered)

    def handle_reset(self):
        self.name_input.clear()
        self.sort_combo.setCurrentIndex(0)
        self.display_promotions(self.controller.get_tutte_promozioni())

    def handle_add(self):
        print("Apertura form per inserimento nuova promozione")
        self.inserisci_promozione()

    def handle_details(self, promo):
        print(f"Apertura dettagli per promozione: {promo.nome}")
        self.dettagli_promozione(promo)

    def inserisci_promozione(self):
        self.inserisci_window = InserisciPromozione()
        self.inserisci_window.promozione_inserita.connect(self.aggiorna_lista_promozioni)
        self.inserisci_window.show()
        self.inserisci_window.raise_()
        self.inserisci_window.activateWindow()

    def dettagli_promozione(self, promo):
        self.dettagli_window = DettagliPromozione(promo, parent_window=self)
        self.dettagli_window.promozione_modificata.connect(self.aggiorna_lista_promozioni)
        self.dettagli_window.show()
        self.dettagli_window.raise_()
        self.dettagli_window.activateWindow()

    def aggiorna_lista_promozioni(self):
        print("Aggiorno lista promozioni...")
        self.controller.reload()
        self.display_promotions(self.controller.get_tutte_promozioni())
