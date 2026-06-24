# Journal — Facturas Rey

## Commit 1 — Andamiaje inicial

- Inicializado repositorio git con remote `origin`
- Creado proyecto Next.js (App Router, TypeScript, Tailwind CSS)
- Configurado backend Python en `api/` con Vercel Serverless Functions:
  - `api/index.py` — endpoint POST que recibe datos y devuelve PDF
  - `api/pdf_generator.py` — generación de PDF con reportlab
- Configuración Vercel (`vercel.json`, `requirements.txt`)
- Layout actualizado con título "Facturas Rey"

## Commit 2 — Dashboard y formulario base

- Creada pantalla Dashboard (`/`) con botón "Generar Factura"
- Creado formulario de factura (`/factura`) con:
  - Campos de datos del receptor (nombre, NIF, dirección)
  - 5 filas iniciales de conceptos con botón "Agregar más"
  - Botones "Factura Provisional" y "Factura Final"
- Instaladas dependencias Python en venv local
- Dev server funcionando en `http://localhost:3000`

### Próximos pasos:
1. Implementar lógica client-side (autocalcular importes, persistencia localStorage)
2. Implementar validaciones y warnings visuales
3. Conectar frontend con backend Python para generación de PDF
