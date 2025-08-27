from dataclasses import dataclass, field
from datetime import datetime

from model import Prenotazione


@dataclass
class Ricevuta:
    id: int = field(init=False)
    prenotazione: Prenotazione
    importo_totale: float
    dettagli: str
    data_emissione: datetime = field(default_factory=datetime.now)

    _next_id = 1  # variabile di classe (non nei campi)

    def __post_init__(self):
        self.id = Ricevuta._next_id
        Ricevuta._next_id += 1

    def genera_testo(self) -> str:
        return (f"Ricevuta #{self.id}\n"
                f"Cliente: {self.prenotazione.cliente.nome_completo}\n"
                f"Servizio: {self.prenotazione.servizio.nome}\n"
                f"Dettagli: {self.dettagli}\n"
                f"Totale: {self.importo_totale:.2f} €\n"
                f"Data: {self.data_emissione.strftime('%d/%m/%Y %H:%M')}")