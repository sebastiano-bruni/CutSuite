from dataclasses import dataclass

@dataclass
class Servizio:
    id: int = field(init=False)
    nome: str
    descrizione: str
    prezzo: float
    durata_minuti: int

    _next_id = 1

    def __post_init__(self):
        self.id = Servizio._next_id
        Servizio._next_id += 1