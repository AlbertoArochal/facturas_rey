from http.server import BaseHTTPRequestHandler
import json
from api.pdf_generator import generar_factura_pdf


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        tipo = data.get("tipo", "final")
        receptor = data.get("receptor", {})
        conceptos = data.get("conceptos", [])

        pdf_bytes = generar_factura_pdf(receptor, conceptos, tipo)

        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header(
            "Content-Disposition",
            f'attachment; filename="factura_{tipo}.pdf"',
        )
        self.send_header("Content-Length", str(len(pdf_bytes)))
        self.end_headers()
        self.wfile.write(pdf_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
