"""Generador de PDF de facturas – réplica fiel al modelo Excel/PDF de Reinaldo Rocha."""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

# ---------------------------------------------------------------------------
# Constants – A4 in points (595.27 × 841.89)
# ---------------------------------------------------------------------------
PAGE_WIDTH, PAGE_HEIGHT = A4
IGIC_RATE = 0.07

# Horizontal positions extracted from the reference PDF (pts)
LEFT = 61.8
RIGHT = 547.9

COL_REF = 72.1
COL_DENOM = 134.0
COL_CANT = 241.7
COL_PRECIO = 287.2
COL_TOTAL = 371.0
COL_DTO = 392.0
COL_NETO = 530.4

# Vertical positions from TOP of the page (pts)
# In ReportLab y=0 is the bottom, so we use PAGE_HEIGHT - y_top
Y_ELECTRICIDAD = 82.0
Y_REINALDO = 85.5
Y_FONTANERIA = 93.0
Y_FACTURA = 118.1
Y_CIF = 132.8
Y_NOMBRE = 143.5
Y_DIRECCION = 154.1
Y_DIRECCION2 = 164.8
Y_TELF = 168.7
Y_DIAGNOSIS = 175.5
Y_SUBHEADERS = 201.1
Y_HEADERS = 211.7
Y_FIRST_ROW = 222.4
ROW_HEIGHT = 10.7          # ~3.8 mm

Y_MATERIAL_TOTAL = 468.1
Y_MANO_HEADERS = 521.5
Y_MANO_FIRST_ROW = 532.1
Y_MANO_TOTAL = 617.6
Y_IGIC = 628.3
Y_TOTALES = 681.7
Y_FOOTER1 = 715.4
Y_FOOTER2 = 745.9
Y_FOOTER3 = 757.0

# Number of rows per table section
TABLE_ROWS = 22


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _fmt_num(n: float) -> str:
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _to_bottom(y_top: float) -> float:
    """Convert a y coordinate measured from the top of the page to ReportLab's
    bottom-up coordinate system."""
    return PAGE_HEIGHT - y_top


def _wrap_text(text: str, max_chars: int) -> list[str]:
    """Very naive word-wrap for table descriptions."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 <= max_chars:
            current = (current + " " + w).strip()
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines if lines else [""]


# ---------------------------------------------------------------------------
# Drawing routines
# ---------------------------------------------------------------------------
def _draw_header(c: canvas.Canvas) -> None:
    """Top header: ELECTRICIDAD & / FONTANERÍA (right), Reinaldo Rocha López (big centre-ish),
    FACTURA (left), CIF (right)."""
    # ELECTRICIDAD &  (right, bold 9 pt)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(RIGHT, _to_bottom(Y_ELECTRICIDAD), "ELECTRICIDAD &")

    # FONTANERÍA (right, bold 9 pt, below)
    c.drawRightString(RIGHT, _to_bottom(Y_FONTANERIA), "FONTANERÍA")

    # Reinaldo Rocha López  (big, bold ~18 pt, roughly centred)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(129.1, _to_bottom(Y_REINALDO), "Reinaldo  Rocha  López")

    # FACTURA (left, bold 9 pt)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(81.7, _to_bottom(Y_FACTURA), "FACTURA")

    # CIF (right, 9 pt)
    c.setFont("Helvetica", 9)
    c.drawRightString(RIGHT, _to_bottom(Y_CIF), "CIF: 78729195B")


def _draw_cliente(c: canvas.Canvas, receptor: dict) -> None:
    """Cliente block – labels left, values left; Fecha / Nº Fact / Telf right."""
    nombre = str(receptor.get("nombre", ""))
    direccion = str(receptor.get("direccion", ""))
    direccion2 = str(receptor.get("direccion2", ""))
    admin = str(receptor.get("admin", ""))
    telefono = str(receptor.get("telefono", ""))
    num_factura = str(receptor.get("num_factura", ""))
    diagnosis = str(receptor.get("diagnosis", ""))
    fecha = receptor.get("fecha", datetime.now().strftime("%d/%m/%Y"))

    c.setFont("Helvetica-Bold", 9)
    c.drawString(61.7, _to_bottom(Y_NOMBRE), "Nombre:")
    c.setFont("Helvetica", 9)
    c.drawString(105.4, _to_bottom(Y_NOMBRE), nombre[:60])
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(RIGHT - 90, _to_bottom(Y_NOMBRE), "Fecha:")
    c.setFont("Helvetica", 9)
    c.drawRightString(RIGHT, _to_bottom(Y_NOMBRE), fecha)

    c.setFont("Helvetica-Bold", 9)
    c.drawString(61.7, _to_bottom(Y_DIRECCION), "Dirección:")
    c.setFont("Helvetica", 9)
    c.drawString(105.4, _to_bottom(Y_DIRECCION), direccion[:70])

    next_y = Y_DIRECCION + 10.7
    if direccion2:
        c.setFont("Helvetica", 9)
        c.drawString(105.4, _to_bottom(next_y), direccion2[:70])
        next_y += 10.7

    if admin:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(61.7, _to_bottom(next_y), "Admon:")
        c.setFont("Helvetica", 9)
        c.drawString(105.4, _to_bottom(next_y), admin[:60])
        next_y += 10.7

    if telefono:
        c.setFont("Helvetica-Bold", 9)
        c.drawRightString(RIGHT - 90, _to_bottom(Y_TELF), "Telf:")
        c.setFont("Helvetica", 9)
        c.drawRightString(RIGHT, _to_bottom(Y_TELF), telefono[:20])

    if num_factura:
        c.setFont("Helvetica-Bold", 9)
        c.drawRightString(RIGHT - 90, _to_bottom(Y_DIRECCION), "Nº Fact:")
        c.setFont("Helvetica", 9)
        c.drawRightString(RIGHT, _to_bottom(Y_DIRECCION), num_factura[:12])

    if diagnosis:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(61.7, _to_bottom(Y_DIAGNOSIS), "Diagnosis:")
        c.setFont("Helvetica", 9)
        c.drawString(105.4, _to_bottom(Y_DIAGNOSIS), diagnosis[:80])


def _draw_table_section(
    c: canvas.Canvas,
    y_subheaders: float,
    y_headers: float,
    y_first_row: float,
    y_totals: float,
    items: list[dict],
    title: str,
    draw_subheaders: bool = True,
    split_ref_header: bool = False,
) -> float:
    """Draw a single table section (MATERIAL or MANO DE OBRA).
    Returns the subtotal for this section.

    * split_ref_header=True  → first row = DENOM..CANT..Euros..Euros..DTO(%)..Euros,
                                 second row = REF., data starts below.
    * split_ref_header=False → single header row with REF. included."""

    if draw_subheaders:
        # Tarifa / Total / Neto
        c.setFont("Helvetica-Bold", 9)
        c.drawRightString(COL_PRECIO, _to_bottom(y_subheaders), "Tarifa")
        c.drawRightString(COL_TOTAL, _to_bottom(y_subheaders), "Total")
        c.drawRightString(COL_NETO, _to_bottom(y_subheaders), "Neto")

    # Column headers
    c.setFont("Helvetica-Bold", 9)
    if not split_ref_header:
        c.drawString(COL_REF, _to_bottom(y_headers), "REF.")
    c.drawString(COL_DENOM, _to_bottom(y_headers), "DENOMINACION")
    c.drawRightString(COL_CANT, _to_bottom(y_headers), "CANT.")
    c.drawRightString(COL_PRECIO, _to_bottom(y_headers), "Euros")
    c.drawRightString(COL_TOTAL, _to_bottom(y_headers), "Euros")
    c.drawRightString(COL_DTO, _to_bottom(y_headers), "DTO(%)")
    c.drawRightString(COL_NETO, _to_bottom(y_headers), "Euros")

    if split_ref_header:
        c.drawString(COL_REF, _to_bottom(y_headers + ROW_HEIGHT), "REF.")

    subtotal = 0.0
    current_y = y_first_row

    # Draw data rows
    for it in items:
        desc = str(it.get("descripcion", ""))
        cant = float(it.get("cantidad", 0) or 0)
        precio = float(it.get("precio", 0) or 0)
        dto = float(it.get("descuento", 0) or 0)
        total_linea = cant * precio
        neto = total_linea * (1 - dto / 100)
        subtotal += neto

        ref = str(it.get("ref", ""))

        c.setFont("Helvetica", 9)
        # Description may wrap to 2 lines (like the model)
        lines = _wrap_text(desc, 40)
        for i, line in enumerate(lines[:2]):
            c.drawString(COL_DENOM, _to_bottom(current_y + i * ROW_HEIGHT), line)

        if ref:
            c.drawString(COL_REF, _to_bottom(current_y), ref[:6])
        c.drawRightString(COL_CANT, _to_bottom(current_y), f"{cant:g}" if cant else "")
        c.drawRightString(COL_PRECIO, _to_bottom(current_y), _fmt_num(precio) if precio else "")
        c.drawRightString(COL_TOTAL, _to_bottom(current_y), _fmt_num(total_linea) if total_linea else "")
        if dto:
            c.drawRightString(COL_DTO, _to_bottom(current_y), f"{dto:g}")
        c.drawRightString(COL_NETO, _to_bottom(current_y), _fmt_num(neto) if neto else "0,00")

        current_y += ROW_HEIGHT * max(1, len(lines[:2]))

    # Section totals line
    c.setFont("Helvetica-Bold", 9)
    c.drawString(108.0, _to_bottom(y_totals), title)
    c.drawRightString(COL_TOTAL, _to_bottom(y_totals), "Totales")
    c.drawRightString(COL_NETO, _to_bottom(y_totals), _fmt_num(subtotal))

    return subtotal


def _draw_igic(c: canvas.Canvas, subtotal_material: float, subtotal_mano_obra: float) -> float:
    combined = subtotal_material + subtotal_mano_obra
    igic = combined * IGIC_RATE
    gran_total = combined + igic

    # IGIC row
    c.setFont("Helvetica-Bold", 9)
    c.drawString(COL_DENOM, _to_bottom(Y_IGIC), "IGIC")
    c.setFont("Helvetica", 9)
    c.drawRightString(COL_CANT, _to_bottom(Y_IGIC), "7%")
    c.drawRightString(COL_PRECIO, _to_bottom(Y_IGIC), _fmt_num(igic) + " €")
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(COL_TOTAL, _to_bottom(Y_IGIC), "Totales")
    c.drawRightString(COL_NETO, _to_bottom(Y_IGIC), _fmt_num(gran_total))

    # Empty rows between IGIC and TOTALES (4 rows)
    for i in range(1, 5):
        c.setFont("Helvetica", 9)
        c.drawRightString(COL_TOTAL, _to_bottom(Y_IGIC + i * ROW_HEIGHT), "0,00")
        c.drawRightString(COL_NETO, _to_bottom(Y_IGIC + i * ROW_HEIGHT), "0,00")

    # TOTALES row
    c.setFont("Helvetica-Bold", 9)
    c.drawString(151.8, _to_bottom(Y_TOTALES), "TOTALES")
    c.drawRightString(COL_TOTAL, _to_bottom(Y_TOTALES), "EUROS")
    c.drawRightString(COL_NETO, _to_bottom(Y_TOTALES), _fmt_num(gran_total))

    # 2 empty rows between TOTALES and footer
    for i in range(1, 3):
        c.setFont("Helvetica", 9)
        c.drawRightString(COL_TOTAL, _to_bottom(Y_TOTALES + i * ROW_HEIGHT), "0,00")
        c.drawRightString(COL_NETO, _to_bottom(Y_TOTALES + i * ROW_HEIGHT), "0,00")

    return gran_total


def _draw_footer(c: canvas.Canvas) -> None:
    c.setFont("Helvetica", 9)
    c.drawString(61.8, _to_bottom(Y_FOOTER1), "Conforme cliente")
    c.drawString(230.3, _to_bottom(Y_FOOTER1), "Número de cuenta BBVA: ES1201823000480201516435")

    c.drawString(61.8, _to_bottom(Y_FOOTER2), "C/Los Toledo ,Edificio Yaiza 4, San Isidro 38611")

    c.drawRightString(RIGHT, _to_bottom(Y_FOOTER3), "Proyectos y Asistencia Técnica")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def generar_factura_pdf(
    receptor: dict,
    conceptos: list[dict],
    tipo: str = "final",
) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    _draw_header(c)
    _draw_cliente(c, receptor)

    material = [it for it in conceptos if it.get("tipo", "material") == "material"]
    mano_obra = [it for it in conceptos if it.get("tipo") == "mano_obra"]

    sub_mat = _draw_table_section(
        c, Y_SUBHEADERS, Y_HEADERS, Y_FIRST_ROW, Y_MATERIAL_TOTAL,
        material, "MATERIAL", draw_subheaders=True, split_ref_header=False,
    )

    sub_mo = _draw_table_section(
        c, Y_MANO_HEADERS - 10.7, Y_MANO_HEADERS, Y_MANO_FIRST_ROW, Y_MANO_TOTAL,
        mano_obra, "MANO DE OBRA", draw_subheaders=False, split_ref_header=True,
    )

    _draw_igic(c, sub_mat, sub_mo)
    _draw_footer(c)

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
