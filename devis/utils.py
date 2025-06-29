import json
import os
from decimal import Decimal

from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet

def charger_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def create_devis(data, config, filename="devis.pdf"):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib import colors

    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm, topMargin=2 * cm,
                            bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    elements = []

    # --- Coordonnées entreprise et client côte à côte ---
    entreprise = config["entreprise"]
    client = data["client"]

    entreprise_info = [
        f"<b>{entreprise['nom']}</b>",
        *entreprise["adresse"],
        f"TVA : {entreprise['tva']}",
        f"Tél : {entreprise['telephone']}",
        f"Email : {entreprise['email']}",
        f"Site : {entreprise['site_web']}"
    ]
    client_info = [
        "<b>Devis à l'attention de :</b>",
        *client["nom_et_adresse"]
    ]

    entreprise_para = [Paragraph(line, styles["Normal"]) for line in entreprise_info]
    client_para = [Paragraph(line, styles["Normal"]) for line in client_info]

    coord_table = Table([
        [entreprise_para, client_para]
    ], colWidths=[9 * cm, 7 * cm])

    coord_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    elements.append(coord_table)
    elements.append(Spacer(1, 1 * cm))

    # Infos facture
    elements.append(Paragraph(f"<b>Devis n°:</b> {data['devis_num']}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date:</b> {data['date']}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # En-tête du tableau + données
    styles = getSampleStyleSheet()

    style_table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        alignment=1,  # 0=left, 1=center, 2=right
        fontName="Helvetica-Bold",
        fontSize=9,
        spaceAfter=6,
    )

    headers = [
        Paragraph("Description", style_table_header),
        Paragraph("Quantité", style_table_header),
        Paragraph("PU HTVA", style_table_header),
        Paragraph("TVA %", style_table_header),
        Paragraph("TVAC", style_table_header)
    ]

    table_data = [headers]  # ← première ligne : les titres
    total_htva = total_tva = total_tvac = 0

    for item in data["lignes"]:
        htva = item["prix_unitaire"]
        quantite = item["quantite"]
        pu = item["prix_unitaire_unitaire"]
        tva = htva * item["tva"] / 100
        tvac = htva + tva

        total_htva += htva
        total_tva += tva
        total_tvac += tvac

        table_data.append([
            item["description"],
            str(quantite),
            f"{pu:.2f} €",
            f"{item['tva']} %",
            f"{tvac:.2f} €"
        ])

    # Totaux
    table_data.append(["", "", f"{total_htva:.2f} €", f"{total_tva:.2f} €", f"{total_tvac:.2f} €"])

    table = Table(table_data, colWidths=[7*cm, 2*cm, 3*cm, 2*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 16))  # espace entre tableau et remarque

    # Titre remarques en gras + souligné
    style_remarque_title = ParagraphStyle(
        name="RemarqueTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        underline=True,
        spaceAfter=6
    )

    # Titre remarques en gras et souligné
    style_remarque_title = ParagraphStyle(
        name="RemarqueTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        underline=True,
        spaceAfter=6
    )
    elements.append(Paragraph("Remarques", style_remarque_title))

    # Contenu de la remarque
    remarque_text = data.get("remarques", "<i>néant</i>")
    elements.append(Paragraph(remarque_text, styles["Normal"]))

    elements.append(Spacer(1, 20))  # espace plus grand avant le pied de page

    # Pied de page
    elements.append(Paragraph(
        "Dans l'attente d'une réponse favorable à ce devis, veuillez agréer nos salutations distinguées.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "<i>Ce devis est soumis à nos conditions générales de vente.</i>",
        styles['Normal']
    ))

    # Ajout de la zone de signature
    elements.append(Spacer(1, 3 * cm))  # Ajoutez un espace avant la zone de signature

    signature_style = ParagraphStyle(
        name="SignatureStyle",
        parent=styles["Normal"],
        alignment=2,  # Alignement à droite
        spaceAfter=20,
    )

    signature_text = Paragraph("Signature pour accord :<br/><br/>________________________", signature_style)
    signature_table = Table([[signature_text]], colWidths=[16 * cm])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))

    elements.append(signature_table)

    doc.build(elements)
    return filename

def generer_pdf_devis(devis, output_path="media/devis"):
    config = charger_config()
    client = devis.client

    data = {
        "client": {
            "nom_et_adresse": [
                client.nom,
                *client.adresse_complete(),
                f"Tél : {client.telephone}",
                f"Email : {client.email}",
            ]
        },
        "devis_num": str(devis.pk).zfill(4),
        "date": devis.date.strftime("%d/%m/%Y"),
        "remarques": devis.remarques,
        "lignes": [
            {
                "description": ligne.description,
                "quantite": ligne.quantite,
                "prix_unitaire_unitaire": ligne.prix_unitaire,
                "prix_unitaire": ligne.prix_unitaire * ligne.quantite,
                "tva": Decimal(ligne.tva),
            }
            for ligne in devis.lignes.all()
        ]
    }

    if output_path is None:
        output_path = "."

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    filename = os.path.join(output_path, f"devis_{devis.pk}.pdf")
    return create_devis(data, config, filename)
