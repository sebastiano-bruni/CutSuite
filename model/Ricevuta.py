from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from model.Prenotazione import Prenotazione


@dataclass
class Ricevuta:
    id: int = field(init=False)
    prenotazione: Prenotazione
    importo_totale: float
    dettagli: str
    sconto_applicato: float = 0.0
    importo_finale: float = field(init=False)
    data_emissione: datetime = field(default_factory=datetime.now)

    _next_id: ClassVar[int] = 1

    def __post_init__(self):
        if not hasattr(self, 'id'):
            self.id = Ricevuta._next_id
            Ricevuta._next_id += 1
        # Calcola l'importo finale
        self.importo_finale = self.importo_totale * (1 - self.sconto_applicato)

    def genera_testo(self):
        """Genera una rappresentazione testuale della ricevuta."""
        cliente_nome = f"{self.prenotazione.cliente.nome_completo}"
        servizio_nome = f"{self.prenotazione.servizio.nome}"
        testo = f"""
        --- RICEVUTA #{self.id} ---
        Data di emissione: {self.data_emissione.strftime('%d/%m/%Y %H:%M')}

        Cliente: {cliente_nome}
        Servizio: {servizio_nome}
        Durata: {self.prenotazione.durata_minuti} minuti

        Descrizione:
        {self.dettagli}

        Importo originale: {self.importo_totale:.2f} €
        Sconto applicato: {self.sconto_applicato * 100:.0f} %
        Importo finale: {self.importo_finale:.2f} €
        """
        return testo

    def genera_pdf(self, filename="ricevuta.pdf"):
        """Genera un file PDF stampabile della ricevuta."""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Titolo
        title_style = ParagraphStyle('Title', parent=styles['Normal'], fontSize=20, spaceAfter=20, alignment=1)
        story.append(Paragraph(f"Ricevuta #{self.id}", title_style))

        # Cliente
        cliente_full_name = getattr(self.prenotazione.cliente, "nome_completo", "N/A")

        dipendente_full_name = "N/A"
        if self.prenotazione.dipendente:
            if hasattr(self.prenotazione.dipendente, 'nome') and hasattr(self.prenotazione.dipendente, 'cognome'):
                dipendente_full_name = f"{self.prenotazione.dipendente.nome} {self.prenotazione.dipendente.cognome}"
            elif hasattr(self.prenotazione.dipendente, 'username'):
                dipendente_full_name = self.prenotazione.dipendente.username

        # Info generali
        story.append(Paragraph(f"<b>Data di emissione:</b> {self.data_emissione.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 0.5 * cm))
        story.append(Paragraph(f"<b>Cliente:</b> {cliente_full_name}", styles['Normal']))
        story.append(Paragraph(f"<b>Servizio:</b> {self.prenotazione.servizio.nome}", styles['Normal']))
        story.append(Paragraph(f"<b>Dipendente:</b> {dipendente_full_name}", styles['Normal']))
        story.append(Paragraph(
            f"<b>Data:</b> {self.prenotazione.data.strftime('%d/%m/%Y')} | <b>Ora:</b> {self.prenotazione.ora.strftime('%H:%M')}",
            styles['Normal']))
        story.append(Spacer(1, 0.5 * cm))

        # Dettagli servizio
        story.append(Paragraph("<b>Descrizione servizio:</b>", styles['Normal']))
        story.append(Paragraph(f"{self.dettagli}", styles['Normal']))
        story.append(Spacer(1, 0.5 * cm))

        # Importi
        story.append(Paragraph(f"<b>Importo originale:</b> {self.importo_totale:.2f} €", styles['Normal']))
        story.append(Paragraph(f"<b>Sconto applicato:</b> {self.sconto_applicato * 100:.0f} %", styles['Normal']))
        story.append(Paragraph(f"<b>Importo finale:</b> {self.importo_finale:.2f} €", styles['Normal']))

        doc.build(story)