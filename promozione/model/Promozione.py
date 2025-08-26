from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Promozione:
    id: int
    nome: str
    descrizione: str
    sconto_percentuale: float
    data_inizio: datetime
    data_fine: datetime
    soglia_promozione: int

    def valida(self) -> bool:
        """Controlla se la promozione è attiva"""
        oggi = datetime.now()
        return self.data_inizio <= oggi <= self.data_fine
