import json
import os
from typing import List
from model.Materiale import Materiale


class StorageMateriale:
    def __init__(self, filename: str = "data/files/materiali.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Materiale]:
        """Carica tutti i materiali dal file JSON"""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []

        materiali = []
        for m in data:

            m_copy = m.copy()

            materiale_id = m_copy.pop("id", None)

            materiale = Materiale(**m_copy)

            if materiale_id is not None:
                materiale.id = materiale_id

            materiali.append(materiale)

        if materiali:
            Materiale._next_id = max(m.id for m in materiali) + 1

        return materiali

    def salva(self, materiali: List[Materiale]) -> None:
        """Salva tutti i materiali nel file JSON"""
        with open(self.filename, "w") as f:
            json.dump([m.__dict__ for m in materiali], f, indent=4)

    def aggiungi(self, materiale: Materiale) -> None:
        """Aggiunge un materiale al file"""
        materiali = self.carica()
        materiali.append(materiale)
        self.salva(materiali)

    def rimuovi(self, id_materiale: int) -> None:
        """Rimuove un materiale per ID"""
        materiali = self.carica()
        materiali = [m for m in materiali if m.id != id_materiale]
        self.salva(materiali)
