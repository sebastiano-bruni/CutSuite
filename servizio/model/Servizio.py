from dataclasses import dataclass

@dataclass
class Servizio:
    id: int
    nome: str
    descrizione: str
    prezzo: float
    durata_minuti: int