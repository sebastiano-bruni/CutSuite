from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Optional

@dataclass
class Dipendente:
    id: int = field(init=False)
    nome: str
    cognome: str
    cf: str  # Aggiunto il codice fiscale come richiesto dai mockup
    email: str
    telefono: str
    username: str
    password: str

    _next_id: ClassVar[int] = 1

    def __post_init__(self):
        # Questo metodo viene chiamato dopo __init__
        # Assicura che l'id sia assegnato solo se non esiste già (es. dopo il caricamento da file)
        if not hasattr(self, 'id'):
            self.id = Dipendente._next_id
            Dipendente._next_id += 1


@dataclass
class Parrucchiere(Dipendente):
    stipendio: int
    ruolo: str = "Parrucchiere"


@dataclass
class Proprietario(Dipendente):
    permessi: int = 1
    ruolo: str = "Proprietario"
