from cliente.model.Cliente import Cliente

class ClienteController:
    def __init__(self):
        self.clienti = []

    def aggiungi_cliente(self, cliente: Cliente):
        self.clienti.append(cliente)

    def get_cliente_by_id(self, id):
        return next((c for c in self.clienti if c.id == id), None)

    def rimuovi_cliente(self, id):
        self.clienti = [c for c in self.clienti if c.id != id]

    def aggiorna_cliente(self, id, **kwargs):
        cliente = self.get_cliente_by_id(id)
        if cliente:
            for key, value in kwargs.items():
                setattr(cliente, key, value)
            return True
        return False

    def get_tutti_clienti(self):
        return self.clienti