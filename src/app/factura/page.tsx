export default function FacturaPage() {
  return (
    <div className="flex flex-col min-h-screen bg-zinc-50">
      <header className="bg-white border-b border-zinc-200">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-zinc-900">Facturas Rey</h1>
          <a
            href="/"
            className="text-sm text-zinc-500 hover:text-zinc-900 transition-colors"
          >
            Volver al inicio
          </a>
        </div>
      </header>

      <main className="flex-1 max-w-4xl mx-auto w-full px-6 py-8">
        <h2 className="text-xl font-semibold text-zinc-900 mb-8">
          Nueva Factura
        </h2>

        <section className="bg-white rounded-lg border border-zinc-200 p-6 mb-6">
          <h3 className="text-sm font-semibold text-zinc-700 uppercase tracking-wide mb-4">
            Datos del Receptor
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-1">
                Nombre / Razón Social
              </label>
              <input
                type="text"
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-1">
                NIF / CIF
              </label>
              <input
                type="text"
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-zinc-700 mb-1">
                Dirección
              </label>
              <input
                type="text"
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
              />
            </div>
          </div>
        </section>

        <section className="bg-white rounded-lg border border-zinc-200 p-6 mb-6">
          <h3 className="text-sm font-semibold text-zinc-700 uppercase tracking-wide mb-4">
            Conceptos
          </h3>

          {Array.from({ length: 5 }).map((_, i) => (
            <div
              key={i}
              className="grid grid-cols-12 gap-3 mb-2 items-start"
            >
              <div className="col-span-6">
                <input
                  type="text"
                  placeholder="Descripción"
                  className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
                />
              </div>
              <div className="col-span-2">
                <input
                  type="text"
                  placeholder="Cant."
                  className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
                />
              </div>
              <div className="col-span-2">
                <input
                  type="text"
                  placeholder="Precio"
                  className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900"
                />
              </div>
              <div className="col-span-2">
                <input
                  type="text"
                  placeholder="Importe"
                  readOnly
                  className="w-full rounded-md border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-500"
                />
              </div>
            </div>
          ))}

          <button className="mt-3 text-sm text-zinc-600 hover:text-zinc-900 transition-colors">
            + Agregar más
          </button>
        </section>

        <div className="flex gap-3 justify-end">
          <button className="rounded-lg border border-zinc-300 px-6 py-2.5 text-sm font-medium text-zinc-700 hover:bg-zinc-100 transition-colors">
            Factura Provisional
          </button>
          <button className="rounded-lg bg-zinc-900 px-6 py-2.5 text-sm font-medium text-white hover:bg-zinc-800 transition-colors">
            Factura Final
          </button>
        </div>
      </main>
    </div>
  );
}
