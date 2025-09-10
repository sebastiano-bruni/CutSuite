import unittest
from unittest.mock import patch
import sys
import os

# Aggiungiamo la cartella radice al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller.MaterialeController import MaterialeController
from model.Materiale import Materiale


class TestMaterialeController(unittest.TestCase):
    """
    Test suite per la classe MaterialeController.
    """

    def setUp(self):
        """Eseguito prima di ogni test."""
        # Mock dello storage per non usare file reali
        self.patcher = patch('controller.MaterialeController.StorageMateriale')
        self.mock_storage_class = self.patcher.start()
        self.mock_storage_instance = self.mock_storage_class.return_value

        # Dati finti
        self.materiale_finto = Materiale(nome="Tinta Blu", categoria="Colorazione", prezzo=15.0, quantita=5,
                                         soglia_scorte=2)
        self.materiale_finto.id = 1

        # Il controller caricherà questa lista
        self.mock_storage_instance.carica.return_value = [self.materiale_finto]

        # Creazione del controller
        self.controller = MaterialeController()

    def tearDown(self):
        """Eseguito dopo ogni test."""
        self.patcher.stop()

    def test_diminuisci_quantita_fallisce_se_insufficente(self):
        """
        Verifica che il metodo diminuisci_quantita ritorni False se si cerca
        di rimuovere una quantità maggiore di quella disponibile.
        """
        quantita_da_rimuovere = 10

        # La quantità da rimuovere (10) è maggiore di quella disponibile (5)
        self.assertGreater(quantita_da_rimuovere, self.materiale_finto.quantita)

        # Chiamiamo il metodo e ci aspettiamo che ritorni False
        successo = self.controller.diminuisci_quantita(self.materiale_finto.id, quantita_da_rimuovere)

        # Verifichiamo che l'operazione non sia andata a buon fine
        self.assertFalse(successo)

        # Verifichiamo che la quantità originale del materiale non sia cambiata
        self.assertEqual(self.materiale_finto.quantita, 5)

        # Verifichiamo che il metodo `salva` NON sia stato chiamato
        self.mock_storage_instance.salva.assert_not_called()


if __name__ == '__main__':
    unittest.main()
