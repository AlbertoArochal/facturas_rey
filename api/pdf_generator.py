from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime


IGIC_RATE = 0.07
ROWS_PER_TABLE = 24
PAGE_WIDTH, PAGE_HEIGHT = A4


def _fmt_num(n: float) -> str:
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _draw_header(c: canvas.Canvas, y: float) -> float:
    c.setFont("Helvetica-Bold", 18)
    c.drawString(20 * mm, y, "ELECTRICIDAD &")
    y -= 6 * mm
    c.drawString(20 * mm, y, "Reinaldo Rocha López")
    y -= 6 * mm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, y, "FONTANERÍA")
    y -= 6 * mm

    c.setFont("Helvetica-Bold", 36)
    c.drawString(150 * mm, y + 12 * mm, "FACTURA")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y - 2 * mm, "Cliente")
    c.drawString(105 * mm, y - 2 * mm, "CIF: 78729195B")

    y -= 10 * mm
    c.line(20 * mm, y, 190 * mm, y)
    return y - 4 * mm


def _draw_cliente(c: canvas.Canvas, y: float, receptor: dict) -> float:
    nombre = receptor.get("nombre", "")
    nif = receptor.get("nif", "")
    direccion = receptor.get("direccion", "")
    telefono = receptor.get("telefono", "")

    c.setFont("Helvetica", 10)
    line_height = 5 * mm
    left_lines = [
        ("Nombre:", nombre),
        ("Dirección:", direccion),
    ]
    if telefono:
        left_lines.append(("Telf:", telefono))

    right_lines = [
        ("Fecha:", datetime.now().strftime("%d/%m/%Y")),
        ("Nº Fact:", receptor.get("num_factura", "")),
    ]

    max_lines = max(len(left_lines), len(right_lines))
    for i in range(max_lines):
        if i < len(left_lines):
            label, value = left_lines[i]
            c.setFont("Helvetica-Bold", 10)
            c.drawString(20 * mm, y, label)
            c.setFont("Helvetica", 10)
            c.drawString(35 * mm, y, str(value)[:60])
        if i < len(right_lines):
            label, value = right_lines[i]
            c.setFont("Helvetica-Bold", 10)
            c.drawString(120 * mm, y, label)
            c.setFont("Helvetica", 10)
            c.drawString(135 * mm, y, str(value)[:30])
        y -= line_height

    if nif:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20 * mm, y, "CIF/NIF:")
        c.setFont("Helvetica", 10)
        c.drawString(35 * mm, y, nif)
        y -= line_height

    return y - 3 * mm


def _draw_diagnosis(c: canvas.Canvas, y: float, receptor: dict) -> float:
    diagnosis = receptor.get("diagnosis", "")
    if diagnosis:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20 * mm, y, "Diagnosis:")
        c.setFont("Helvetica", 10)
        c.drawString(42 * mm, y, diagnosis[:80])
        y -= 7 * mm
    return y - 2 * mm


def _draw_table(
    c: canvas.Canvas,
    y: float,
    title: str,
    items: list[dict],
    row_height: float = 4 * mm,
) -> tuple[float, float]:
    cols = {
        "ref": 22 * mm,
        "denom": 75 * mm,
        "cant": 110 * mm,
        "precio": 130 * mm,
        "total": 148 * mm,
        "dto": 165 * mm,
        "neto": 180 * mm,
    }

    c.setFont("Helvetica-Bold", 9)
    c.drawString(cols["ref"] - 2 * mm, y, "Tarifa")
    c.drawString(cols["denom"] + 20 * mm, y, "Total")
    c.drawString(cols["neto"], y, "Neto")
    y -= 4 * mm

    c.setFont("Helvetica-Bold", 8)
    c.drawString(cols["ref"], y, "REF.")
    c.drawString(cols["denom"], y, "DENOMINACION")
    c.drawString(cols["cant"], y, "CANT.")
    c.drawString(cols["precio"], y, "Euros")
    c.drawString(cols["total"], y, "Euros")
    c.drawString(cols["dto"], y, "DTO(%)")
    c.drawString(cols["neto"], y, "Euros")
    y -= 3 * mm
    c.line(20 * mm, y, 190 * mm, y)
    y -= row_height

    c.setFont("Helvetica", 8)
    subtotal = 0.0
    for i in range(ROWS_PER_TABLE):
        if i < len(items):
            it = items[i]
            desc = str(it.get("descripcion", ""))
            cant = float(it.get("cantidad", 0) or 0)
            precio = float(it.get("precio", 0) or 0)
            dto = float(it.get("descuento", 0) or 0)
            total_linea = cant * precio
            neto = total_linea * (1 - dto / 100)
            subtotal += neto

            ref = str(it.get("ref", ""))
            if ref:
                c.drawString(cols["ref"], y, ref[:6])
            c.drawString(cols["denom"], y, desc[:40])
            c.drawRightString(cols["cant"] + 8 * mm, y, f"{cant:g}" if cant else "")
            c.drawRightString(cols["precio"] + 8 * mm, y, _fmt_num(precio) if precio else "")
            c.drawRightString(cols["total"] + 8 * mm, y, _fmt_num(total_linea) if total_linea else "")
            if dto:
                c.drawRightString(cols["dto"] + 8 * mm, y, f"{dto:g}")
            c.drawRightString(cols["neto"] + 8 * mm, y, _fmt_num(neto) if neto else "0,00")
        y -= row_height

    y -= 2 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, title)
    c.drawString(120 * mm, y, "Totales")
    c.drawRightString(cols["neto"] + 8 * mm, y, _fmt_num(subtotal))
    y -= 6 * mm

    return y, subtotal


def _draw_igic(
    c: canvas.Canvas,
    y: float,
    base_imponible: float,
) -> tuple[float, float, float]:
    igic = base_imponible * IGIC_RATE
    total = base_imponible + igic

    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "IGIC")
    c.drawString(50 * mm, y, f"{int(IGIC_RATE * 100)}%")
    c.drawString(80 * mm, y, _fmt_num(igic) + " €")
    c.drawString(120 * mm, y, "Totales")
    c.drawRightString(188 * mm, y, _fmt_num(total))
    y -= 8 * mm

    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, y, "TOTALES")
    c.drawString(100 * mm, y, "EUROS")
    c.drawRightString(188 * mm, y, _fmt_num(total))
    y -= 10 * mm

    return y, igic, total


def _draw_footer(c: canvas.Canvas, y: float) -> float:
    y = 30 * mm
    c.setFont("Helvetica", 9)
    c.drawString(20 * mm, y, "Conforme cliente")
    c.drawString(100 * mm, y, "Número de cuenta BBVA: ES1201823000480201516435")
    y -= 6 * mm
    c.drawString(20 * mm, y, "C/Los Toledo, Edificio Yaiza 4, San Isidro 38611")
    y -= 6 * mm
    c.drawString(20 * mm, y, "Proyectos y Asistencia Técnica")
    return y


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

    material = [c for c in conceptos if c.get("tipo", "material") == "material"]
    mano_obra = [c for c in conceptos if c.get("tipo") == "mano_obra"]

    y, _ = _draw_table(c, y, "MATERIAL", material)
    y, _ = _draw_table(c, y, "MANO DE OBRA", mano_obra)

    total_neto = sum(
        float(c.get("cantidad", 0) or 0) * float(c.get("precio", 0) or 0)
        * (1 - float(c.get("descuento", 0) or 0) / 100)
        for c in conceptos
    )
    _draw_igic(c, y, total_neto)
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
