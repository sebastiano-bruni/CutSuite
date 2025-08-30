import json
import os
from typing import List
from model.Prenotazione import Prenotazione
from model.Cliente import Cliente
from model.Servizio import Servizio
from model.Dipendente import Dipendente
from datetime import datetime

# Importa i controller necessari per la deserializzazione
from controller.ClienteController import ClienteController
from controller.ServizioController import ServizioController
from controller.DipendenteController import DipendenteController


class StoragePrenotazione:
    def __init__(self, filename: str = "data/files/prenotazioni.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Prenotazione]:
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        prenotazioni = []

        # Inizializza i controller per recuperare gli oggetti correlati
        cliente_controller = ClienteController()
        servizio_controller = ServizioController()
        dipendente_controller = DipendenteController()

        for p in data:
            prenotazione_id = p.pop("id", None)

            # Carica gli oggetti completi usando gli ID salvati
            cliente = cliente_controller.get_cliente_by_id(p.pop("cliente_id"))
            servizio = servizio_controller.get_servizio_by_id(p.pop("servizio_id"))
            dipendente = dipendente_controller.get_dipendente_by_id(p.pop("dipendente_id"))

            # Converte le stringhe ISO in oggetti datetime
            data_obj = datetime.fromisoformat(p.pop("data"))
            ora_obj = datetime.fromisoformat(p.pop("ora"))

            prenotazione = Prenotazione(
                cliente=cliente,
                servizio=servizio,
                dipendente=dipendente,
                data=data_obj,
                ora=ora_obj,
                durata_minuti=p["durata_minuti"],
                prezzo=p["prezzo"],
                stato=p["stato"],
                email_cliente=p["email_cliente"],
                note=p["note"]
            )

            if prenotazione_id is not None:
                prenotazione.id = prenotazione_id
            prenotazioni.append(prenotazione)

        if prenotazioni:
            Prenotazione._next_id = max(p.id for p in prenotazioni) + 1

        return prenotazioni

    def salva(self, prenotazioni: List[Prenotazione]) -> None:
        data = []
        for p in prenotazioni:
            p_dict = p.__dict__.copy()

            # Salva gli ID al posto degli oggetti
            p_dict['cliente_id'] = p.cliente.id if p.cliente else None
            p_dict['servizio_id'] = p.servizio.id if p.servizio else None
            p_dict['dipendente_id'] = p.dipendente.id if p.dipendente else None

            # Rimuove gli oggetti prima della serializzazione
            del p_dict['cliente']
            del p_dict['servizio']
            del p_dict['dipendente']

            # Converte gli oggetti datetime in stringhe ISO per la serializzazione
            p_dict['data'] = p_dict['data'].isoformat()
            p_dict['ora'] = p_dict['ora'].isoformat()

            data.append(p_dict)

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def aggiungi(self, prenotazione: Prenotazione) -> None:
        prenotazioni = self.carica()
        prenotazioni.append(prenotazione)
        self.salva(prenotazioni)

    def rimuovi(self, id_prenotazione: int) -> None:
        prenotazioni = self.carica()
        prenotazioni = [p for p in prenotazioni if p.id != id_prenotazione]
        self.salva(prenotazioni)
