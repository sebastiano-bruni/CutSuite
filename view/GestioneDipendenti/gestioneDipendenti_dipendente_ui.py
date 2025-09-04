# CutSuite/view/GestioneDipendenti/gestioneDipendenti_dipendente_ui.py
from view.GestioneDipendenti.gestioneDipendenti_ui import GestioneDipendenti
from view.GestioneDipendenti.dettagliDipendente_ui import DettagliDipendente


class DettagliDipendenteDipendente(DettagliDipendente):

    def __init__(self, dipendente):
        super().__init__(dipendente)

        if hasattr(self, "edit_button"):
            self.edit_button.hide()
        if hasattr(self, "delete_button"):
            self.delete_button.hide()


class GestioneDipendentiDipendente(GestioneDipendenti):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, "add_button"):
            self.add_button.hide()

    def dettagli_dipendente(self, dip):
        # Mostra la versione read-only dei dettagli
        self.dettagli_window = DettagliDipendenteDipendente(dip)
        self.dettagli_window.dipendente_modificato.connect(self.aggiorna_lista_dipendenti)
        self.dettagli_window.show()
        self.dettagli_window.raise_()
        self.dettagli_window.activateWindow()
