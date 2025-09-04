import os
import json
import datetime


class GestoreBackup:
    def __init__(self, gestore_clienti, gestore_prenotazioni, gestore_dipendenti, gestore_servizi, gestore_magazzino):
        self.gestore_clienti = gestore_clienti
        self.gestore_prenotazioni = gestore_prenotazioni
        self.gestore_dipendenti = gestore_dipendenti
        self.gestore_servizi = gestore_servizi
        self.gestore_magazzino = gestore_magazzino

        # Lista dei file di backup effettuati
        self.collectionBackup = []

    # ------------------- METODI GET DATI -------------------

    def getDatiClienti(self):
        return self.gestore_clienti.listaClienti()

    def getDatiPrenotazioni(self):
        return self.gestore_prenotazioni.listaPrenotazioni()

    def getDatiDipendenti(self):
        return self.gestore_dipendenti.listaDipendenti()

    def getDatiServizi(self):
        return self.gestore_servizi.listaServizi()

    def getDatiMagazzino(self):
        return self.gestore_magazzino.listaMateriali()

    # ------------------- SUPPORTO SERIALIZZAZIONE -------------------

    @staticmethod
    def _default_serializer(obj):
        """Funzione usata da json.dump per convertire oggetti custom."""
        if hasattr(obj, "__dict__"):
            return obj.__dict__  # converte l’oggetto in dict
        return str(obj)  # fallback

    # ------------------- EFFETTUA BACKUP -------------------

    def effettuaBackup(self) -> bool:
        """
        Recupera i dati da tutti i gestori e li salva in un file JSON.
        Ritorna True se il backup va a buon fine, False altrimenti.
        """
        try:
            backup_data = {
                "clienti": self.getDatiClienti(),
                "prenotazioni": self.getDatiPrenotazioni(),
                "dipendenti": self.getDatiDipendenti(),
                "servizi": self.getDatiServizi(),
                "magazzino": self.getDatiMagazzino(),
            }

            # Nome file con timestamp
            filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            path = os.path.join("backups", filename)

            os.makedirs("backups", exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=4, ensure_ascii=False, default=self._default_serializer)

            self.collectionBackup.append(path)
            print(f"✅ Backup effettuato: {path}")
            return True

        except Exception as e:
            print(f"❌ Errore durante il backup: {e}")
            return False
