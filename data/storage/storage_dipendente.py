import json
import os
from typing import List
from model.Dipendente import Dipendente, Parrucchiere, Proprietario


class StorageDipendente:
    def __init__(self, filename: str = "data/files/dipendenti.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Dipendente]:
        """Carica tutti i dipendenti dal file JSON, ricreando la classe corretta"""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []

        dipendenti = []
        for d in data:
            cls_name = d.pop("__class__", "Dipendente")
            dip_id = d.pop("id", None)

            # Recupera tutti i campi necessari per il costruttore della classe base
            kwargs = {
                "nome": d.get("nome"),
                "cognome": d.get("cognome"),
                "cf": d.get("cf"),
                "email": d.get("email"),
                "telefono": d.get("telefono"),
                "username": d.get("username"),
                "password": d.get("password")
            }

            dip = None
            if cls_name == "Parrucchiere":
                kwargs["stipendio"] = d.get("stipendio")
                kwargs["ruolo"] = d.get("ruolo", "Parrucchiere")
                dip = Parrucchiere(**kwargs)
            elif cls_name == "Proprietario":
                kwargs["permessi"] = d.get("permessi")
                kwargs["ruolo"] = d.get("ruolo", "Proprietario")
                dip = Proprietario(**kwargs)
            else:
                dip = Dipendente(**kwargs)

            if dip and dip_id is not None:
                dip.id = dip_id
                dipendenti.append(dip)

        if dipendenti:
            Dipendente._next_id = max(d.id for d in dipendenti) + 1

        return dipendenti

    def salva(self, dipendenti: List[Dipendente]) -> None:
        """Salva tutti i dipendenti nel file JSON"""
        data = []
        for d in dipendenti:
            d_dict = d.__dict__.copy()
            d_dict["__class__"] = d.__class__.__name__
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
