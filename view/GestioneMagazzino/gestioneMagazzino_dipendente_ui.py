# CutSuite/view/GestioneMagazzino/gestioneMagazzino_dipendente_ui.py
from PyQt6.QtWidgets import QMessageBox
from view.GestioneMagazzino.gestioneMagazzino_ui import GestioneMagazzino
from view.GestioneMagazzino.dettagliMateriale_ui import DettagliMateriale
from view.GestioneMagazzino.modificaMateriale_ui import ModificaMateriale

class DettagliMaterialeDipendente(DettagliMateriale):

    def __init__(self, materiale):
        super().__init__(materiale)

        if hasattr(self, "edit_button"):
            self.edit_button.hide()

class GestioneMagazzinoDipendente(GestioneMagazzino):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dettagli_materiale(self, mat):

        self.dettagli_window = DettagliMaterialeDipendente(mat)
        self.dettagli_window.materiale_modificato.connect(self.aggiorna_lista_materiali)
        self.dettagli_window.show()
        self.dettagli_window.raise_()
        self.dettagli_window.activateWindow()
