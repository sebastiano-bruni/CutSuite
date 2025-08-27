import json
import os
from typing import List
from model.Dipendente import Dipendente, Parrucchiere, Proprietario

class StorageDipendente:
    def __init__(self, filename: str = "data/files/dipendenti.json"):
        self.filename = filename
        # se non esiste il file, crealo vuoto
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Dipendente]:
        """Carica tutti i dipendenti dal file JSON, ricreando la classe corretta"""
        with open(self.filename, "r") as f:
            data = json.load(f)

        dipendenti = []
        for d in data:
            cls_name = d.pop("__class__", "Dipendente")  # recupera il tipo
            if cls_name == "Parrucchiere":
                dip = Parrucchiere(**d)
            elif cls_name == "Proprietario":
                dip = Proprietario(**d)
            else:
                dip = Dipendente(**d)
            dipendenti.append(dip)
        return dipendenti

    def salva(self, dipendenti: List[Dipendente]) -> None:
        """Salva tutti i dipendenti nel file JSON"""
        data = []
        for d in dipendenti:
            d_dict = d.__dict__.copy()
            d_dict["__class__"] = d.__class__.__name__  # aggiunge il tipo
            data.append(d_dict)
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def aggiungi(self, dipendente: Dipendente) -> None:
        """Aggiunge un dipendente al file"""
        dipendenti = self.carica()
        dipendenti.append(dipendente)
        self.salva(dipendenti)

    def rimuovi(self, id_dipendente: int) -> None:
        """Rimuove un dipendente per ID"""
        dipendenti = self.carica()
        dipendenti = [d for d in dipendenti if d.id != id_dipendente]
        self.salva(dipendenti)