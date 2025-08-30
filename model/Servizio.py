from dataclasses import dataclass, field
from typing import ClassVar, Optional
from model.Materiale import Materiale

@dataclass
class Servizio:
    id: int = field(init=False)
    nome: str
    descrizione: str
    prezzo: float
    durata_minuti: int
    materiale: Optional[Materiale] = None
    quantita_materiale: int = 0

    _next_id: ClassVar[int] = 1

    def __post_init__(self):
        if not hasattr(self, 'id'):
            self.id = Servizio._next_id
            Servizio._next_id += 1
