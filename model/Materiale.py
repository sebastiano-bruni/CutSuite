from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Optional

@dataclass
class Materiale:
    id: int = field(init=False)
    nome: str
    categoria: str
    prezzo: float
    quantita: int
    soglia_scorte: int

    _next_id: ClassVar[int] = 1

    def __post_init__(self):
        self.id = Materiale._next_id
        Materiale._next_id += 1

    def usa(self, qta: int):
        """Riduce la quantità disponibile"""
        if qta > self.quantita:
            raise ValueError("Quantità richiesta superiore alla disponibilità")
        self.quantita -= qta
