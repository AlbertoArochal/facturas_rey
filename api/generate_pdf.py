import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.pdf_generator import generar_factura_pdf

data = json.loads(sys.stdin.read())
pdf_bytes = generar_factura_pdf(
    data.get("receptor", {}),
    data.get("conceptos", []),
    data.get("tipo", "final"),
)
sys.stdout.buffer.write(pdf_bytes)
