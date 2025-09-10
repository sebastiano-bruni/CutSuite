import json
import os
from typing import List
from model.Ricevuta import Ricevuta
from datetime import datetime
from controller.PrenotazioneController import PrenotazioneController


class StorageRicevuta:
    def __init__(self, filename: str = "data/files/ricevute.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def carica(self) -> List[Ricevuta]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        ricevute = []
        prenotazione_controller = PrenotazioneController()

        for r in data:
            ricevuta_id = r.get("id")
            prenotazione = prenotazione_controller.get_prenotazione_by_id(r.get("prenotazione_id"))
            data_emissione = datetime.fromisoformat(r["data_emissione"])

            ricevuta = Ricevuta(
                prenotazione=prenotazione,
                importo_totale=r["importo_totale"],
                dettagli=r.get("dettagli", ""),
                sconto_applicato=r.get("sconto_applicato", 0.0),
                data_emissione=data_emissione
            )

            # Forzo ID se salvato
            if ricevuta_id is not None:
                ricevuta.id = ricevuta_id

            ricevute.append(ricevuta)

        # Aggiorno _next_id
        if ricevute:
            Ricevuta._next_id = max(r.id for r in ricevute) + 1

        return ricevute

    def salva(self, ricevute: List[Ricevuta]) -> None:
        data = []
        for r in ricevute:
            r_dict = {
                "id": r.id,
                "prenotazione_id": r.prenotazione.id if r.prenotazione else None,
                "importo_totale": r.importo_totale,
                "sconto_applicato": r.sconto_applicato,
                "importo_finale": r.importo_finale,
                "dettagli": r.dettagli,
                "data_emissione": r.data_emissione.isoformat()
            }
            data.append(r_dict)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def aggiungi(self, ricevuta: Ricevuta) -> None:
        ricevute = self.carica()
        ricevute.append(ricevuta)
        self.salva(ricevute)