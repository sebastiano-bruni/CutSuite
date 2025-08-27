from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
@dataclass
class Materiale:
    id: int = field(init=False)
    nome: str
    categoria: str
    quantita: int

    _next_id = 1

    def __post_init__(self):
        self.id = Materiale._next_id
        Materiale._next_id += 1

    def usa(self, qta: int):
        """Riduce la quantità disponibile"""
        if qta > self.quantita:
            raise ValueError("Quantità richiesta superiore alla disponibilità")
        self.quantita -= qta