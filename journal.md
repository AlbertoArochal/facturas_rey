# Journal — Facturas Rey

## Último estado — 24/06/2026

### Commits (8)
```
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
- **Header rediseñado**: ELECTRICIDAD & + FONTANERÍA a la derecha, Reinaldo Rocha López a la izquierda, FACTURA grande a la izquierda. Sin solapamiento.
- **Tablas dinámicas**: solo dibuja filas con datos (no 24 filas vacías). Descripción truncada a 50 chars.
- **Factura Provisional**: descarga + abre previsualización en nueva pestaña
- **Suspense boundary**: arreglado error de build con useSearchParams()
- **Tema**: Catppuccin Mocha oscuro
- **Dev server**: `nohup npx next dev -H 0.0.0.0 -p 3000 > /tmp/nextdev.log 2>&1 &`
- **Restart server**: `kill -9 $(lsof -t -i:3000) 2>/dev/null; sleep 1`
- **Test PDF**: `source venv/bin/activate && echo '...' | python3 api/generate_pdf.py > /tmp/test.pdf`
- **Python venv**: `source venv/bin/activate`

### Pendiente (próxima sesión)
1. Desplegar en Vercel (verificar que api/index.py funciona con serverless)
2. Ajustar layout de columnas en tabla PDF para que coincida más exactamente con referencia
