from model.Ricevuta import Ricevuta
from data.storage.storage_ricevuta import StorageRicevuta
from datetime import datetime
from typing import List


class RicevutaController:
    def __init__(self):
        self.storage = StorageRicevuta("data/files/ricevute.json")
        self.ricevute = self.storage.carica()

    def aggiungi_ricevuta(self, ricevuta: Ricevuta):
        self.ricevute.append(ricevuta)
        self.storage.salva(self.ricevute)

    def get_ricevuta_by_id(self, id):
        return next((r for r in self.ricevute if r.id == id), None)

    def rimuovi_ricevuta(self, id):
        self.ricevute = [r for r in self.ricevute if r.id != id]
        self.storage.salva(self.ricevute)

    def get_tutte_ricevute(self) -> List[Ricevuta]:
        return self.ricevute

    def reload(self):
        """Ricarica la lista delle ricevute dallo storage."""
        self.ricevute = self.storage.carica()
