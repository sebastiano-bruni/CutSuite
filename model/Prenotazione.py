from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from model import Cliente, Dipendente, Servizio


@dataclass
class Prenotazione:
    id: int = field(init=False)
    cliente: Cliente
    servizio: Servizio
    dipendente: Dipendente
    data: datetime
    ora: datetime
    durata_minuti: Optional[int] = None
    stato: str = "Non pagata"  # Non pagata, Pagata

    _next_id = 1  # variabile di classe (non nei campi)

    def __post_init__(self):
        self.id = Prenotazione._next_id
        Prenotazione._next_id += 1
        if self.durata_minuti is None:
            self.durata_minuti = self.servizio.durata_minuti