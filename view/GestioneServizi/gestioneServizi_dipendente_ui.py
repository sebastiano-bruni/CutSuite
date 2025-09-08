# CutSuite/view/GestioneServizi/gestioneServizi_dipendente_ui.py
from view.GestioneServizi.dettagliServizio_ui import DettagliServizio
from view.GestioneServizi.gestioneServizi_ui import GestioneServizi

class DettagliServizioDipendente(DettagliServizio):

    def __init__(self, promozione):
        super().__init__(promozione)

        if hasattr(self, "edit_button"):
            self.edit_button.hide()
        if hasattr(self, "delete_button"):
            self.delete_button.hide()

class GestioneServiziDipendente(GestioneServizi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, "add_button"):
            self.add_button.hide()
        if hasattr(self, "stats_button"):
            self.stats_button.hide()

    def dettagli_servizio(self, dip):
        # Mostra la versione read-only dei dettagli
        self.dettagli_window = DettagliServizioDipendente(dip)
        self.dettagli_window.servizio_modificato.connect(self.aggiorna_lista_servizi)
        self.dettagli_window.show()
        self.dettagli_window.raise_()
        self.dettagli_window.activateWindow()
