from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
@dataclass
class Materiale:
    id: int
    nome: str
    categoria: str
    quantita: int

    def usa(self, qta: int):
        """Riduce la quantità disponibile"""
        if qta > self.quantita:
            raise ValueError("Quantità richiesta superiore alla disponibilità")
        self.quantita -= qta