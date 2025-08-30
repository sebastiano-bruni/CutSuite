from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Optional
from model.Cliente import Cliente
from model.Servizio import Servizio
from model.Dipendente import Dipendente

@dataclass
class Prenotazione:
    id: int = field(init=False)
    cliente: Cliente
    servizio: Servizio
    dipendente: Dipendente
    data: datetime
    ora: datetime
    durata_minuti: int
    prezzo: float
    stato: str
    email_cliente: str
    note: str

    _next_id: ClassVar[int] = 1

    def __post_init__(self):
        if not hasattr(self, 'id'):
            self.id = Prenotazione._next_id
            Prenotazione._next_id += 1
