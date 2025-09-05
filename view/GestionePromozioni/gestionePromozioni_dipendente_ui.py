# CutSuite/view/GestionePromozioni/gestionePromozioni_dipendente_ui.py
from view.GestionePromozioni.gestionePromozioni_ui import GestionePromozioni
from view.GestionePromozioni.dettagliPromozione_ui import DettagliPromozione


class DettagliPromozioneDipendente(DettagliPromozione):

    def __init__(self, promozione):
        super().__init__(promozione)

        if hasattr(self, "edit_button"):
            self.edit_button.hide()
        if hasattr(self, "delete_button"):
            self.delete_button.hide()


class GestionePromozioniDipendente(GestionePromozioni):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, "add_button"):
            self.add_button.hide()

    def dettagli_promozione(self, promo):
        # Mostra la versione read-only dei dettagli
        self.dettagli_window = DettagliPromozioneDipendente(promo)
        self.dettagli_window.promozione_modificata.connect(self.aggiorna_lista_promozioni)
        self.dettagli_window.show()
        self.dettagli_window.raise_()
        self.dettagli_window.activateWindow()
