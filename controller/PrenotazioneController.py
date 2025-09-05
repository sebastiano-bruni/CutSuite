from model.Prenotazione import Prenotazione
from data.storage.storage_prenotazione import StoragePrenotazione
from data.storage.storage_materiale import StorageMateriale   # 👈 aggiungi questa import
from datetime import datetime


class PrenotazioneController:
    def __init__(self):
        self.storage = StoragePrenotazione("data/files/prenotazioni.json")
        self.storage_materiali = StorageMateriale("data/files/materiali.json")  # 👈 inizializzazione mancante
        self.prenotazioni = self.storage.carica()

    def aggiungi_prenotazione(self, prenotazione: Prenotazione):
        servizio = prenotazione.servizio
        materiale = servizio.materiale
        quantita = servizio.quantita_materiale

        # 1. Controllo disponibilità
        if materiale and materiale.quantita < quantita:
            raise ValueError(
                f"Materiale insufficiente: {materiale.nome} "
                f"(richiesto {quantita}, disponibile {materiale.quantita})"
            )

        # 2. Decremento il materiale (in memoria)
        if materiale:
            materiale.usa(quantita)

            # aggiorno lo stato dei materiali nel JSON
            materiali_attuali = self.storage_materiali.carica()
            for m in materiali_attuali:
                if m.id == materiale.id:
                    m.quantita = materiale.quantita
                    break
            self.storage_materiali.salva(materiali_attuali)

        # 3. Salvo la prenotazione
        self.prenotazioni.append(prenotazione)
        self.storage.salva(self.prenotazioni)
    def get_prenotazione_by_id(self, id):
        return next((p for p in self.prenotazioni if p.id == id), None)

    def rimuovi_prenotazione(self, id):
        prenotazione = self.get_prenotazione_by_id(id)
        if prenotazione:
            servizio = prenotazione.servizio
            materiale = servizio.materiale
            quantita = servizio.quantita_materiale

            # 1. Ripristino materiale usato
            if materiale:
                materiali_attuali = self.storage_materiali.carica()
                for m in materiali_attuali:
                    if m.id == materiale.id:
                        m.quantita += quantita
                        break
                self.storage_materiali.salva(materiali_attuali)

            # 2. Rimuovo prenotazione
            self.prenotazioni = [p for p in self.prenotazioni if p.id != id]
            self.storage.salva(self.prenotazioni)
            return True
        return False

    def aggiorna_prenotazione(self, id, **kwargs):
        prenotazione = self.get_prenotazione_by_id(id)
        if prenotazione:
            for key, value in kwargs.items():
                setattr(prenotazione, key, value)
            self.storage.salva(self.prenotazioni)
            return True
        return False

    def get_tutte_prenotazioni(self):
        return self.prenotazioni

    def reload(self):
        """Ricarica la lista delle prenotazioni dallo storage."""
        self.prenotazioni = self.storage.carica()
