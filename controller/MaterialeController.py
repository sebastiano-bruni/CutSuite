from model.Materiale import Materiale
from data.storage.storage_materiale import StorageMateriale

class MaterialeController:
    def __init__(self):
        self.storage = StorageMateriale("data/files/materiali.json")
        self.materiali = self.storage.carica()

    def aggiungi_materiale(self, materiale: Materiale):
        self.materiali.append(materiale)
        self.storage.salva(self.materiali)

    def get_materiale_by_id(self, id):
        return next((m for m in self.materiali if m.id == id), None)

    def rimuovi_materiale(self, id):
        self.materiali = [m for m in self.materiali if m.id != id]
        self.storage.salva(self.materiali)

    def aggiorna_materiale(self, id, **kwargs):
        materiale = self.get_materiale_by_id(id)
        if materiale:
            for key, value in kwargs.items():
                setattr(materiale, key, value)
            self.storage.salva(self.materiali)
            return True
        return False

    def get_tutti_materiali(self):
        return self.materiali

    def ricerca_materiale_per_nome(self, nome: str):
        nome = nome.lower()
        return [m for m in self.materiali if nome in m.nome.lower()]

    def ricerca_materiale_per_categoria(self, categoria: str):
        categoria = categoria.lower()
        return [m for m in self.materiali if categoria in m.categoria.lower()]

    def aumenta_quantita(self, id, qta: int):
        materiale = self.get_materiale_by_id(id)
        if materiale:
            materiale.quantita += qta
            self.storage.salva(self.materiali)
            return True
        return False

    def diminuisci_quantita(self, id, qta: int):
        materiale = self.get_materiale_by_id(id)
        if materiale and materiale.quantita >= qta:
            materiale.quantita -= qta
            self.storage.salva(self.materiali)
            return True
        return False