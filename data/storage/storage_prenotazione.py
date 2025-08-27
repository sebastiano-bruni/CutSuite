import json
import os
from typing import List
from model.Prenotazione import Prenotazione

class StoragePrenotazione:
    def __init__(self, filename: str = "data/files/prenotazioni.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Prenotazione]:
        with open(self.filename, "r") as f:
            data = json.load(f)
        return [Prenotazione(**p) for p in data]

    def salva(self, prenotazioni: List[Prenotazione]) -> None:
        with open(self.filename, "w") as f:
            json.dump([p.__dict__ for p in prenotazioni], f, indent=4)

    def aggiungi(self, prenotazione: Prenotazione) -> None:
        prenotazioni = self.carica()
        prenotazioni.append(prenotazione)
        self.salva(prenotazioni)

    def rimuovi(self, id_prenotazione: int) -> None:
        prenotazioni = self.carica()
        prenotazioni = [p for p in prenotazioni if p.id != id_prenotazione]
        self.salva(prenotazioni)