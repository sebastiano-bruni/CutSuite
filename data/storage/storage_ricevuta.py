import json
import os
from typing import List
from model.Ricevuta import Ricevuta
from model.Prenotazione import Prenotazione
from datetime import datetime
from controller.PrenotazioneController import PrenotazioneController


class StorageRicevuta:
    def __init__(self, filename: str = "data/files/ricevute.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Ricevuta]:
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        ricevute = []
        prenotazione_controller = PrenotazioneController()

        for r in data:
            ricevuta_id = r.pop("id", None)

            prenotazione = prenotazione_controller.get_prenotazione_by_id(r.pop("prenotazione_id"))
            data_emissione_str = r.pop("data_emissione")

            ricevuta = Ricevuta(
                prenotazione=prenotazione,
                importo_totale=r["importo_totale"],
                data_emissione=datetime.fromisoformat(data_emissione_str),
                dettagli=r.get("dettagli", None)
            )

            if ricevuta_id is not None:
                ricevuta.id = ricevuta_id
            ricevute.append(ricevuta)

        if ricevute:
            Ricevuta._next_id = max(r.id for r in ricevute) + 1

        return ricevute

    def salva(self, ricevute: List[Ricevuta]) -> None:
        data = []
        for r in ricevute:
            r_dict = r.__dict__.copy()

            r_dict['prenotazione_id'] = r.prenotazione.id if r.prenotazione else None
            del r_dict['prenotazione']

            r_dict['data_emissione'] = r_dict['data_emissione'].isoformat()

            data.append(r_dict)

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def aggiungi(self, ricevuta: Ricevuta) -> None:
        ricevute = self.carica()
        ricevute.append(ricevuta)
        self.salva(ricevute)
