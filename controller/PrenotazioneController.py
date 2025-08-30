from model.Prenotazione import Prenotazione
from data.storage.storage_prenotazione import StoragePrenotazione
from datetime import datetime


class PrenotazioneController:
    def __init__(self):
        self.storage = StoragePrenotazione("data/files/prenotazioni.json")
        self.prenotazioni = self.storage.carica()

    def aggiungi_prenotazione(self, prenotazione: Prenotazione):
        self.prenotazioni.append(prenotazione)
        self.storage.salva(self.prenotazioni)

    def get_prenotazione_by_id(self, id):
        return next((p for p in self.prenotazioni if p.id == id), None)

    def rimuovi_prenotazione(self, id):
        self.prenotazioni = [p for p in self.prenotazioni if p.id != id]
        self.storage.salva(self.prenotazioni)

    def aggiorna_prenotazione(self, id, **kwargs):
        prenotazione = self.get_prenotazione_by_id(id)
        if prenotazione:
            for key, value in kwargs.items():
                setattr(prenotazione, key, value)
            self.storage.salva(self.prenotazioni)
            return True
        return False

    def get_tutte_prenotazioni(self):
        return self.prenotazioni

    def reload(self):
        """Ricarica la lista delle prenotazioni dallo storage."""
        self.prenotazioni = self.storage.carica()
