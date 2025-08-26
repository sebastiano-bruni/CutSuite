from promozione.model.Promozione import Promozione

class PromozioneController:
    def __init__(self):
        self.promozioni = []

    def aggiungi_promozione(self, promozione: Promozione):
        self.promozioni.append(promozione)

    def get_promozione_by_id(self, id):
        return next((p for p in self.promozioni if p.id == id), None)

    def rimuovi_promozione(self, id):
        self.promozioni = [p for p in self.promozioni if p.id != id]

    def aggiorna_promozione(self, id, **kwargs):
        promozione = self.get_promozione_by_id(id)
        if promozione:
            for key, value in kwargs.items():
                setattr(promozione, key, value)
            return True
        return False

    def get_tutte_promozioni(self):
        return self.promozioni