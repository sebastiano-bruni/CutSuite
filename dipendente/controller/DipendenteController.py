from dipendente.model.Dipendente import Dipendente

class DipendenteController:
    def __init__(self):
        self.dipendenti = []

    def aggiungi_dipendente(self, dipendente: Dipendente):
        self.dipendenti.append(dipendente)

    def get_dipendente_by_id(self, id):
        return next((d for d in self.dipendenti if d.id == id), None)

    def rimuovi_dipendente(self, id):
        self.dipendenti = [d for d in self.dipendenti if d.id != id]

    def aggiorna_dipendente(self, id, **kwargs):
        dipendente = self.get_dipendente_by_id(id)
        if dipendente:
            for key, value in kwargs.items():
                setattr(dipendente, key, value)
            return True
        return False

    def get_tutti_dipendenti(self):
        return self.dipendenti