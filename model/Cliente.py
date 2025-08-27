from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

class Cliente():

    @dataclass
    class Cliente:
        id: int = field(init=False)
        nome: str
        cognome: str
        cf: str
        email: str
        telefono: str
        numVisite: int = 0
        statoFedelta: bool = False

        _next_id = 1   #variabile di classe (non nei campi)

        def __post_init__(self):
            self.id = Cliente._next_id
            Cliente._next_id += 1


        @property
        def nome_completo(self) -> str:
            return f"{self.nome} {self.cognome}"

        def incrementa_visita(self):
            self.numVisite += 1
            if self.numVisite >= 10:
                self.statoFedelta = True
