import sys
from PyQt6.QtWidgets import QApplication

from backup.gestore_backup import GestoreBackup
from view.GestioneClienti.gestioneClienti_ui import GestioneClienti
from view.GestioneDipendenti.gestioneDipendenti_ui import GestioneDipendenti
from view.GestioneMagazzino.gestioneMagazzino_ui import GestioneMagazzino
from view.GestionePrenotazioni.gestionePrenotazioni_ui import GestionePrenotazioni
from view.GestionePromozioni.gestionePromozioni_ui import GestionePromozioni
from view.GestioneServizi.gestioneServizi_ui import GestioneServizi


if __name__ == "__main__":
    # Prima di creare QWidget serve la QApplication
    app = QApplication(sys.argv)

    # Istanzia i gestori
    g_clienti = GestioneClienti()
    g_prenotazioni = GestionePrenotazioni()
    g_dipendenti = GestioneDipendenti()
    g_servizi = GestioneServizi()
    g_magazzino = GestioneMagazzino()

    # Crea gestore backup
    gestore_backup = GestoreBackup(
        g_clienti, g_prenotazioni, g_dipendenti, g_servizi, g_magazzino
    )

    # Forza il backup
    gestore_backup.effettuaBackup()

    # Chiudi senza avviare la GUI
    sys.exit(0)
