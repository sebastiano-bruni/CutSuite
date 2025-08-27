import json
import os
from typing import List
from model.Materiale import Materiale  # importa la tua dataclass Materiale

class StorageMateriale:
    def __init__(self, filename: str = "data/files/materiali.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Materiale]:
        """Carica tutti i materiali dal file JSON"""
        with open(self.filename, "r") as f:
            data = json.load(f)
        return [Materiale(**m) for m in data]

    def salva(self, materiali: List[Materiale]) -> None:
        """Salva tutti i materiali nel file JSON"""
        with open(self.filename, "w") as f:
            json.dump([m.__dict__ for m in materiali], f, indent=4)

    def aggiungi(self, materiale: Materiale) -> None:
        materiali = self.carica()
        materiali.append(materiale)
        self.salva(materiali)

    def rimuovi(self, id_materiale: int) -> None:
        materiali = self.carica()
        materiali = [m for m in materiali if m.id != id_materiale]
        self.salva(materiali)