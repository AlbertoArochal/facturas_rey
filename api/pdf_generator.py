from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime


def generar_factura_pdf(
    receptor: dict,
    conceptos: list[dict],
    tipo: str = "final",
) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40 * mm

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40 * mm, y, "FACTURA")
    y -= 10 * mm

    c.setFont("Helvetica", 10)
    c.drawString(40 * mm, y, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    y -= 7 * mm

    c.setFont("Helvetica-Bold", 11)
    c.drawString(40 * mm, y, "DATOS DEL RECEPTOR")
    y -= 6 * mm
    c.setFont("Helvetica", 10)
    c.drawString(40 * mm, y, f"Nombre: {receptor.get('nombre', '')}")
    y -= 5 * mm
    c.drawString(40 * mm, y, f"NIF/CIF: {receptor.get('nif', '')}")
    y -= 5 * mm
    c.drawString(40 * mm, y, f"Dirección: {receptor.get('direccion', '')}")
    y -= 10 * mm

    c.setFont("Helvetica-Bold", 11)
    c.drawString(40 * mm, y, "CONCEPTOS")
    y -= 6 * mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(40 * mm, y, "Descripción")
    c.drawString(100 * mm, y, "Cant.")
    c.drawString(130 * mm, y, "Precio")
    c.drawString(160 * mm, y, "Importe")
    y -= 5 * mm

    c.setStrokeColor(colors.black)
    c.line(40 * mm, y, 170 * mm, y)
    y -= 4 * mm

    c.setFont("Helvetica", 9)
    total = 0
    for conc in conceptos:
        desc = conc.get("descripcion", "")
        cant = conc.get("cantidad", 0)
        precio = conc.get("precio", 0)
        importe = cant * precio
        total += importe

        c.drawString(40 * mm, y, desc[:35])
        c.drawString(100 * mm, y, str(cant))
        c.drawString(130 * mm, y, f"{precio:.2f}")
        c.drawString(160 * mm, y, f"{importe:.2f}")
        y -= 5 * mm

    y -= 4 * mm
    c.line(40 * mm, y, 170 * mm, y)
    y -= 6 * mm

    c.setFont("Helvetica-Bold", 11)
    c.drawString(130 * mm, y, "TOTAL:")
    c.drawString(160 * mm, y, f"{total:.2f}")

    if tipo == "provisional":
        c.saveState()
        c.setFont("Helvetica", 40)
        c.setFillColor(colors.Color(0, 0, 0, alpha=0.15))
        c.translate(width / 2, height / 2)
        c.rotate(45)
        c.drawCentredString(0, 0, "PROVISIONAL - NO VÁLIDA")
        c.restoreState()

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
