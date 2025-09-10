from model.Ricevuta import Ricevuta
from data.storage.storage_ricevuta import StorageRicevuta
from datetime import datetime
from typing import List
from controller.PrenotazioneController import PrenotazioneController
from controller.PromozioneController import PromozioneController


class RicevutaController:
    def __init__(self):
        self.storage = StorageRicevuta("data/files/ricevute.json")
        self.ricevute = self.storage.carica()
        self.prenotazione_controller = PrenotazioneController()
        self.promozione_controller = PromozioneController()

    def aggiungi_ricevuta(self, ricevuta: Ricevuta):

        cliente_id = ricevuta.prenotazione.cliente.id
        importo = ricevuta.importo_totale

        sconto = self.promozione_controller.calcola_sconto_cliente(cliente_id)
        importo_finale = importo * (1 - sconto)

        ricevuta.sconto_applicato = sconto
        ricevuta.importo_finale = importo_finale

        self.ricevute.append(ricevuta)
        self.storage.salva(self.ricevute)

        prenotazione = self.prenotazione_controller.get_prenotazione_by_id(ricevuta.prenotazione.id)
        if prenotazione:
            prenotazione.stato = "pagata"
            self.prenotazione_controller.storage.salva(self.prenotazione_controller.prenotazioni)

    def get_ricevuta_by_id(self, id):
        return next((r for r in self.ricevute if r.id == id), None)

    def rimuovi_ricevuta(self, id):
        self.ricevute = [r for r in self.ricevute if r.id != id]
        self.storage.salva(self.ricevute)

    def get_tutte_ricevute(self) -> List[Ricevuta]:
        return self.ricevute

    def reload(self):
        """Ricarica la lista delle ricevute dallo storage."""
        self.ricevute = self.storage.carica()
