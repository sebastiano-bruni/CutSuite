# CutSuite/auth/permissions.py
# Mappa etichette dei pulsanti -> "chiave funzionalità" (così restiamo allineati alla UI attuale)
FEATURES = {
    "Gestione Clienti": "clienti",
    "Gestione Prenotazioni": "prenotazioni",
    "Gestione Servizi": "servizi",
    "Gestione Dipendenti": "dipendenti",
    "Gestione Magazzino": "magazzino",
    "Gestione Promozioni": "promozioni",
}

ALL = set(FEATURES.values())
ROLE_PERMISSIONS = {
    "Proprietario": ALL,
    "Parrucchiere": ALL,  # ← in futuro restringi qui (es. {"clienti","prenotazioni","servizi"})
}

def role_of(user) -> str:
    if getattr(user, "ruolo", None):
        return user.ruolo
    # fallback su permessi
    return "Proprietario" if getattr(user, "permessi", 0) == 1 else "Parrucchiere"

def is_allowed(user, feature_label: str) -> bool:
    role = role_of(user)
    key = FEATURES.get(feature_label)
    if key is None:
        return True  # se non mappata, non blocchiamo
    return key in ROLE_PERMISSIONS.get(role, set())
