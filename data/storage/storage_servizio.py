import json
import os
from typing import List
from model.Servizio import Servizio

class StorageServizio:
    def __init__(self, filename: str = "data/files/servizi.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Servizio]:
        with open(self.filename, "r") as f:
            data = json.load(f)
        return [Servizio(**s) for s in data]

    def salva(self, servizi: List[Servizio]) -> None:
        with open(self.filename, "w") as f:
            json.dump([s.__dict__ for s in servizi], f, indent=4)

    def aggiungi(self, servizio: Servizio) -> None:
        servizi = self.carica()
        servizi.append(servizio)
        self.salva(servizi)

    def rimuovi(self, id_servizio: int) -> None:
        servizi = self.carica()
        servizi = [s for s in servizi if s.id != id_servizio]
        self.salva(servizi)