from controller.ClienteController import ClienteController
from model.Promozione import Promozione
from data.storage.storage_promozione import StoragePromozione
from controller.PrenotazioneController import PrenotazioneController

class PromozioneController:
    def __init__(self):
        self.storage = StoragePromozione("data/files/promozioni.json")
        self.promozioni = self.storage.carica()

    def aggiungi_promozione(self, promozione: Promozione):
        self.promozioni.append(promozione)
        self.storage.salva(self.promozioni)

    def get_promozione_by_id(self, id):
        return next((p for p in self.promozioni if p.id == id), None)

    def rimuovi_promozione(self, id):
        self.promozioni = [p for p in self.promozioni if p.id != id]
        self.storage.salva(self.promozioni)

    def aggiorna_promozione(self, id, **kwargs):
        promozione = self.get_promozione_by_id(id)
        if promozione:
            for key, value in kwargs.items():
                setattr(promozione, key, value)
            self.storage.salva(self.promozioni)
            return True
        return False

    def get_tutte_promozioni(self):
        return self.promozioni

    def ricerca_promozione_per_nome(self, nome: str):
        nome = nome.lower()
        return [p for p in self.promozioni if nome in p.nome.lower()]

    def reload(self):

        self.promozioni = self.storage.carica()

    def calcola_sconto_cliente(self, promozioni: list, cliente_id: str) -> float:

        #prenotazione_controller = PrenotazioneController()
        #numero_prenotazioni = prenotazione_controller.get_numero_prenotazioni_pagate(cliente_id)
        cliente_controller = ClienteController()
        numero_prenotazioni = cliente_controller.get_cliente_by_id(cliente_id).numVisite

        sconto_massimo = 0.0

        for promo in promozioni:
            if promo.valida() and numero_prenotazioni >= promo.soglia_promozione:
                sconto = promo.sconto_percentuale / 100
                if sconto > sconto_massimo:
                    sconto_massimo = sconto

        return sconto_massimo
