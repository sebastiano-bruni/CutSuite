import json
import os
from typing import List
from model.Ricevuta import Ricevuta

class StorageRicevuta:
    def __init__(self, filename: str = "data/files/ricevute.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Ricevuta]:
        with open(self.filename, "r") as f:
            data = json.load(f)
        return [Ricevuta(**r) for r in data]

    def salva(self, ricevute: List[Ricevuta]) -> None:
        with open(self.filename, "w") as f:
            json.dump([r.__dict__ for r in ricevute], f, indent=4)

    def aggiungi(self, ricevuta: Ricevuta) -> None:
        ricevute = self.carica()
        ricevute.append(ricevuta)
        self.salva(ricevute)

    def rimuovi(self, id_ricevuta: int) -> None:
        ricevute = self.carica()
        ricevute = [r for r in ricevute if r.id != id_ricevuta]
        self.salva(ricevute)