from PyQt6.QtCore import QObject, pyqtSignal

class AppSignals(QObject):
    """
    Definisce i segnali globali per l'applicazione.
    Passiamo l'ID del cliente per essere più specifici su cosa è cambiato.
    """
    cliente_modificato = pyqtSignal(int)

# Creiamo un'unica istanza globale che useremo in tutta l'app
app_signals = AppSignals()