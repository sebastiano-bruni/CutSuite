from model.Prenotazione import Prenotazione
from data.storage.storage_prenotazione import StoragePrenotazione
from data.storage.storage_materiale import StorageMateriale
from datetime import datetime, timedelta


class PrenotazioneController:
    def __init__(self):
        self.storage = StoragePrenotazione("data/files/prenotazioni.json")
        self.storage_materiali = StorageMateriale("data/files/materiali.json")
        self.prenotazioni = self.storage.carica()

    # -------------------------------
    # UTIL
    # -------------------------------
    def _refresh(self):
        """Ricarica sempre dallo storage per evitare liste non aggiornate."""
        self.prenotazioni = self.storage.carica()

    # -------------------------------
    # Controllo disponibilità dipendente
    # -------------------------------
    def dipendente_disponibile(self, dipendente_id, data_inizio, durata_minuti):
        """
        Ritorna True se il dipendente è libero nell'intervallo [data_inizio, data_inizio+durata).
        Regola di overlap (consente attacco immediato a fine slot):
            overlap se: inizio_esistente < nuova_fine AND fine_esistente > nuova_inizio
        quindi NO overlap se: fine_esistente <= nuova_inizio OR inizio_esistente >= nuova_fine
        """
        # assicurati di avere dati freschi
        self._refresh()

        nuova_fine = data_inizio + timedelta(minutes=durata_minuti)

        for p in self.prenotazioni:
            if not hasattr(p, "dipendente") or p.dipendente is None:
                continue
            if p.dipendente.id != dipendente_id:
                continue

            inizio_esistente = p.ora                     # datetime
            fine_esistente = p.ora + timedelta(minutes=p.durata_minuti)

            # c'è sovrapposizione?
            if inizio_esistente < nuova_fine and fine_esistente > data_inizio:
                return False

        return True

    # -------------------------------
    # Lista dipendenti disponibili per un orario
    # -------------------------------
    def dipendenti_disponibili(self, lista_dipendenti, data_inizio, durata_minuti):
        # dati freschi prima di calcolare
        self._refresh()

        disponibili = []
        for d in lista_dipendenti:
            if self.dipendente_disponibile(d.id, data_inizio, durata_minuti):
                disponibili.append(d)
        return disponibili

    # -------------------------------
    # Aggiunta prenotazione con controllo disponibilità
    # -------------------------------
    def aggiungi_prenotazione(self, prenotazione: Prenotazione):
        servizio = prenotazione.servizio
        materiale = servizio.materiale
        quantita = servizio.quantita_materiale

        # ricontrolla con dati freschi (concorrenza/altre finestre)
        self._refresh()

        # Controllo disponibilità dipendente
        if not self.dipendente_disponibile(
            prenotazione.dipendente.id,
            prenotazione.ora,
            servizio.durata_minuti
        ):
            raise ValueError("Dipendente non disponibile in questo orario")

        # Controllo materiale
        if materiale and materiale.quantita < quantita:
            raise ValueError(
                f"Materiale insufficiente: {materiale.nome} "
                f"(richiesto {quantita}, disponibile {materiale.quantita})"
            )

        if materiale:
            materiale.usa(quantita)
            materiali_attuali = self.storage_materiali.carica()
            for m in materiali_attuali:
                if m.id == materiale.id:
                    m.quantita = materiale.quantita
                    break
            self.storage_materiali.salva(materiali_attuali)

        # Salvo la prenotazione
        self.prenotazioni.append(prenotazione)
        self.storage.salva(self.prenotazioni)

    # -------------------------------
    # Metodi esistenti
    # -------------------------------
    def get_prenotazione_by_id(self, id):
        return next((p for p in self.prenotazioni if p.id == id), None)

    def rimuovi_prenotazione(self, id):
        prenotazione = self.get_prenotazione_by_id(id)
        if prenotazione:
            servizio = prenotazione.servizio
            materiale = servizio.materiale
            quantita = servizio.quantita_materiale

            if materiale:
                materiali_attuali = self.storage_materiali.carica()
                for m in materiali_attuali:
                    if m.id == materiale.id:
                        m.quantita += quantita
                        break
                self.storage_materiali.salva(materiali_attuali)

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
        self._refresh()
        self.aggiorna_stati()

    def aggiorna_stati(self):
        now = datetime.now()
        modificato = False

        for pren in self.prenotazioni:
            fine = pren.ora + timedelta(minutes=pren.durata_minuti)

            if pren.stato != "pagata":
                if now < fine:
                    pren.stato = "non effettuata"
                else:
                    pren.stato = "effettuata"
                modificato = True

        if modificato:
            self.storage.salva(self.prenotazioni)

    def get_numero_prenotazioni_pagate(self, cliente_id: str) -> int:
        return sum(1 for p in self.prenotazioni if p.cliente.id == cliente_id and p.stato == "pagata")