from model.Ricevuta import Ricevuta
from data.storage.storage_ricevuta import StorageRicevuta

class RicevutaController:
    def __init__(self):
        self.storage = StorageRicevuta("data/files/ricevute.json")         # istanza dello storage
        self.ricevute = self.storage.carica()    # carica tutte le ricevute dal file

    def aggiungi_ricevuta(self, ricevuta: Ricevuta):
        self.ricevute.append(ricevuta)
        self.storage.salva(self.ricevute)       # salva subito nel file

    def get_ricevuta_by_id(self, id):
        return next((r for r in self.ricevute if r.id == id), None)

    def rimuovi_ricevuta(self, id):
        self.ricevute = [r for r in self.ricevute if r.id != id]
        self.storage.salva(self.ricevute)

    def aggiorna_ricevuta(self, id, **kwargs):
        ricevuta = self.get_ricevuta_by_id(id)
        if ricevuta:
            for key, value in kwargs.items():
                setattr(ricevuta, key, value)
            self.storage.salva(self.ricevute)
            return True
        return False

    def get_tutte_ricevute(self):
        return self.ricevute

    def stampa_ricevuta(self, id):
        ricevuta = self.get_ricevuta_by_id(id)
        if ricevuta:
            return ricevuta.genera_testo()
        return f"Nessuna ricevuta trovata con id {id}"