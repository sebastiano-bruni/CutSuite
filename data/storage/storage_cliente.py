import json
import os
from typing import List
from model.Cliente import Cliente  # importa la tua dataclass Cliente

class StorageCliente:
    def __init__(self, filename: str = "data/files/clienti.json"):
        self.filename = filename
        # se non esiste il file, crealo vuoto
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def carica(self) -> List[Cliente]:
        """Carica tutti i clienti dal file JSON"""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []

        clienti = []
        for c in data:
            cliente = Cliente(
                nome=c["nome"],
                cognome=c["cognome"],
                cf=c["cf"],
                email=c["email"],
                telefono=c["telefono"],
                numVisite=c.get("numVisite", 0),
                statoFedelta=(c.get("statoFedelta") == "attivo")
            )
            cliente.id = c["id"]  # assegna manualmente l'id salvato
            clienti.append(cliente)

        # 🔥 aggiorno anche il contatore degli id
        if clienti:
            Cliente._next_id = max(c.id for c in clienti) + 1

        return clienti


    def salva(self, clienti: List[Cliente]) -> None:
        """Salva tutti i clienti nel file JSON"""
        with open(self.filename, "w") as f:
            json.dump([c.__dict__ for c in clienti], f, indent=4)

    def aggiungi(self, cliente: Cliente) -> None:
        """Aggiunge un cliente al file"""
        clienti = self.carica()
        clienti.append(cliente)
        self.salva(clienti)

    def rimuovi(self, id_cliente: int) -> None:
        """Rimuove un cliente per ID"""
        clienti = self.carica()
        clienti = [c for c in clienti if c.id != id_cliente]
        self.salva(clienti)