# Especificaciones del Proyecto: Facturas Rey (MVP)

Este documento define los requisitos, la arquitectura, el flujo de trabajo y las restricciones técnicas para el desarrollo del proyecto **Facturas Rey**. El agente de OpenCode debe seguir estas instrucciones de forma estricta.

---

## 1. Descripción General del Proyecto
**Facturas Rey** es una aplicación web destinada a la generación y gestión de facturas. El objetivo principal es migrar un flujo de trabajo actual (basado en una hoja de cálculo Excel y una plantilla PDF de referencia) hacia una interfaz web moderna, intuitiva y robusta, desplegada en **Vercel**, con un backend de procesamiento en **Python**.

---

## 2. Arquitectura y Tecnologías
* **Frontend:** Interfaz web interactiva (se recomienda Next.js o React para facilitar el despliegue serverless en Vercel). El diseño debe ser limpio, profesional y completamente en **castellano**.
* **Backend:** Servicios en **Python** para el procesamiento de datos, cálculos financieros y la generación exacta del documento PDF final.
* **Despliegue:** Plataforma **Vercel** (utilizando Vercel Serverless Functions para el entorno de Python si se requiere una arquitectura unificada).
* **Persistencia Local:** Los datos de la última factura generada deben persistir en el navegador (ej. `localStorage`) o mediante una sesión ligera para permitir la recuperación del trabajo.

---

## 3. Requisitos Funcionales (Flujo de la Interfaz Web)

### Pantalla Inicial (Dashboard / Home)
1.  **Botón "Generar Factura":** Al hacer clic, redirige o abre una nueva pantalla/formulario para la introducción de datos.
2.  **Estado de Persistencia:** Si el usuario ya generó una factura anteriormente, la pantalla inicial debe mostrar de forma prominente:
    * La opción de **volver a descargar** el último PDF generado.
    * La opción de **retomar el trabajo** anterior, precargando todos los campos en el formulario de edición.

### Pantalla de Creación / Formulario de Factura
1.  **Datos del Receptor:** Campos obligatorios para Nombre/Razón Social, NIF/CIF, Dirección, etc.
2.  **Sección Dinámica de Conceptos (Líneas de Factura):**
    * De forma predeterminada, la interfaz debe mostrar **al menos cinco (5) espacios (filas)** para conceptos de facturación.
    * Cada fila constará de campos como: Descripción, Cantidad, Precio Unitario e Importe (autocalculado).
    * **Botón "Agregar más":** Permite añadir nuevas filas de conceptos de forma indefinida.
    * **Regla de Limpieza:** Si al procesar la factura algún concepto está completamente vacío, el sistema **debe ignorar esa línea** de forma automática sin arrojar errores.
3.  **Acciones del Formulario:**
    * **Botón "Factura Provisional":** Genera y previsualiza un documento idéntico al diseño final pero con una **marca de agua clara** o texto indicativo (ej. "PROVISIONAL - NO VÁLIDA").
    * **Botón "Factura Final":** Si el usuario está conforme, este botón procesa, bloquea, genera y **descarga automáticamente** el documento PDF definitivo.

---

## 4. Gestión de Errores y Robustez (Mapeo de Fallos)
El sistema debe tolerar errores comunes del operador mediante un sistema de alertas en pantalla (**warnings/notificaciones**) sin interrumpir el flujo ni romper la aplicación:
* **Concepto Incompleto:** Si una fila de concepto tiene texto pero le falta la cantidad o el precio, se mostrará un warning visual en la fila ("Campos obligatorios faltantes") e ignorará la línea en el cálculo si no se subsana, pero no tumbará el renderizado.
* **Formato Numérico Incorrecto:** Si el usuario introduce letras en campos de precio o cantidad, el sistema mostrará un warning dinámico, aplicando un fallback temporal (ej. asumir 0 o el último valor válido) para evitar crasheos de tipos de datos.

---

## 5. Protocolo de Git, Commits y Resiliencia (Instrucciones para el Agente)
El agente de OpenCode debe ceñirse rigurosamente a las siguientes reglas de control de versiones y persistencia de desarrollo:

1.  **Commits por Interacción:** Cada cambio o evolución completada a través de un prompt de interacción debe guardarse en un commit local independiente.
2.  **Restricción de Push:** El agente **NO debe hacer `git push`** bajo ninguna circunstancia a menos que el usuario lo autorice explícitamente en el chat.
3.  **Estrategia de Ramas:**
    * Todo el desarrollo del MVP base se realiza en la rama `main` del repositorio: `https://github.com/AlbertoArochal/facturas_rey`.
    * Cualquier experimento, prueba o funcionalidad que exceda estas especificaciones (como integraciones con Google Drive u otros sistemas externos) **debe desarrollarse en una rama separada**. No se realizará `git merge` a `main` sin confirmación previa del usuario.
4.  **Archivo de Resiliencia (`journal.md`):**
    * Para mitigar pérdidas por posibles crasheos o reinicios del contexto del agente, **cada vez que se realice un commit, el agente debe actualizar un archivo local en la raíz llamado `journal.md`**.
    * Este archivo registrará cronológicamente: el estado actual del desarrollo, qué archivos fueron modificados, el hash del commit y los pasos inmediatos a seguir. Servirá como punto de restauración para retomar el trabajo exactamente donde se dejó.

---

## 6. Referencias de Diseño y Datos
El backend en Python debe replicar matemáticamente las fórmulas de la hoja de cálculo y visualmente la estética del PDF de referencia:
* **Ubicación:** Los archivos base se encuentran en la carpeta raíz del proyecto (una spreadsheet/Excel y un PDF de referencia).
* **Fidelidad:** El resultado final del PDF generado por el backend de Python debe ser **siempre similar y equivalente en diseño, tipografía y distribución al PDF de referencia**.

---

## 7. Sección de Ayuda / Help (Para el Usuario Final)

Esta sección debe ser accesible desde la propia interfaz web para guiar al usuario:

### 💡 Guía de Uso Rápido de Facturas Rey

* **¿Cómo empiezo una factura?**
    Haga clic en el botón **"Generar Factura"** en la pantalla de inicio. Rellene los datos del receptor y complete las líneas de los conceptos que desea facturar.
* **¿Qué pasa si necesito más de 5 líneas de conceptos?**
    El formulario viene con 5 líneas iniciales de forma predeterminada. Si necesita más, simplemente haga clic en el botón **"Agregar más"** al final de la tabla para abrir nuevas filas.
* **¿Tengo que borrar las filas que no use?**
    No. Si deja una fila completamente en blanco, el sistema la ignorará automáticamente al calcular los totales y generar el documento.
* **¿Para qué sirve la "Factura Provisional"?**
    Le permite descargar o visualizar un borrador exacto de la factura con una marca de agua. Úselo para revisar que los datos, subtotales e impuestos sean correctos antes de emitir el documento definitivo.
* **¿Cómo descargo la factura oficial?**
    Una vez que revise el borrador y esté conforme, haga clic en **"Factura Final"**. Esto generará el PDF oficial sin marcas de agua y lo descargará en su dispositivo.
* **¿Puedo recuperar una factura si cierro el navegador?**
    Sí. Facturas Rey guarda automáticamente su último trabajo. Al regresar a la página de inicio, verá la opción de **"Retomar el trabajo anterior"** con todos los datos tal y como los dejó, o bien **"Volver a descargar"** el último PDF definitivo que haya generado.