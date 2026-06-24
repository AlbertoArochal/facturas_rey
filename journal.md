# Journal — Facturas Rey

## Último estado — 24/06/2026

### Commits (9)
```
a8b1a27 Fix PDF layout: elimina solapamientos, ajusta header/tablas/IGIC/footer al formato del Excel de referencia
8f30653 Header PDF rediseñado (sin solapamiento) + preview provisional + Suspense boundary + solo filas con datos
0ad74f1 first commit
ebc471a journal actualizado con estado final antes de reinicio de sesión
012c610 PDF rediseñado con IGIC + fix Retomar trabajo con ?nuevo=1 + selector Material/Mano de Obra
477e276 Lógica client-side completa + API funcional con generación PDF
1c6696f Catppuccin Mocha dark theme aplicado a toda la interfaz
1306d74 Dashboard y formulario base con datos de receptor y conceptos
5723703 Andamiaje inicial: Next.js + Python backend + configuración Vercel
```

### Funcionalidad completa
- **Dashboard `/`**: Generar Factura (?nuevo=1), Retomar trabajo, Descargar último PDF
- **Formulario `/factura`**: receptor + conceptos con tipo (material/mano_obra), auto-save, validación, descarga PDF
- **API `/api/generar`**: PDF con cabecera, 2 tablas (MATERIAL + MANO DE OBRA), IGIC 7%, footer
- **Header rediseñado**: ELECTRICIDAD & FONTANERÍA + CIF a la derecha, Reinaldo Rocha López a la izquierda, FACTURA grande abajo. Sin solapamiento verificado con pdfminer.
- **Tablas dinámicas**: solo dibuja filas con datos. Descripción truncada a 32 chars para no solapar con columna CANT. Columnas alineadas con Excel de referencia.
- **IGIC**: calculado solo sobre MANO DE OBRA (como en Excel). Layout igual al spreadsheet: IGIC|0.07|<importe>|Totales|<subtotal+igic> + TOTALES|EUROS|<gran_total>
- **Footer**: "Conforme cliente," + IBAN a la derecha. "C/Los Toledo..." izquierda. "Proyectos y Asistencia Técnica" derecha.
- **Factura Provisional**: descarga + abre previsualización en nueva pestaña
- **Suspense boundary**: arreglado error de build con useSearchParams()
- **Tema**: Catppuccin Mocha oscuro
- **Dev server**: `nohup npx next dev -H 0.0.0.0 -p 3000 > /tmp/nextdev.log 2>&1 &`
- **Restart server**: `kill -9 $(lsof -t -i:3000) 2>/dev/null; sleep 1`
- **Test PDF**: `source venv/bin/activate && echo '...' | python3 generate_pdf.py > /tmp/test.pdf`
- **Python venv**: `source venv/bin/activate`

### Fixes aplicados para Vercel deploy
- `api/generar.py`: Cambiado import de `from api.pdf_generator` a `from pdf_generator` (Vercel añade `api/` al `sys.path`, no el directorio padre)
- `generate_pdf.py`: Movido fuera de `api/` (era un script CLI sin `handler` class, Vercel intentaba desplegarlo como serverless function y fallaba). Ajustado `sys.path` al moverse.
- `vercel.json`: Sin cambios necesarios, la config `vercel-python@3.0.0` es correcta.

### Pendiente (próxima sesión)
1. ~~Desplegar en Vercel (verificar que api/index.py funciona con serverless)~~ → Probar `vercel deploy` o `vercel --prod` tras los fixes
