from model.Dipendente import Dipendente
from data.storage.storage_dipendente import StorageDipendente

class DipendenteController:
    def __init__(self):
        self.storage = StorageDipendente("data/files/dipendenti.json")
        self.dipendenti = self.storage.carica()

    def aggiungi_dipendente(self, dipendente: Dipendente):
        self.dipendenti.append(dipendente)
        self.storage.salva(self.dipendenti)

    def get_dipendente_by_id(self, id):
        return next((d for d in self.dipendenti if d.id == id), None)

    def rimuovi_dipendente(self, id):
        self.dipendenti = [d for d in self.dipendenti if d.id != id]
        self.storage.salva(self.dipendenti)

    def aggiorna_dipendente(self, id, **kwargs):
        dipendente = self.get_dipendente_by_id(id)
        if dipendente:
            for key, value in kwargs.items():
                setattr(dipendente, key, value)
            self.storage.salva(self.dipendenti)
            return True
        return False

    def get_tutti_dipendenti(self):
        return self.dipendenti

    def ricerca_dipendente_per_nome(self, nome: str):
        nome = nome.lower()
        return [d for d in self.dipendenti if nome in d.nome.lower()]

    def ricerca_dipendente_per_ruolo(self, ruolo: str):
        ruolo = ruolo.lower()
        return [d for d in self.dipendenti if hasattr(d, "ruolo") and d.ruolo.lower() == ruolo]

    def ricerca_dipendente_per_permessi(self, livello_permessi: int):
        return [d for d in self.dipendenti if hasattr(d, "permessi") and d.permessi == livello_permessi]