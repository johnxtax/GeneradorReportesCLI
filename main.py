from excel_to_pdf import generar_reportes

if __name__ == "__main__":
    pdf_final = generar_reportes()  # Capturar correctamente el nombre del PDF final

    if pdf_final:  # Asegurar que pdf_final no es None
        print(f"✅ Reporte generado exitosamente: {pdf_final}")
    else:
        print("❌ Error: No se generó el reporte final correctamente.")