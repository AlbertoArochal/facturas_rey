import { NextRequest, NextResponse } from "next/server";
import { execSync } from "child_process";
import path from "path";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const venvPython = path.join(process.cwd(), "venv", "bin", "python3");
    const script = path.join(process.cwd(), "api", "generate_pdf.py");
    const input = JSON.stringify(body);

    const pdfBuffer = execSync(`${venvPython} ${script}`, {
      input,
      maxBuffer: 10 * 1024 * 1024,
    });

    return new NextResponse(pdfBuffer, {
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `attachment; filename="factura_${body.tipo}.pdf"`,
      },
    });
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return NextResponse.json(
      { error: "Error al generar la factura", detalle: msg },
      { status: 500 }
    );
  }
}
