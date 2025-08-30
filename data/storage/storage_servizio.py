import json
import os
from typing import List, Optional
from model.Servizio import Servizio
from model.Materiale import Materiale
from controller.MaterialeController import MaterialeController


class StorageServizio:
    def __init__(self, filename: str = "data/files/servizi.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Servizio]:
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []

        servizi = []
        materiale_controller = MaterialeController()

        for s in data:
            servizio_id = s.pop("id", None)

            # Carico l'oggetto Materiale se l'ID è presente
            materiale_id = s.pop("materiale_id", None)
            materiale = materiale_controller.get_materiale_by_id(materiale_id) if materiale_id else None

            servizio = Servizio(
                nome=s["nome"],
                descrizione=s["descrizione"],
                prezzo=s["prezzo"],
                durata_minuti=s["durata_minuti"],
                materiale=materiale,
                quantita_materiale=s["quantita_materiale"]
            )

            if servizio_id is not None:
                servizio.id = servizio_id

            servizi.append(servizio)

        if servizi:
            Servizio._next_id = max(s.id for s in servizi) + 1

        return servizi

    def salva(self, servizi: List[Servizio]) -> None:
        def custom_encoder(obj):
            if isinstance(obj, Materiale):
                return {"materiale_id": obj.id}
            # Se è un oggetto Servizio, gestisco la serializzazione manualmente
            if isinstance(obj, Servizio):
                d = obj.__dict__.copy()
                d['materiale_id'] = d['materiale'].id if d['materiale'] else None
                del d['materiale']  # Rimuovo l'oggetto Materiale prima di serializzare
                return d
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

        with open(self.filename, "w") as f:
            # Uso la funzione di default per la serializzazione
            json.dump([custom_encoder(s) for s in servizi], f, indent=4)

    def aggiungi(self, servizio: Servizio) -> None:
        servizi = self.carica()
        servizi.append(servizio)
        self.salva(servizi)

    def rimuovi(self, id_servizio: int) -> None:
        servizi = self.carica()
        servizi = [s for s in servizi if s.id != id_servizio]
        self.salva(servizi)
