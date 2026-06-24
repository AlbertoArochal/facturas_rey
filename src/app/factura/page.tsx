export default function FacturaPage() {
  return (
    <div className="flex flex-col min-h-screen bg-base">
      <header className="bg-mantle border-b border-surface-0">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <h1 className="text-xl font-bold text-text">Facturas Rey</h1>
          <a
            href="/"
            className="text-sm text-overlay-1 hover:text-text transition-colors"
          >
            Volver al inicio
          </a>
        </div>
      </header>

      <main className="flex-1 max-w-4xl mx-auto w-full px-6 py-8 space-y-6">
        <h2 className="text-lg font-semibold text-text">Nueva Factura</h2>

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
                className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-subtext-0 mb-1.5">
                NIF / CIF
              </label>
              <input
                type="text"
                className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-subtext-0 mb-1.5">
                Dirección
              </label>
              <input
                type="text"
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
            <div className="col-span-6">
              <span className="text-xs text-overlay-1 uppercase tracking-wider">
                Descripción
              </span>
            </div>
            <div className="col-span-2">
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

          {Array.from({ length: 5 }).map((_, i) => (
            <div
              key={i}
              className="grid grid-cols-12 gap-3 mb-2"
            >
              <div className="col-span-12 sm:col-span-6">
                <input
                  type="text"
                  placeholder="Descripción"
                  className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
                />
              </div>
              <div className="col-span-4 sm:col-span-2">
                <input
                  type="text"
                  placeholder="0"
                  className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
                />
              </div>
              <div className="col-span-4 sm:col-span-2">
                <input
                  type="text"
                  placeholder="0.00"
                  className="w-full rounded-lg border border-surface-1 bg-surface-0 px-3 py-2 text-sm text-text placeholder-overlay-1 focus:outline-none focus:ring-2 focus:ring-mauve focus:border-transparent transition-all"
                />
              </div>
              <div className="col-span-4 sm:col-span-2">
                <input
                  type="text"
                  placeholder="0.00"
                  readOnly
                  className="w-full rounded-lg border border-surface-0 bg-crust px-3 py-2 text-sm text-overlay-2"
                />
              </div>
            </div>
          ))}

          <button className="mt-3 text-sm text-mauve hover:text-lavender transition-colors">
            + Agregar más
          </button>
        </section>

        <div className="flex gap-3 justify-end">
          <button className="rounded-lg border border-surface-1 px-6 py-2.5 text-sm font-medium text-subtext-0 hover:bg-surface-0 hover:text-text transition-all">
            Factura Provisional
          </button>
          <button className="rounded-lg bg-green text-base px-6 py-2.5 text-sm font-medium hover:brightness-110 transition-all">
            Factura Final
          </button>
        </div>
      </main>
    </div>
  );
}
