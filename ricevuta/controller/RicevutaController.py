from ricevuta.model.Ricevuta import Ricevuta

class RicevutaController:
    def __init__(self):
        self.ricevute = []

    def aggiungi_ricevuta(self, ricevuta: Ricevuta):
        self.ricevute.append(ricevuta)

    def get_ricevuta_by_id(self, id):
        return next((r for r in self.ricevute if r.id == id), None)

    def rimuovi_ricevuta(self, id):
        self.ricevute = [r for r in self.ricevute if r.id != id]

    def aggiorna_ricevuta(self, id, **kwargs):
        ricevuta = self.get_ricevuta_by_id(id)
        if ricevuta:
            for key, value in kwargs.items():
                setattr(ricevuta, key, value)
            return True
        return False

    def get_tutte_ricevute(self):
        return self.ricevute