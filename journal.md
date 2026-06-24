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

## Commit 4 — Lógica de impuestos + PDF rediseñado + fix Retomar trabajo

- "Generar Factura" ahora usa `?nuevo=1` para limpiar el estado; "Retomar trabajo" carga desde localStorage
- Receptor ahora incluye: nombre, nif, direccion, telefono, diagnosis, num_factura
- Cada concepto tiene un selector de tipo: `material` o `mano_obra` (default `material`)
- Auto-save protegido con `useRef` para no sobrescribir datos durante la carga inicial
- PDF rediseñado basándose en `027 358 Mario Alexander Jiménez Gómez.pdf`:
  - Cabecera "ELECTRICIDAD & Reinaldo Rocha López / FONTANERÍA" + "FACTURA"
  - Sección cliente con CIF, Nombre, Dirección, Telf, Fecha, Nº Fact
  - Línea de Diagnosis
  - Tabla MATERIAL (24 filas) con columnas: REF, DENOMINACION, CANT, Tarifa, Total, DTO%, Neto
  - Tabla MANO DE OBRA (24 filas) con la misma estructura
  - IGIC 7% calculado sobre el total (material + mano de obra)
  - TOTALES EUROS al final
  - Footer: Conforme cliente, cuenta BBVA, dirección
- Marca de agua diagonal en facturas provisionales
- Números formateados con coma decimal europea (6,12 en lugar de 6.12)

### Próximos pasos:
1. Ajustar márgenes y posición exacta de elementos del PDF
2. Hacer el título y subtítulos más alineados con el original
3. Preparar despliegue en Vercel
