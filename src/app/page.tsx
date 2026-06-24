import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-zinc-50">
      <header className="bg-white border-b border-zinc-200">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-zinc-900">Facturas Rey</h1>
          <p className="text-sm text-zinc-500">Generación y gestión de facturas</p>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-6">
        <div className="max-w-md w-full text-center space-y-6">
          <div className="space-y-2">
            <h2 className="text-3xl font-semibold text-zinc-900">
              Bienvenido
            </h2>
            <p className="text-zinc-600">
              Genere facturas profesionales de forma rápida y sencilla.
            </p>
          </div>

          <Link
            href="/factura"
            className="inline-block w-full rounded-lg bg-zinc-900 px-6 py-3 text-white font-medium hover:bg-zinc-800 transition-colors"
          >
            Generar Factura
          </Link>

          <div className="border-t border-zinc-200 pt-6 mt-6">
            <p className="text-sm text-zinc-400">
              Sus facturas se guardan automáticamente.
              Puede retomar su trabajo o descargar el último PDF desde aquí.
            </p>
          </div>
        </div>
      </main>

      <footer className="border-t border-zinc-200 py-4">
        <p className="text-center text-xs text-zinc-400">
          &copy; {new Date().getFullYear()} Facturas Rey
        </p>
      </footer>
    </div>
  );
}
