import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFrame, QComboBox, QGroupBox,
    QScrollArea, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

# Importa il controller che gestisce la logica del magazzino
from controller.MaterialeController import MaterialeController
from view.GestioneMagazzino.dettagliMateriale_ui import DettagliMateriale
from view.GestioneMagazzino.inserisciMateriale_ui import InserisciMateriale


class GestioneMagazzino(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CutSuite - Gestione Magazzino")
        self.resize(1000, 700)
        self.inserisci_window = None
        self.dettagli_window = None
        self.controller = MaterialeController()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("CutSuite - Gestione Magazzino")
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
        self.sort_combo.addItems(["Nome A-Z", "Nome Z-A", "Prezzo crescente", "Prezzo decrescente", "Durata crescente",
                                  "Durata decrescente"])
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

        category_layout = QVBoxLayout()
        category_label = QLabel("Ricerca per categoria")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Inserisci categoria")
        self.category_input.setStyleSheet("padding: 8px; border: 1px solid #cccccc; border-radius: 4px;")
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_input)

        search_fields_layout.addLayout(name_layout)
        search_fields_layout.addLayout(category_layout)
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

        materials_label = QLabel("Lista materiali")
        materials_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(materials_label)

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
        self.materials_layout = QVBoxLayout(scroll_widget)
        self.materials_layout.setSpacing(10)
        self.materials_layout.setContentsMargins(15, 15, 15, 15)

        self.display_materials(self.controller.get_tutti_materiali())

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, 1)

        separator3 = QFrame()
        separator3.setFrameShape(QFrame.Shape.HLine)
        separator3.setFrameShadow(QFrame.Shadow.Sunken)
        separator3.setStyleSheet("color: #cccccc;")
        main_layout.addWidget(separator3)

        add_button = QPushButton("Inserisci materiale")
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

    def display_materials(self, materials):
        for i in reversed(range(self.materials_layout.count())):
            item = self.materials_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        for mat in materials:
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
            name_label = QLabel(mat.nome)
            name_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            category_label = QLabel(mat.categoria)
            category_label.setStyleSheet("color: #666666; font-size: 13px;")
            data_layout.addWidget(name_label)
            data_layout.addWidget(category_label)
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
            details_btn.clicked.connect(lambda checked, m=mat: self.handle_details(m))
            layout.addWidget(details_btn)

            self.materials_layout.addWidget(frame)

        self.materials_layout.addStretch()

    def handle_search(self):
        self.controller.reload()
        name = self.name_input.text().strip().lower()
        category = self.category_input.text().strip().lower()
        sort_order = self.sort_combo.currentText()

        all_materials = self.controller.get_tutti_materiali()
        filtered = [
            m for m in all_materials
            if (name in m.nome.lower() if name else True)
               and (category in m.categoria.lower() if category else True)
        ]

        if sort_order == "Prezzo crescente":
            filtered.sort(key=lambda m: m.prezzo)
        elif sort_order == "Prezzo decrescente":
            filtered.sort(key=lambda m: m.prezzo, reverse=True)
        elif sort_order == "Durata crescente":
            filtered.sort(key=lambda m: m.durata_minuti)
        elif sort_order == "Durata decrescente":
            filtered.sort(key=lambda m: m.durata_minuti, reverse=True)
        elif sort_order == "Nome Z-A":
            filtered.sort(key=lambda m: m.nome, reverse=True)
        else:  # Nome A-Z
            filtered.sort(key=lambda m: m.nome)

        self.display_materials(filtered)

    def handle_reset(self):
        self.name_input.clear()
        self.category_input.clear()
        self.sort_combo.setCurrentIndex(0)
        self.display_materials(self.controller.get_tutti_materiali())

    def handle_add(self):
        print("Apertura form per inserimento nuovo materiale")
        self.inserisci_materiale()

    def handle_details(self, mat):
        print(f"Apertura dettagli per materiale: {mat.nome}")
        self.dettagli_materiale(mat)

    def inserisci_materiale(self):
        self.inserisci_window = InserisciMateriale()
        # Connetti il segnale della finestra di inserimento
        self.inserisci_window.materiale_inserito.connect(self.aggiorna_lista_materiali)
        self.inserisci_window.show()
        self.inserisci_window.raise_()
        self.inserisci_window.activateWindow()

    def dettagli_materiale(self, mat):
        self.dettagli_window = DettagliMateriale(mat)
        # Connetti il segnale della finestra dei dettagli
        self.dettagli_window.materiale_modificato.connect(self.aggiorna_lista_materiali)
        self.dettagli_window.show()
        self.dettagli_window.raise_()
        self.dettagli_window.activateWindow()

    def aggiorna_lista_materiali(self):
        print("Aggiorno lista materiali...")
        self.controller.reload()
        self.display_materials(self.controller.get_tutti_materiali())

    def listaMateriali(self):
        return self.controller.get_tutti_materiali()
