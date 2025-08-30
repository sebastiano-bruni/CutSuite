import json
import os
from typing import List
from model.Promozione import Promozione
from datetime import datetime


class StoragePromozione:
    def __init__(self, filename: str = "data/files/promozioni.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Promozione]:
        """Carica tutte le promozioni dal file JSON"""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        promozioni = []
        for p in data:
            promo_id = p.pop("id", None)

            # Converte le stringhe in oggetti datetime
            data_inizio_str = p.pop("data_inizio")
            data_fine_str = p.pop("data_fine")

            promozione = Promozione(
                nome=p["nome"],
                descrizione=p["descrizione"],
                sconto_percentuale=p["sconto_percentuale"],
                data_inizio=datetime.fromisoformat(data_inizio_str),
                data_fine=datetime.fromisoformat(data_fine_str),
                soglia_promozione=p["soglia_promozione"]
            )

            if promo_id is not None:
                promozione.id = promo_id
            promozioni.append(promozione)

        if promozioni:
            Promozione._next_id = max(p.id for p in promozioni) + 1

        return promozioni

    def salva(self, promozioni: List[Promozione]) -> None:
        """Salva tutte le promozioni nel file JSON"""
        data = []
        for p in promozioni:
            p_dict = p.__dict__.copy()
            # Converte gli oggetti datetime in stringhe ISO per la serializzazione
            p_dict['data_inizio'] = p_dict['data_inizio'].isoformat()
            p_dict['data_fine'] = p_dict['data_fine'].isoformat()
            data.append(p_dict)

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def aggiungi(self, promozione: Promozione) -> None:
        promozioni = self.carica()
        promozioni.append(promozione)
        self.salva(promozioni)

    def rimuovi(self, id_promozione: int) -> None:
        promozioni = self.carica()
        promozioni = [p for p in promozioni if p.id != id_promozione]
        self.salva(promozioni)
