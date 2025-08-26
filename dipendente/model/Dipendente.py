from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Dipendente:
    id: int
    nome: str
    cognome: str
    email: str
    telefono: str
    username: str
    password: str


@dataclass
class Parrucchiere(Dipendente):
    stipendio: int
    ruolo: str  # es: "Parrucchiere" o "Proprietario"


@dataclass
class Proprietario(Dipendente):
    permessi: int = 1  # esempio: livello di permessi