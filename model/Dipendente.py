from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Dipendente:
    id: int = field(init=False)
    nome: str
    cognome: str
    email: str
    telefono: str
    username: str
    password: str

    _next_id = 1

    def __post_init__(self):
        self.id = Dipendente._next_id
        Dipendente._next_id += 1


@dataclass
class Parrucchiere(Dipendente):
    stipendio: int
    ruolo: str  # es: "Parrucchiere" o "Proprietario"


@dataclass
class Proprietario(Dipendente):
    permessi: int = 1  # esempio: livello di permessi