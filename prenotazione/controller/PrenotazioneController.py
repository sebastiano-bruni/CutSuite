from prenotazione.model.Prenotazione import Prenotazione

class PrenotazioneController:
    def __init__(self):
        self.prenotazioni = []

    def aggiungi_prenotazione(self, prenotazione: Prenotazione):
        self.prenotazioni.append(prenotazione)

    def get_prenotazione_by_id(self, id):
        return next((p for p in self.prenotazioni if p.id == id), None)

    def rimuovi_prenotazione(self, id):
        self.prenotazioni = [p for p in self.prenotazioni if p.id != id]

    def aggiorna_prenotazione(self, id, **kwargs):
        prenotazione = self.get_prenotazione_by_id(id)
        if prenotazione:
            for key, value in kwargs.items():
                setattr(prenotazione, key, value)
            return True
        return False

    def get_tutte_prenotazioni(self):
        return self.prenotazioni