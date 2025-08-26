from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

class Cliente():

    @dataclass
    class Cliente:
        id: int
        nome: str
        cognome: str
        cf: str
        email: str
        telefono: str
        numVisite: int = 0
        statoFedelta: bool = False


        @property
        def nome_completo(self) -> str:
            return f"{self.nome} {self.cognome}"

        def incrementa_visita(self):
            self.numVisite += 1
            if self.numVisite >= 10:
                self.statoFedelta = True
