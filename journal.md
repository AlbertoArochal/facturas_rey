# Journal — Facturas Rey

## Último estado — 24/06/2026

### Commits (5)
```
012c610 PDF rediseñado con IGIC + fix Retomar trabajo con ?nuevo=1 + selector Material/Mano de Obra
477e276 Lógica client-side completa + API funcional con generación PDF
1c6696f Catppuccin Mocha dark theme
1306d74 Dashboard y formulario base
5723703 Andamiaje inicial
```

### Funcionalidad completa
- **Dashboard `/`**: Generar Factura (?nuevo=1), Retomar trabajo, Descargar último PDF
- **Formulario `/factura`**: receptor + conceptos con tipo (material/mano_obra), auto-save, validación, descarga PDF
- **API `/api/generar`**: PDF con cabecera, 2 tablas, IGIC 7%, footer. Cálculos coinciden con el PDF de referencia.
- **Tema**: Catppuccin Mocha oscuro
- **Dev server**: `nohup npx next dev -H 0.0.0.0 -p 3000 > /tmp/nextdev.log 2>&1 &`
- **Restart server**: `kill -9 $(lsof -t -i:3000) 2>/dev/null; sleep 1`
- **Test PDF**: `source venv/bin/activate && echo '...' | python3 api/generate_pdf.py > /tmp/test.pdf`
- **Python venv**: `source venv/bin/activate`

### Pendiente (próxima sesión)
1. Ajustar posición/márgenes del PDF para coincidir visualmente con la referencia
2. Hacer que el título de cabecera no se solape ("ELECTRICIDAD &" vs "FACTURA")
3. Previsualización de factura provisional en pantalla (no solo descarga)
4. Desplegar en Vercel
