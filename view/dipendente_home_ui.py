# CutSuite/view/dipendente_home_ui.py
from PyQt6.QtWidgets import QMessageBox
from view.home_ui import HomeWindow

class DipendenteHomeWindow(HomeWindow):

    def __init__(self, user, parent=None):
        super().__init__(user, parent)

    def open_dipendenti_management(self):
        # import locale per evitare cicli
        from view.GestioneDipendenti.gestioneDipendenti_dipendente_ui import GestioneDipendentiDipendente
        if self.dipendenti_window is None:
            self.dipendenti_window = GestioneDipendentiDipendente()
        self.dipendenti_window.show()
        self.dipendenti_window.raise_()
        self.dipendenti_window.activateWindow()

    def open_magazzino_management(self):
        from view.GestioneMagazzino.gestioneMagazzino_dipendente_ui import GestioneMagazzinoDipendente
        if self.magazzino_window is None:
            self.magazzino_window = GestioneMagazzinoDipendente()
        self.magazzino_window.show()
        self.magazzino_window.raise_()
        self.magazzino_window.activateWindow()

    def open_servizi_management(self):
        from view.GestioneServizi.gestioneServizi_dipendente_ui import GestioneServiziDipendente
        if self.servizi_window is None:
            self.servizi_window = GestioneServiziDipendente()
        self.servizi_window.show()
        self.servizi_window.raise_()
        self.servizi_window.activateWindow()