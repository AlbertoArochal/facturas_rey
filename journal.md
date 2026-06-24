# Journal — Facturas Rey

## Commit 1 — Andamiaje inicial

- Inicializado repositorio git con remote `origin`
- Creado proyecto Next.js (App Router, TypeScript, Tailwind CSS)
- Configurado backend Python en `api/` con Vercel Serverless Functions:
  - `api/index.py` — endpoint POST que recibe datos y devuelve PDF
  - `api/pdf_generator.py` — generación de PDF con reportlab
- Configuración Vercel (`vercel.json`, `requirements.txt`)
- Layout actualizado con título "Facturas Rey"

### Próximos pasos:
1. Implementar pantalla Dashboard (Home) con botón "Generar Factura" y persistencia
2. Implementar formulario de factura con datos de receptor y conceptos dinámicos
3. Conectar frontend con backend Python
