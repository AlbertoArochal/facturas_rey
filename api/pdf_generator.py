from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime


IGIC_RATE = 0.07
PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT = 20 * mm
RIGHT = 190 * mm
USABLE = RIGHT - LEFT

# Column positions (from left margin)
COL_REF = LEFT
COL_DENOM = LEFT + 12 * mm
COL_CANT = LEFT + 65 * mm
COL_PRECIO = LEFT + 85 * mm
COL_TOTAL = LEFT + 108 * mm
COL_DTO = LEFT + 128 * mm
COL_NETO = RIGHT

LIGHT_GRAY = colors.Color(0.85, 0.85, 0.85)


def _fmt_num(n: float) -> str:
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _draw_header(c: canvas.Canvas, y: float) -> float:
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(RIGHT, y, "ELECTRICIDAD & FONTANERÍA")
    c.setFont("Helvetica", 9)
    c.drawRightString(RIGHT, y - 4.5 * mm, "CIF: 78729195B")
    y -= 12 * mm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(LEFT, y, "Reinaldo Rocha López")
    y -= 15 * mm

    c.setFont("Helvetica-Bold", 36)
    c.drawString(LEFT + 5 * mm, y, "FACTURA")
    y -= 16 * mm

    c.line(LEFT, y, RIGHT, y)
    return y - 5 * mm


def _draw_cliente(c: canvas.Canvas, y: float, receptor: dict) -> float:
    nombre = receptor.get("nombre", "")
    nif = receptor.get("nif", "")
    direccion = receptor.get("direccion", "")
    telefono = receptor.get("telefono", "")
    admin = receptor.get("admin", "")

    line_h = 5 * mm

    c.setFont("Helvetica-Bold", 9)
    c.drawString(LEFT, y, "Nombre:")
    c.setFont("Helvetica", 9)
    c.drawString(LEFT + 17 * mm, y, str(nombre)[:60])
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(RIGHT - 18 * mm, y, "Nº Fact:")
    c.setFont("Helvetica", 9)
    c.drawRightString(RIGHT, y, str(receptor.get("num_factura", ""))[:12])
    y -= line_h

    c.setFont("Helvetica-Bold", 9)
    c.drawString(LEFT, y, "Dirección:")
    c.setFont("Helvetica", 9)
    c.drawString(LEFT + 17 * mm, y, str(direccion)[:60])
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(RIGHT - 18 * mm, y, "Fecha:")
    c.setFont("Helvetica", 9)
    c.drawRightString(RIGHT, y, datetime.now().strftime("%d/%m/%Y"))
    y -= line_h

    if admin:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(LEFT, y, "Admon:")
        c.setFont("Helvetica", 9)
        c.drawString(LEFT + 17 * mm, y, str(admin)[:60])
        y -= line_h

    if nif:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(LEFT, y, "CIF/NIF:")
        c.setFont("Helvetica", 9)
        c.drawString(LEFT + 17 * mm, y, str(nif)[:20])
        y -= line_h

    if telefono:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(LEFT, y, "Telf:")
        c.setFont("Helvetica", 9)
        c.drawString(LEFT + 17 * mm, y, str(telefono)[:20])
        y -= line_h

    return y - 3 * mm


def _draw_diagnosis(c: canvas.Canvas, y: float, receptor: dict) -> float:
    diagnosis = receptor.get("diagnosis", "")
    if diagnosis:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(LEFT, y, "Diagnosis:")
        c.setFont("Helvetica", 9)
        c.drawString(LEFT + 17 * mm, y, diagnosis[:80])
        y -= 7 * mm
    return y - 3 * mm


def _draw_table(
    c: canvas.Canvas,
    y: float,
    title: str,
    items: list[dict],
) -> tuple[float, float]:
    row_h = 4.5 * mm

    # Sub-header line: "Tarifa", "Total", "Neto" above the right columns
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(COL_PRECIO, y, "Tarifa")
    c.drawRightString(COL_TOTAL, y, "Total")
    c.drawRightString(COL_NETO, y, "Neto")
    y -= 3.5 * mm

    # Column headers
    c.setFont("Helvetica-Bold", 8)
    c.drawString(COL_REF, y, "REF.")
    c.drawString(COL_DENOM, y, "DENOMINACION")
    c.drawRightString(COL_CANT, y, "CANT.")
    c.drawRightString(COL_PRECIO, y, "Euros")
    c.drawRightString(COL_TOTAL, y, "Euros")
    c.drawRightString(COL_DTO, y, "DTO(%)")
    c.drawRightString(COL_NETO, y, "Euros")
    y -= 3 * mm

    c.line(LEFT, y, RIGHT, y)
    y -= row_h

    c.setFont("Helvetica", 8)
    subtotal = 0.0
    for it in items:
        desc = str(it.get("descripcion", ""))[:32]
        cant = float(it.get("cantidad", 0) or 0)
        precio = float(it.get("precio", 0) or 0)
        dto = float(it.get("descuento", 0) or 0)
        total_linea = cant * precio
        neto = total_linea * (1 - dto / 100)
        subtotal += neto

        ref = str(it.get("ref", ""))
        if ref:
            c.drawString(COL_REF, y, ref[:6])
        c.drawString(COL_DENOM, y, desc)
        c.drawRightString(COL_CANT, y, f"{cant:g}" if cant else "")
        c.drawRightString(COL_PRECIO, y, _fmt_num(precio) if precio else "")
        c.drawRightString(COL_TOTAL, y, _fmt_num(total_linea) if total_linea else "")
        if dto:
            c.drawRightString(COL_DTO, y, f"{dto:g}")
        c.drawRightString(COL_NETO, y, _fmt_num(neto) if neto else "0,00")
        y -= row_h

    y -= 2 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(COL_DENOM, y, title)
    c.drawRightString(COL_TOTAL, y, "Totales")
    c.drawRightString(COL_NETO, y, _fmt_num(subtotal))
    y -= 8 * mm

    return y, subtotal


def _draw_igic_and_totals(
    c: canvas.Canvas,
    y: float,
    subtotal_material: float,
    subtotal_mano_obra: float,
) -> tuple[float, float, float, float]:
    igic = subtotal_mano_obra * IGIC_RATE
    total_mano_obra_igic = subtotal_mano_obra + igic
    gran_total = subtotal_material + total_mano_obra_igic

    c.setFont("Helvetica-Bold", 9)
    c.drawString(COL_DENOM, y, "IGIC")
    c.setFont("Helvetica", 9)
    c.drawRightString(COL_CANT, y, str(IGIC_RATE))
    c.drawRightString(COL_PRECIO, y, _fmt_num(igic))
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(COL_TOTAL, y, "Totales")
    c.drawRightString(COL_NETO, y, _fmt_num(total_mano_obra_igic))
    y -= 8 * mm

    y -= 4 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(COL_DENOM, y, "TOTALES")
    c.drawRightString(COL_TOTAL, y, "EUROS")
    c.drawRightString(COL_NETO, y, _fmt_num(gran_total))
    y -= 12 * mm

    return y, igic, gran_total, subtotal_mano_obra


def _draw_footer(c: canvas.Canvas, y: float) -> None:
    footer_y = 25 * mm
    if y < footer_y + 20 * mm:
        c.showPage()
        y = PAGE_HEIGHT - 20 * mm

    y = footer_y + 20 * mm

    c.setFont("Helvetica", 9)
    c.drawString(LEFT, y, "Conforme cliente,")
    c.drawRightString(RIGHT, y, "Número de cuenta BBVA: ES1201823000480201516435")
    y -= 6 * mm
    c.drawString(LEFT, y, "C/Los Toledo, Edificio Yaiza 4, San Isidro 38611")
    y -= 6 * mm
    c.drawRightString(RIGHT, y, "Proyectos y Asistencia Técnica")


def generar_factura_pdf(
    receptor: dict,
    conceptos: list[dict],
    tipo: str = "final",
) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    y = PAGE_HEIGHT - 20 * mm
    y = _draw_header(c, y)
    y = _draw_cliente(c, y, receptor)
    y = _draw_diagnosis(c, y, receptor)

    material = [it for it in conceptos if it.get("tipo", "material") == "material"]
    mano_obra = [it for it in conceptos if it.get("tipo") == "mano_obra"]

    y, sub_mat = _draw_table(c, y, "MATERIAL", material)
    y, sub_mo = _draw_table(c, y, "MANO DE OBRA", mano_obra)

    y, igic, gran_total, _ = _draw_igic_and_totals(c, y, sub_mat, sub_mo)

    _draw_footer(c, y)

    if tipo == "provisional":
        c.saveState()
        c.setFont("Helvetica-Bold", 60)
        c.setFillColor(colors.Color(0.8, 0, 0, alpha=0.25))
        c.translate(PAGE_WIDTH / 2, PAGE_HEIGHT / 2)
        c.rotate(30)
        c.drawCentredString(0, 0, "PROVISIONAL")
        c.restoreState()

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
