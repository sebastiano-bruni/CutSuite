from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Cliente:
    id: int = field(init=False)
    nome: str
    cognome: str
    cf: str
    email: str
    telefono: str
    numVisite: int = 0
    statoFedelta: str = "inattivo"  # semplice stringa

    _next_id: ClassVar[int] = 1  # variabile di classe

    def __post_init__(self):
        self.id = Cliente._next_id
        Cliente._next_id += 1

    @property
    def nome_completo(self) -> str:
        return f"{self.nome} {self.cognome}"

    def incrementa_visita(self):
        self.numVisite += 1
        if self.numVisite >= 10:
            self.statoFedelta = "attivo"