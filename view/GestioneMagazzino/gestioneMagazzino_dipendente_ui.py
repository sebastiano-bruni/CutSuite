# CutSuite/view/GestionePromozioni/gestionePromozioni_dipendente_ui.py
from view.GestionePromozioni.gestionePromozioni_ui import GestionePromozioni
from view.GestionePromozioni.dettagliPromozione_ui import DettagliPromozione


class DettagliMaterialeDipendente(DettagliPromozione):

    def __init__(self, promozione):
        super().__init__(promozione)

        self.edit_button.hide()
        self.delete_button.hide()


class GestioneMagazziniDipendente(GestionePromozioni):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Nascondo il pulsante "Aggiungi promozione"
        self.add_button.hide()

    def dettagli_promozione(self, promo):
        """Mostra i dettagli della promozione in modalità read-only"""
        self.dettagli_window = DettagliMaterialeDipendente(promo)
        self.dettagli_window.promozione_modificata.connect(self.aggiorna_lista_promozioni)
        self.dettagli_window.show()
        self.dettagli_window.raise_()
        self.dettagli_window.activateWindow()
