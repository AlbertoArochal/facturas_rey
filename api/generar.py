import sys
import os
import json
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

try:
    from pdf_generator import generar_factura_pdf
except ImportError:
    from api.pdf_generator import generar_factura_pdf


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
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
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self._send_json(500, {"error": str(e), "traceback": tb})

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
