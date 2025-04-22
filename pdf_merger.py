from pypdf import PdfWriter
import os

def unir_pdfs(pdf_final, *archivos):
    """Une los PDFs de ventas, deducciones e impuestos en un solo archivo y luego los elimina."""

    # Crea un objeto PdfWriter, que nos permite combinar archivos PDF
    writer = PdfWriter()

    # Filtra los archivos recibidos: solo incluye los que existen en el sistema
    archivos_existentes = [pdf for pdf in archivos if os.path.exists(pdf)]  # Solo usar los que existen

    # Si no se encontró ningún archivo existente, muestra un mensaje de error y termina la función
    if not archivos_existentes:
        print("❌ Error: No hay archivos temporales para unir. El reporte puede estar incompleto.")
        return

    # Recorre cada PDF existente y lo agrega al objeto writer
    for pdf in archivos_existentes:
        with open(pdf, "rb") as f:  # Abre el archivo en modo binario de solo lectura
            writer.append(f)        # Agrega el contenido del PDF al escritor

    # Guarda el PDF final combinando todos los archivos previos
    with open(pdf_final, "wb") as output_pdf:
        writer.write(output_pdf)  # Escribe el contenido combinado en un nuevo archivo

    print(f"Reporte final exportado como {pdf_final}")

    # Elimina cada uno de los archivos temporales que fueron usados
    for pdf in archivos_existentes:
        os.remove(pdf)
        print(f" Archivo eliminado: {pdf}")
