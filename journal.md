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

## Commit 3 — Lógica client-side completa + API funcional

- Dashboard (`/`) convertido a cliente con:
  - Botón "Retomar trabajo" navega a `/factura` con datos guardados
  - Botón "Descargar último PDF" recupera PDF desde localStorage
  - Sección de persistencia se muestra solo si hay datos guardados
- Formulario (`/factura`) convertido a cliente con:
  - State para receptor (nombre, nif, direccion) y array dinámico de conceptos
  - Autocálculo de importe = cantidad × precio en tiempo real
  - Botón "+ Agregar más" añade filas dinámicamente
  - Validación: filas vacías se ignoran, filas incompletas muestran warning en rojo
  - Persistencia automática en localStorage (`factura_datos`)
  - Botones "Factura Provisional" y "Factura Final" llaman al API y descargan PDF
- API route `/api/generar` que ejecuta `api/generate_pdf.py` vía venv Python
- PDF generado correctamente con reportlab

### Próximos pasos:
1. Revisar diseño del PDF generado contra el PDF de referencia
2. Mejorar manejo de errores y feedback visual al usuario
3. Preparar despliegue en Vercel
