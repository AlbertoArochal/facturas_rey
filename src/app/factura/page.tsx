"use client";

import { Suspense, useEffect, useState, useCallback, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";

type Concepto = {
  descripcion: string;
  cantidad: string;
  precio: string;
  tipo: "material" | "mano_obra";
};

function parseNum(val: string): number {
  if (!val.trim()) return 0;
  const n = parseFloat(val.replace(",", "."));
  return isNaN(n) ? 0 : n;
}

function fmtImporte(val: number): string {
  return val.toFixed(2);
}

const INITIAL_CONCEPTOS: Concepto[] = Array.from({ length: 5 }, () => ({
  descripcion: "",
  cantidad: "",
  precio: "",
  tipo: "material",
}));

function FacturaForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const esNuevo = searchParams.get("nuevo") === "1";

  const [receptor, setReceptor] = useState({
    nombre: "",
    nif: "",
    direccion: "",
    telefono: "",
    diagnosis: "",
    num_factura: "",
  });

  const [conceptos, setConceptos] = useState<Concepto[]>(INITIAL_CONCEPTOS);

  const [errores, setErrores] = useState<Record<string, string>>({});
  const cargadoRef = useRef(false);

  useEffect(() => {
    if (esNuevo) {
      localStorage.removeItem("factura_datos");
      setReceptor({
        nombre: "",
        nif: "",
        direccion: "",
        telefono: "",
        diagnosis: "",
        num_factura: "",
      });
      setConceptos(INITIAL_CONCEPTOS);
      cargadoRef.current = true;
      return;
    }
    const raw = localStorage.getItem("factura_datos");
    if (raw) {
      try {
        const data = JSON.parse(raw);
        if (data.receptor) setReceptor(data.receptor);
        if (data.conceptos) setConceptos(data.conceptos);
      } catch {
        /* ignore */
      }
    }
    cargadoRef.current = true;
  }, [esNuevo]);

  const guardar = useCallback(() => {
    if (!cargadoRef.current) return;
    localStorage.setItem(
      "factura_datos",
      JSON.stringify({ receptor, conceptos })
    );
  }, [receptor, conceptos]);

  useEffect(() => {
    guardar();
  }, [guardar]);

  const actualizarReceptor = (campo: keyof typeof receptor, val: string) => {
    setReceptor((prev) => ({ ...prev, [campo]: val }));
  };

  const actualizarConcepto = (
    idx: number,
    campo: keyof Concepto,
    val: string
  ) => {
    setConceptos((prev) => {
      const copy = [...prev];
      copy[idx] = { ...copy[idx], [campo]: val };
      return copy;
    });
    setErrores((prev) => {
      const next = { ...prev };
      delete next[`conc_${idx}`];
      return next;
    });
  };

  const agregarFila = () => {
    setConceptos((prev) => [
      ...prev,
      { descripcion: "", cantidad: "", precio: "", tipo: "material" },
    ]);
  };

  const validar = (): Concepto[] | null => {
    const nuevosErrores: Record<string, string> = {};
    const validos: Concepto[] = [];

    conceptos.forEach((c, i) => {
      const tieneDesc = c.descripcion.trim().length > 0;
      const tieneCant = c.cantidad.trim().length > 0;
      const tienePrecio = c.precio.trim().length > 0;

      if (!tieneDesc && !tieneCant && !tienePrecio) return;

      if (tieneDesc && (!tieneCant || !tienePrecio)) {
        nuevosErrores[`conc_${i}`] = "Campos obligatorios faltantes";
        return;
      }

      if (tieneCant && isNaN(parseNum(c.cantidad))) {
        nuevosErrores[`conc_${i}`] = "Cantidad no válida";
        return;
      }
      if (tienePrecio && isNaN(parseNum(c.precio))) {
        nuevosErrores[`conc_${i}`] = "Precio no válido";
        return;
      }

      validos.push(c);
    });

    setErrores(nuevosErrores);
    return Object.keys(nuevosErrores).length === 0 ? validos : null;
  };

  const generar = async (tipo: "provisional" | "final") => {
    const conceptosValidos = validar();
    if (!conceptosValidos) return;

    const body = {
      tipo,
      receptor,
      conceptos: conceptosValidos.map((c) => ({
        descripcion: c.descripcion,
        cantidad: parseNum(c.cantidad),
        precio: parseNum(c.precio),
        tipo: c.tipo,
        descuento: 0,
      })),
    };

    try {
      const res = await fetch("/api/generar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!res.ok) throw new Error("Error al generar factura");

      const blob = await res.blob();
      const b64 = await new Promise<string>((resolve) => {
        const reader = new FileReader();
        reader.onload = () => {
          const result = reader.result as string;
          resolve(result.split(",")[1]);
        };
        reader.readAsDataURL(blob);
      });
      localStorage.setItem("factura_ultimo_pdf", b64);

      const url = URL.createObjectURL(blob);
      if (tipo === "provisional") {
        const a = document.createElement("a");
        a.href = url;
        a.download = `factura_provisional.pdf`;
        a.click();
        window.open(url, "_blank");
      } else {
        const a = document.createElement("a");
        a.href = url;
        a.download = `factura_${tipo}.pdf`;
        a.click();
      }
      URL.revokeObjectURL(url);
    } catch {
      setErrores((prev) => ({
        ...prev,
        global: "Error al generar la factura. Intente de nuevo.",
      }));
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-base">
      <header className="bg-mantle border-b border-surface-0">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <h1 className="text-xl font-bold text-text">Facturas Rey</h1>
          <button
            onClick={() => router.push("/")}
            className="text-sm text-overlay-1 hover:text-text transition-colors"
          >
            Volver al inicio
          </button>
        </div>
      </header>

      <main className="flex-1 max-w-4xl mx-auto w-full px-6 py-8 space-y-6">
        <h2 className="text-lg font-semibold text-text">Nueva Factura</h2>

        {errores.global && (
          <div className="rounded-lg bg-red/10 border border-red px-4 py-3 text-sm text-red">
            {errores.global}
          </div>
        )}

        <section className="bg-mantle rounded-xl border border-surface-0 p-6">
          <h3 className="text-xs font-semibold text-overlay-1 uppercase tracking-wider mb-4">
            Datos del Receptor
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-subtext-0 mb-1.5">
                Nombre / Razón Social
              </label>
              <input
                type="text"
                value={receptor.nombre}
                onChange={(e) => actualizarReceptor("nombre", e.target.value)}
                className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-subtext-0 mb-1.5">
                NIF / CIF
              </label>
              <input
                type="text"
                value={receptor.nif}
                onChange={(e) => actualizarReceptor("nif", e.target.value)}
                className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-subtext-0 mb-1.5">
                Dirección
              </label>
              <input
                type="text"
                value={receptor.direccion}
                onChange={(e) => actualizarReceptor("direccion", e.target.value)}
                className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-subtext-0 mb-1.5">
                Teléfono
              </label>
              <input
                type="text"
                value={receptor.telefono}
                onChange={(e) => actualizarReceptor("telefono", e.target.value)}
                className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-subtext-0 mb-1.5">
                Nº Factura
              </label>
              <input
                type="text"
                value={receptor.num_factura}
                onChange={(e) => actualizarReceptor("num_factura", e.target.value)}
                className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-subtext-0 mb-1.5">
                Diagnosis
              </label>
              <input
                type="text"
                value={receptor.diagnosis}
                onChange={(e) => actualizarReceptor("diagnosis", e.target.value)}
                className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
              />
            </div>
          </div>
        </section>

        <section className="bg-mantle rounded-xl border border-surface-0 p-6">
          <h3 className="text-xs font-semibold text-overlay-1 uppercase tracking-wider mb-4">
            Conceptos
          </h3>

          <div className="hidden sm:grid grid-cols-12 gap-3 mb-2 px-3">
            <div className="col-span-5">
              <span className="text-xs text-overlay-1 uppercase tracking-wider">
                Descripción
              </span>
            </div>
            <div className="col-span-2">
              <span className="text-xs text-overlay-1 uppercase tracking-wider">
                Tipo
              </span>
            </div>
            <div className="col-span-1">
              <span className="text-xs text-overlay-1 uppercase tracking-wider">
                Cant.
              </span>
            </div>
            <div className="col-span-2">
              <span className="text-xs text-overlay-1 uppercase tracking-wider">
                Precio
              </span>
            </div>
            <div className="col-span-2">
              <span className="text-xs text-overlay-1 uppercase tracking-wider">
                Importe
              </span>
            </div>
          </div>

          {conceptos.map((c, i) => {
            const importe = parseNum(c.cantidad) * parseNum(c.precio);
            return (
              <div key={i}>
                <div className="grid grid-cols-12 gap-3 mb-1">
                  <div className="col-span-12 sm:col-span-5">
                    <input
                      type="text"
                      value={c.descripcion}
                      onChange={(e) =>
                        actualizarConcepto(i, "descripcion", e.target.value)
                      }
                      placeholder="Descripción"
                      className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
                    />
                  </div>
                  <div className="col-span-7 sm:col-span-2">
                    <select
                      value={c.tipo}
                      onChange={(e) =>
                        actualizarConcepto(
                          i,
                          "tipo",
                          e.target.value as "material" | "mano_obra"
                        )
                      }
                      className="w-full rounded-lg border border-surface-1 bg-surface-0 px-2 py-2 text-sm text-text focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
                    >
                      <option value="material">Material</option>
                      <option value="mano_obra">Mano de Obra</option>
                    </select>
                  </div>
                  <div className="col-span-3 sm:col-span-1">
                    <input
                      type="text"
                      value={c.cantidad}
                      onChange={(e) =>
                        actualizarConcepto(i, "cantidad", e.target.value)
                      }
                      placeholder="0"
                      className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
                    />
                  </div>
                  <div className="col-span-5 sm:col-span-2">
                    <input
                      type="text"
                      value={c.precio}
                      onChange={(e) =>
                        actualizarConcepto(i, "precio", e.target.value)
                      }
                      placeholder="0.00"
                      className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
                    />
                  </div>
                  <div className="col-span-4 sm:col-span-2">
                    <input
                      type="text"
                      value={fmtImporte(importe)}
                      readOnly
                      className="w-full rounded-lg border border-surface-0 bg-crust px-3 py-2 text-sm text-overlay-2"
                    />
                  </div>
                </div>
                {errores[`conc_${i}`] && (
                  <p className="text-xs text-red mb-1 col-span-12">
                    {errores[`conc_${i}`]}
                  </p>
                )}
              </div>
            );
          })}

          <button
            onClick={agregarFila}
            className="mt-3 text-sm text-mauve hover:text-lavender transition-colors"
          >
            + Agregar más
          </button>
        </section>

        <div className="flex gap-3 justify-end">
          <button
            onClick={() => generar("provisional")}
            className="rounded-lg border border-surface-1 px-6 py-2.5 text-sm font-medium text-subtext-0 hover:bg-surface-0 hover:text-text transition-all"
          >
            Factura Provisional
          </button>
          <button
            onClick={() => generar("final")}
            className="rounded-lg bg-green text-base px-6 py-2.5 text-sm font-medium hover:brightness-110 transition-all"
          >
            Factura Final
          </button>
        </div>
      </main>
    </div>
  );
}

export default function FacturaPage() {
  return (
    <Suspense fallback={<div className="flex min-h-screen bg-base items-center justify-center text-text text-lg">Cargando...</div>}>
      <FacturaForm />
    </Suspense>
  );
}
