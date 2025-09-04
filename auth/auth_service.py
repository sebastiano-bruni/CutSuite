# CutSuite/auth/auth_service.py
from controller.DipendenteController import DipendenteController
from model.Dipendente import Proprietario  # importa la sottoclasse Proprietario

def authenticate(username: str, password: str):
    """
    Ritorna l'oggetto Dipendente/Proprietario se (username, password) coincidono,
    altrimenti None. (Per ora password in chiaro: così non tocchiamo i dati)
    """

    # ✅ Caso hardcoded admin (puoi anche leggerlo da file in futuro)
    if username == "admin" and password == "admin":
        return Proprietario(
            nome="Super",
            cognome="Admin",
            cf="ADMINCF",
            email="admin@cutsuite.it",
            telefono="0000000000",
            username="admin",
            password="admin"
        )

    # ✅ Caso dipendenti
    ctrl = DipendenteController()
    for d in ctrl.get_tutti_dipendenti():
        if d.username == username and d.password == password:
            return d

    return None


def is_admin(user) -> bool:
    # Admin se Proprietario o se ha permessi = 1
    ruolo = getattr(user, "ruolo", "") or ""
    return ruolo.lower() == "proprietario" or getattr(user, "permessi", 0) == 1
