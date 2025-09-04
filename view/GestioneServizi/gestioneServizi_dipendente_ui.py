# CutSuite/view/GestioneServizi/gestioneServizi_dipendente_ui.py
from view.GestioneServizi.gestioneServizi_ui import GestioneServizi


class GestioneServiziDipendente(GestioneServizi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 Nascondo il pulsante "Inserisci servizio"
        if hasattr(self, "add_button"):
            self.add_button.hide()
