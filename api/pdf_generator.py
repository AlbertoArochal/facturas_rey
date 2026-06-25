"""Generador de PDF de facturas – HTML + Jinja2 + WeasyPrint."""

import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from io import BytesIO

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _fmt(n):
    """Format number with comma as decimal separator."""
    if n is None:
        return ""
    return f"{float(n):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _enrich(items):
    """Add neto / total_linea to each item."""
    out = []
    for it in items:
        cant = float(it.get("cantidad", 0) or 0)
        precio = float(it.get("precio", 0) or 0)
        dto = float(it.get("descuento", 0) or 0)
        total = cant * precio
        neto = total * (1 - dto / 100)
        enriched = dict(it)
        enriched["total_linea"] = total
        enriched["neto"] = neto
        out.append(enriched)
    return out


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
_TPL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
_jinja = Environment(loader=FileSystemLoader(_TPL_DIR))
_jinja.filters["fmt"] = _fmt


def generar_factura_pdf(receptor, conceptos, tipo="final"):
    material_raw = [it for it in conceptos if it.get("tipo", "material") == "material"]
    mano_obra_raw = [it for it in conceptos if it.get("tipo") == "mano_obra"]

    material = _enrich(material_raw)
    mano_obra = _enrich(mano_obra_raw)

    subtotal_material = sum(it["neto"] for it in material)
    subtotal_mano_obra = sum(it["neto"] for it in mano_obra)

    combined = subtotal_material + subtotal_mano_obra
    igic = combined * 0.07
    total_con_igic = combined + igic

    ctx = {
        "receptor": receptor,
        "material": material,
        "mano_obra": mano_obra,
        "subtotal_material": subtotal_material,
        "subtotal_mano_obra": subtotal_mano_obra,
        "igic": igic,
        "total_con_igic": total_con_igic,
        "tipo": tipo,
    }

    template = _jinja.get_template("factura.html")
    html_str = template.render(ctx)

    buffer = BytesIO()
    HTML(string=html_str).write_pdf(buffer)
    buffer.seek(0)
    return buffer.getvalue()
