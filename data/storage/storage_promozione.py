import json
import os
from typing import List
from model.Promozione import Promozione

class StoragePromozione:
    def __init__(self, filename: str = "data/files/promozioni.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Promozione]:
        with open(self.filename, "r") as f:
            data = json.load(f)
        return [Promozione(**p) for p in data]

    def salva(self, promozioni: List[Promozione]) -> None:
        with open(self.filename, "w") as f:
            json.dump([p.__dict__ for p in promozioni], f, indent=4)

    def aggiungi(self, promozione: Promozione) -> None:
        promozioni = self.carica()
        promozioni.append(promozione)
        self.salva(promozioni)

    def rimuovi(self, id_promozione: int) -> None:
        promozioni = self.carica()
        promozioni = [p for p in promozioni if p.id != id_promozione]
        self.salva(promozioni)