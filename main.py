import sys
from PyQt6.QtWidgets import QApplication
from view.home_ui import HomeWindow  # importa la tua classe HomeWindow
from view.accesso_ui import LoginWindow
from backup.gestore_backup import GestoreBackup
from backup.scheduler_backup import SchedulerBackup

from view.GestioneClienti.gestioneClienti_ui import GestioneClienti
from view.GestioneDipendenti.gestioneDipendenti_ui import GestioneDipendenti
from view.GestioneMagazzino.gestioneMagazzino_ui import GestioneMagazzino
from view.GestionePrenotazioni.gestionePrenotazioni_ui import GestionePrenotazioni
from view.GestionePromozioni.gestionePromozioni_ui import GestionePromozioni
from view.GestioneServizi.gestioneServizi_ui import GestioneServizi

def main():

    # 1. Avvia la GUI
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

    # 2. Istanzia i gestori
    gestore_clienti = GestioneClienti()
    gestore_prenotazioni = GestionePrenotazioni()
    gestore_dipendenti = GestioneDipendenti()
    gestore_servizi = GestioneServizi()
    gestore_magazzino = GestioneMagazzino()

    # 3. Crea GestoreBackup
    gestore_backup = GestoreBackup(
        gestore_clienti,
        gestore_prenotazioni,
        gestore_dipendenti,
        gestore_servizi,
        gestore_magazzino
    )

    # 4. Avvia scheduler (in background, non blocca PyQt)
    scheduler = SchedulerBackup(gestore_backup)
    scheduler.avvia_background()

if __name__ == "__main__":
    main()