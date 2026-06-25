"use client";

import Link from "next/link";
import { ArrowLeft, FileText, FileCheck, Plus, Trash2, Lightbulb } from "lucide-react";

export default function AyudaPage() {
  return (
    <div className="flex flex-col min-h-screen bg-base">
      <header className="bg-mantle border-b border-surface-0">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-4 sm:py-5 flex items-center gap-3">
          <Link
            href="/"
            className="text-overlay-1 hover:text-text transition-colors p-1"
            aria-label="Volver al inicio"
          >
            <ArrowLeft size={20} />
          </Link>
          <h1 className="text-lg sm:text-xl font-bold text-text">Ayuda</h1>
        </div>
      </header>

      <main className="flex-1 max-w-3xl mx-auto w-full px-4 sm:px-6 py-6 sm:py-10 space-y-8">
        <section>
          <h2 className="text-base sm:text-lg font-semibold text-text mb-3">
            Cómo generar una factura paso a paso
          </h2>
          <p className="text-subtext-0 text-sm leading-relaxed">
            Sigue estos pasos para crear una factura profesional desde el móvil o el ordenador.
          </p>
        </section>

        <ol className="space-y-6">
          <li className="bg-mantle rounded-xl border border-surface-0 p-4 sm:p-5">
            <div className="flex items-start gap-3">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-mauve text-base flex items-center justify-center text-sm font-bold">1</span>
              <div>
                <h3 className="text-sm font-semibold text-text">Rellena los datos del cliente</h3>
                <p className="text-subtext-0 text-sm mt-1 leading-relaxed">
                  En la pantalla de factura, introduce el <strong>nombre</strong>, <strong>dirección</strong>, <strong>teléfono</strong>, <strong>número de factura</strong> y la <strong>diagnosis</strong> (descripción del trabajo). Todos los campos son importantes para que la factura quede completa.
                </p>
              </div>
            </div>
          </li>

          <li className="bg-mantle rounded-xl border border-surface-0 p-4 sm:p-5">
            <div className="flex items-start gap-3">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-mauve text-base flex items-center justify-center text-sm font-bold">2</span>
              <div>
                <h3 className="text-sm font-semibold text-text">Añade los conceptos</h3>
                <p className="text-subtext-0 text-sm mt-1 leading-relaxed">
                  Pulsa el botón <strong className="inline-flex items-center gap-1 text-mauve"><Plus size={14} /> Agregar concepto</strong> para añadir líneas. Para cada concepto indica:
                </p>
                <ul className="list-disc list-inside text-subtext-0 text-sm mt-2 space-y-1">
                  <li><strong>Descripción</strong>: nombre del producto o servicio</li>
                  <li><strong>Tipo</strong>: Material o Mano de Obra</li>
                  <li><strong>Cantidad</strong>: número de unidades</li>
                  <li><strong>Precio</strong>: precio unitario</li>
                </ul>
                <p className="text-subtext-0 text-sm mt-2">
                  El importe se calcula automáticamente. En el móvil puedes eliminar una línea con el icono <Trash2 size={14} className="inline text-red" />.
                </p>
              </div>
            </div>
          </li>

          <li className="bg-mantle rounded-xl border border-surface-0 p-4 sm:p-5">
            <div className="flex items-start gap-3">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-mauve text-base flex items-center justify-center text-sm font-bold">3</span>
              <div>
                <h3 className="text-sm font-semibold text-text">Genera la factura</h3>
                <p className="text-subtext-0 text-sm mt-1 leading-relaxed">
                  Tienes dos opciones al final de la página:
                </p>
                <div className="flex flex-col sm:flex-row gap-3 mt-3">
                  <div className="flex-1 rounded-lg border border-surface-1 p-3">
                    <div className="flex items-center gap-2 text-subtext-0 text-sm font-medium">
                      <FileText size={16} /> Factura Provisional
                    </div>
                    <p className="text-xs text-overlay-1 mt-1">
                      Genera un borrador con marca de agua <strong>PROVISIONAL</strong>. Útil para presupuestos o revisiones.
                    </p>
                  </div>
                  <div className="flex-1 rounded-lg border border-green/30 bg-green/5 p-3">
                    <div className="flex items-center gap-2 text-green text-sm font-medium">
                      <FileCheck size={16} /> Factura Final
                    </div>
                    <p className="text-xs text-overlay-1 mt-1">
                      Genera la factura definitiva sin marcas de agua, lista para entregar al cliente.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </li>

          <li className="bg-mantle rounded-xl border border-surface-0 p-4 sm:p-5">
            <div className="flex items-start gap-3">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-mauve text-base flex items-center justify-center text-sm font-bold">4</span>
              <div>
                <h3 className="text-sm font-semibold text-text">Descarga y comparte</h3>
                <p className="text-subtext-0 text-sm mt-1 leading-relaxed">
                  El PDF se descarga automáticamente a tu dispositivo. También puedes retomar el trabajo más tarde: los datos se guardan automáticamente en el navegador.
                </p>
              </div>
            </div>
          </li>
        </ol>

        <section className="bg-mantle rounded-xl border border-surface-0 p-4 sm:p-5">
          <h3 className="text-sm font-semibold text-text mb-3 flex items-center gap-2">
            <Lightbulb size={16} className="text-yellow" /> Consejos rápidos
          </h3>
          <ul className="space-y-2 text-subtext-0 text-sm">
            <li className="flex items-start gap-2">
              <span className="text-mauve mt-0.5">•</span>
              <span>En el móvil, usa el teclado numérico al introducir cantidades y precios.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-mauve mt-0.5">•</span>
              <span>Si cierras la página accidentalmente, vuelve a abrirla y pulsa <strong>Retomar trabajo</strong> en la pantalla de inicio.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-mauve mt-0.5">•</span>
              <span>El IGIC del 7% se aplica automáticamente sobre el total de material y mano de obra.</span>
            </li>
          </ul>
        </section>

        <div className="text-center pt-4">
          <Link
            href="/factura?nuevo=1"
            className="inline-block w-full sm:w-auto rounded-xl bg-mauve px-8 py-4 text-lg font-medium text-base hover:brightness-110 transition-all shadow-lg min-h-[56px] flex items-center justify-center"
          >
            Ir a generar factura
          </Link>
        </div>
      </main>
    </div>
  );
}
