from materiale.model.Materiale import Materiale

class MaterialeController:
    def __init__(self):
        self.materiali = []

    def aggiungi_materiale(self, materiale: Materiale):
        self.materiali.append(materiale)

    def get_materiale_by_id(self, id):
        return next((m for m in self.materiali if m.id == id), None)

    def rimuovi_materiale(self, id):
        self.materiali = [m for m in self.materiali if m.id != id]

    def aggiorna_materiale(self, id, **kwargs):
        materiale = self.get_materiale_by_id(id)
        if materiale:
            for key, value in kwargs.items():
                setattr(materiale, key, value)
            return True
        return False

    def get_tutti_materiali(self):
        return self.materiali