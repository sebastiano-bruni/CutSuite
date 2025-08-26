from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from cliente.model import Cliente
from dipendente.model import Dipendente
from servizio.model import Servizio


@dataclass
class Prenotazione:
    id: int
    cliente: Cliente
    servizio: Servizio
    dipendente: Dipendente
    data: datetime
    ora: datetime
    durata_minuti: Optional[int] = None
    stato: str = "Non pagata"  # Non pagata, Pagata

    def __post_init__(self):
        if self.durata_minuti is None:
            self.durata_minuti = self.servizio.durata_minuti