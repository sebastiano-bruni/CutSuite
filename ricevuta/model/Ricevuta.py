from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Ricevuta:
    id: int
    prenotazione: Prenotazione
    importo_totale: float
    data_emissione: datetime = field(default_factory=datetime.now)
    dettagli: str

    def genera_testo(self) -> str:
        return (f"Ricevuta #{self.id}\n"
                f"Cliente: {self.prenotazione.cliente.nome_completo}\n"
                f"Servizio: {self.prenotazione.servizio.nome}\n"
                f"Dettagli: {self.dettagli}\n"
                f"Totale: {self.importo_totale:.2f} €\n"
                f"Data: {self.data_emissione.strftime('%d/%m/%Y %H:%M')}")