from model.Cliente import Cliente
from data.storage.storage_cliente import StorageCliente

class ClienteController:
    def __init__(self):
        self.storage = StorageCliente("data/files/clienti.json")
        self.clienti = self.storage.carica()

    def crea_cliente(self, cliente: Cliente):
        self.clienti.append(cliente)
        self.storage.salva(self.clienti)

    def get_cliente_by_id(self, id):
        return next((c for c in self.clienti if c.id == id), None)

    def rimuovi_cliente(self, id):
        self.clienti = [c for c in self.clienti if c.id != id]
        self.storage.salva(self.clienti)

    def aggiorna_cliente(self, id, **kwargs):
        cliente = self.get_cliente_by_id(id)
        if cliente:
            for key, value in kwargs.items():
                setattr(cliente, key, value)
            self.storage.salva(self.clienti)
            return True
        return False

    def get_tutti_clienti(self):
        return self.clienti

    def reload(self):
        self.clienti = self.storage.carica()

    def ricerca_cliente_per_nome(self, nome: str):
        nome = nome.lower()
        return [c for c in self.clienti if nome in c.nome.lower()]