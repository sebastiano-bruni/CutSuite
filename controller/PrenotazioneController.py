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

    def ricerca_prenotazioni_per_cliente(self, cliente_id: int):
        return [p for p in self.prenotazioni if p.cliente.id == cliente_id]

    def ricerca_prenotazioni_per_data(self, data: datetime):
        return [p for p in self.prenotazioni if p.data.date() == data.date()]

    def ricerca_prenotazioni_per_dipendente(self, dipendente_id: int):
        return [p for p in self.prenotazioni if p.dipendente.id == dipendente_id]

    def aggiorna_stato_pagamento(self, id: int, stato: str):
        prenotazione = self.get_prenotazione_by_id(id)
        if prenotazione:
            prenotazione.stato = stato
            self.storage.salva(self.prenotazioni)
            return True
        return False

    def prenotazioni_future(self):
        now = datetime.now()
        return [p for p in self.prenotazioni if datetime.combine(p.data.date(), p.ora.time()) > now]

    def visualizza_prenotazioni_giornaliere(self):
        today = datetime.now().date()
        return [p for p in self.prenotazioni if p.data.date() == today]