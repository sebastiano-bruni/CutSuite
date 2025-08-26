from servizio.model.Servizio import Servizio

class ServizioController:
    def __init__(self):
        self.servizi = []

    def aggiungi_servizio(self, servizio: Servizio):
        self.servizi.append(servizio)

    def get_servizio_by_id(self, id):
        return next((s for s in self.servizi if s.id == id), None)

    def rimuovi_servizio(self, id):
        self.servizi = [s for s in self.servizi if s.id != id]

    def aggiorna_servizio(self, id, **kwargs):
        servizio = self.get_servizio_by_id(id)
        if servizio:
            for key, value in kwargs.items():
                setattr(servizio, key, value)
            return True
        return False

    def get_tutti_servizi(self):
        return self.servizi