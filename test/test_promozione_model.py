import unittest
from datetime import datetime, timedelta
import sys
import os
from unittest.mock import patch

# Aggiungiamo la cartella radice al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.Promozione import Promozione


class TestPromozioneModel(unittest.TestCase):
    """
    Test suite per la classe (modello) Promozione.
    Questo test non ha bisogno di mock perché la classe non dipende da file.
    """

    def test_valida_promozione_con_date(self):
        """
        Verifica che il metodo valida() funzioni correttamente in base alle date.
        """
        # "Oggi" per il nostro test sarà una data fissa
        oggi = datetime(2025, 10, 15)

        # 1. Test di una promozione ATTIVA
        promo_attiva = Promozione(
            nome="Sconto Ottobre", descrizione="...", sconto_percentuale=10,
            data_inizio=oggi - timedelta(days=5),  # Iniziata 5 giorni fa
            data_fine=oggi + timedelta(days=5),  # Finisce tra 5 giorni
            soglia_promozione=0
        )

        # Falsifichiamo la data odierna per il test
        with patch('model.Promozione.datetime') as mock_datetime:
            mock_datetime.now.return_value = oggi
            self.assertTrue(promo_attiva.valida(), "La promozione dovrebbe essere attiva")

        # 2. Test di una promozione SCADUTA
        promo_scaduta = Promozione(
            nome="Sconto Settembre", descrizione="...", sconto_percentuale=10,
            data_inizio=oggi - timedelta(days=20),  # Iniziata 20 giorni fa
            data_fine=oggi - timedelta(days=5),  # Finita 5 giorni fa
            soglia_promozione=0
        )

        with patch('model.Promozione.datetime') as mock_datetime:
            mock_datetime.now.return_value = oggi
            self.assertFalse(promo_scaduta.valida(), "La promozione dovrebbe essere scaduta")

        # 3. Test di una promozione FUTURA
        promo_futura = Promozione(
            nome="Sconto Novembre", descrizione="...", sconto_percentuale=10,
            data_inizio=oggi + timedelta(days=5),  # Inizia tra 5 giorni
            data_fine=oggi + timedelta(days=20),  # Finisce tra 20 giorni
            soglia_promozione=0
        )

        with patch('model.Promozione.datetime') as mock_datetime:
            mock_datetime.now.return_value = oggi
            self.assertFalse(promo_futura.valida(), "La promozione non dovrebbe essere ancora attiva")


if __name__ == '__main__':
    unittest.main()
