from model.Servizio import Servizio
from data.storage.storage_servizio import StorageServizio

class ServizioController:
    def __init__(self):
        self.storage = StorageServizio("data/files/servizi.json")
        self.servizi = self.storage.carica()

    def aggiungi_servizio(self, servizio: Servizio):
        self.servizi.append(servizio)
        self.storage.salva(self.servizi)

    def get_servizio_by_id(self, id):
        return next((s for s in self.servizi if s.id == id), None)

    def rimuovi_servizio(self, id):
        self.servizi = [s for s in self.servizi if s.id != id]
        self.storage.salva(self.servizi)

    def aggiorna_servizio(self, id, **kwargs):
        servizio = self.get_servizio_by_id(id)
        if servizio:
            for key, value in kwargs.items():
                setattr(servizio, key, value)
            self.storage.salva(self.servizi)
            return True
        return False

    def get_tutti_servizi(self):
        return self.servizi

    def ricerca_servizio_per_nome(self, nome: str):
        nome = nome.lower()
        return [s for s in self.servizi if nome in s.nome.lower()]

    def servizi_ordinati_per_prezzo(self):
        return sorted(self.servizi, key=lambda s: s.prezzo)

    def servizi_ordinati_per_durata(self):
        return sorted(self.servizi, key=lambda s: s.durata_minuti)