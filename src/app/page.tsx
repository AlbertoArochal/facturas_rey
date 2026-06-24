"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Home() {
  const [tieneDatos, setTieneDatos] = useState(false);
  const [tienePdf, setTienePdf] = useState(false);

  useEffect(() => {
    setTieneDatos(localStorage.getItem("factura_datos") !== null);
    setTienePdf(localStorage.getItem("factura_ultimo_pdf") !== null);
  }, []);

  const descargarUltimoPdf = () => {
    const b64 = localStorage.getItem("factura_ultimo_pdf");
    if (!b64) return;
    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    const blob = new Blob([bytes], { type: "application/pdf" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "factura.pdf";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col min-h-screen bg-base">
      <header className="bg-mantle border-b border-surface-0">
        <div className="max-w-4xl mx-auto px-6 py-5">
          <h1 className="text-xl font-bold text-text">Facturas Rey</h1>
          <p className="text-sm text-overlay-0">
            Generación y gestión de facturas
          </p>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-6">
        <div className="max-w-md w-full text-center space-y-8">
          <div className="space-y-2">
            <h2 className="text-3xl font-semibold text-text">Bienvenido</h2>
            <p className="text-subtext-0">
              Genere facturas profesionales de forma rápida y sencilla.
            </p>
          </div>

          <Link
            href="/factura"
            className="inline-block w-full rounded-lg bg-mauve px-6 py-3 text-base font-medium text-base hover:brightness-110 transition-all"
          >
            Generar Factura
          </Link>

          {(tieneDatos || tienePdf) && (
            <div className="border-t border-surface-0 pt-8 mt-8 space-y-3">
              <p className="text-sm text-overlay-1">
                Su última factura está guardada.
              </p>
              <div className="flex gap-3">
                {tieneDatos && (
                  <Link
                    href="/factura"
                    className="flex-1 rounded-lg border border-surface-1 px-4 py-2 text-sm text-subtext-0 hover:bg-surface-0 transition-colors"
                  >
                    Retomar trabajo
                  </Link>
                )}
                {tienePdf && (
                  <button
                    onClick={descargarUltimoPdf}
                    className="flex-1 rounded-lg border border-surface-1 px-4 py-2 text-sm text-subtext-0 hover:bg-surface-0 transition-colors"
                  >
                    Descargar último PDF
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="border-t border-surface-0 py-4">
        <p className="text-center text-xs text-overlay-0">
          &copy; {new Date().getFullYear()} Facturas Rey
        </p>
      </footer>
    </div>
  );
}
