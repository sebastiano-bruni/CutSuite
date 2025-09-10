import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

# Aggiungiamo la cartella radice al path per trovare i moduli del progetto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller.PrenotazioneController import PrenotazioneController
from model.Prenotazione import Prenotazione
from model.Cliente import Cliente
from model.Servizio import Servizio
from model.Materiale import Materiale
from model.Dipendente import Parrucchiere


class TestPrenotazioneController(unittest.TestCase):
    """
    Test suite per la classe PrenotazioneController.
    Si concentra sulla logica di business, come la gestione dei materiali.
    """

    def setUp(self):
        """
        Eseguito prima di ogni test. Prepara un ambiente pulito e controllato
        "mockando" (simulando) le interazioni con i file.
        """
        # Patch degli storage per isolare il controller dal file system
        self.patcher_prenotazione = patch('controller.PrenotazioneController.StoragePrenotazione')
        self.patcher_materiale = patch('controller.PrenotazioneController.StorageMateriale')
        self.mock_storage_prenotazione_class = self.patcher_prenotazione.start()
        self.mock_storage_materiale_class = self.patcher_materiale.start()

        # Creazione delle istanze mock degli storage
        self.mock_storage_prenotazione = self.mock_storage_prenotazione_class.return_value
        self.mock_storage_materiale = self.mock_storage_materiale_class.return_value

        # Creazione di dati finti per i test
        self.materiale_finto = Materiale(nome="Shampoo", categoria="Cura", prezzo=10.0, quantita=20, soglia_scorte=5)
        self.materiale_finto.id = 1

        self.servizio_con_materiale = Servizio(nome="Lavaggio Speciale", descrizione="...", prezzo=15.0,
                                               durata_minuti=20, materiale=self.materiale_finto, quantita_materiale=2)
        self.servizio_con_materiale.id = 1

        self.cliente_finto = Cliente(nome="Giulia", cognome="Neri", cf="...", email="...", telefono="...")
        self.cliente_finto.id = 1

        self.dipendente_finto = Parrucchiere(nome="Luca", cognome="Rossi", cf="...", email="...", telefono="...",
                                             username="luca", password="password", stipendio=1500)
        self.dipendente_finto.id = 1

        # Il controller caricherà queste liste finte
        self.mock_storage_prenotazione.carica.return_value = []
        self.mock_storage_materiale.carica.return_value = [self.materiale_finto]

        # Creazione del controller che userà gli storage finti
        self.controller = PrenotazioneController()

    def tearDown(self):
        """Eseguito dopo ogni test per pulire."""
        self.patcher_prenotazione.stop()
        self.patcher_materiale.stop()

    def test_aggiungi_prenotazione_con_materiale_sufficiente(self):
        """
        Verifica che aggiungendo una prenotazione, la quantità del materiale
        associato venga decrementata correttamente.
        """
        prenotazione = Prenotazione(
            cliente=self.cliente_finto, servizio=self.servizio_con_materiale,
            dipendente=self.dipendente_finto, data=datetime.now(), ora=datetime.now(),
            durata_minuti=20, prezzo=15, email_cliente="...", note=""
        )

        self.controller.aggiungi_prenotazione(prenotazione)

        # Verifica che il salvataggio dei materiali sia stato chiamato
        self.mock_storage_materiale.salva.assert_called_once()
        # Prendi la lista di materiali passata a `salva`
        materiali_salvati = self.mock_storage_materiale.salva.call_args[0][0]
        # Controlla che la quantità sia stata aggiornata (20 - 2 = 18)
        self.assertEqual(materiali_salvati[0].quantita, 18)

        # Verifica che anche la prenotazione sia stata salvata
        self.mock_storage_prenotazione.salva.assert_called_once()
        self.assertIn(prenotazione, self.controller.prenotazioni)

    def test_aggiungi_prenotazione_con_materiale_insufficiente(self):
        """
        Verifica che venga sollevata un'eccezione se il materiale non è sufficiente.
        """
        # Impostiamo una quantità di materiale insufficiente
        self.materiale_finto.quantita = 1

        prenotazione = Prenotazione(
            cliente=self.cliente_finto, servizio=self.servizio_con_materiale,  # Richiede 2 unità
            dipendente=self.dipendente_finto, data=datetime.now(), ora=datetime.now(),
            durata_minuti=20, prezzo=15, email_cliente="...", note=""
        )

        # Verifichiamo che venga sollevata l'eccezione corretta
        with self.assertRaises(ValueError):
            self.controller.aggiungi_prenotazione(prenotazione)

        # Verifichiamo che non sia stato effettuato nessun salvataggio
        self.mock_storage_materiale.salva.assert_not_called()
        self.mock_storage_prenotazione.salva.assert_not_called()


if __name__ == '__main__':
    unittest.main()

