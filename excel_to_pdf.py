import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import datetime
import os
from pdf_merger import unir_pdfs

# Ruta del archivo Excel
FILE_PATH = "DatosPrueba.xlsx"


def generar_pdf(df, nombre_pdf, titulo, interno, propietario, placa, saldo=None, totales=None, revisado_por=""):
    """Genera un PDF con encabezado y cálculo del saldo a pagar."""
    c = canvas.Canvas(nombre_pdf, pagesize=landscape(letter))

    # Listas de columnas que requieren formatos especiales
    columnas_monetarias = ["VENTA", "VENTA_NETA", "ANTICIPO", "VALOR", "IMPUESTOS", "BASE"]
    columnas_porcentuales = ["OCUPACION"]

    # Definir anchos fijos para mantener alineación entre reportes
    anchos_fijos = {
        "FECHA": 50, "VIAJE": 42, "TIPO": 60, "RECORRIDO": 150, "VENTA": 60,
        "VENTA_NETA": 80, "OFERTA": 60, "PASAJES": 80, "OCUPACION": 80, "ANTICIPO": 80,
        "CONCEPTO": 150, "VALOR": 80, "BASE": 80, "IMPUESTOS": 80
    }

    # Aplicar anchos fijos a todas las columnas
    max_widths = {col: anchos_fijos.get(col, 80) for col in df.columns}

    def dibujar_encabezado():

        ruta_imagen = "LogoGenerico.png"
        # Dibuja el logo en la ubicacion que desee
        try:
            c.drawImage(ruta_imagen, 680, 500, width=100, height=100, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

        """Dibuja el encabezado y los títulos de las columnas."""
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, 575, "LIQUIDACION DE AFILIADOS")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, 565, "Reporte Financiero de Vehículo")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, 520, f"Vehiculo: {interno} - {placa}")


        # Agregar el nombre de quien revisó el informe (si está disponible)
        if revisado_por:
            c.setFont("Helvetica-Bold", 9)
            c.drawString(575, 510, f"Revisado por: {revisado_por}")

        c.setFont("Helvetica-Bold", 9)  # Ajuste de fuente para que se vea bien
        c.drawString(30, 510, f"Afiliados: {propietario}")

        # Agregar el título SOLO UNA VEZ
        c.setFont("Helvetica-Bold", 9)
        c.drawString(30, 490, titulo)

        c.line(30, 485, 750, 485)  # Línea separadora debajo del título
        c.line(30, 472, 750, 472)  # Línea separadora debajo del título

        # Dibujar encabezados de columnas alineados correctamente
        c.setFont("Helvetica-Bold", 8)
        x_offset = 30
        y_offset = 475
        for col in df.columns:
            c.drawString(x_offset, y_offset, col[:10])
            x_offset += max_widths[col]

        return y_offset - 12

        # Iniciar primera página con encabezado
    y_offset = dibujar_encabezado()
    spacing = 12  # Espaciado entre filas
    max_rows_per_page = 30
    row_count = 0

    # Dibujar datos con ajuste de espacio y paginación automática
    c.setFont("Helvetica", 7)
    for _, row in df.iterrows():
        if row_count >= max_rows_per_page:
            c.showPage()  # Nueva página
            y_offset = dibujar_encabezado()  # Redibujar encabezado en cada página
            c.setFont("Helvetica", 7)  # Restablecer fuente normal
            row_count = 0  # Reiniciar el contador de filas por página

        x_offset = 30
        for col, value in zip(df.columns, row):
            if col in columnas_monetarias:
                try:
                    value = f"${float(value):,.0f}"
                except ValueError:
                    pass
            elif col in columnas_porcentuales:
                try:
                    value = f"{float(value) * 100:.0f}%"
                except ValueError:
                    pass

            c.drawString(x_offset, y_offset, str(value)[:50])  # Mostrar máximo 50 caracteres por celda
            x_offset += max_widths[col]  # Moverse a la siguiente columna
        y_offset -= spacing
        row_count += 1

    # Si hay totales, agregarlos al final sin crear nueva página
    if totales is not None:

        # Dibujar línea superior de los totales
        c.line(30, y_offset - 6, 750, y_offset - 6)
        y_offset -= 15  # Espaciado antes de los totales
        c.setFont("Helvetica", 8)  # Fuente más pequeña y sin negrilla
        c.drawString(30, y_offset, "Total")

        # Asegurar alineación de los totales con sus respectivas columnas
        x_offset = 30
        for col in df.columns:
            if col in totales and col in max_widths:
                total_value = totales[col]
                if col in columnas_monetarias:
                    total_value = f"${total_value:,.0f}"  # Formato dinero
                else:
                    total_value = f"{total_value:,}"  # Formato numérico simple

                c.drawString(x_offset, y_offset, str(total_value))  # Dibujar total alineado

            x_offset += max_widths[col]  # Mover a la siguiente columna
        c.line(30, y_offset - 3, 750, y_offset - 3)

    # Mostrar el saldo a pagar solo en la última página
    if saldo is not None:
        c.showPage()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, 575, "LIQUIDACION DE AFILIADOS")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, 530, "Resumen Financiero")
        c.line(30, 525, 750, 525)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, 500, "Saldo")
        c.setFont("Helvetica-Bold", 15)
        c.drawString(150, 500, f"${saldo:,.0f}")

    c.save()

def generar_reportes():
    """Genera un solo PDF final sin guardar los archivos individuales."""
    df_ventas = pd.read_excel(FILE_PATH, sheet_name="Tabla_ventas")
    df_deducciones = pd.read_excel(FILE_PATH, sheet_name="Tabla_deducciones")
    df_Oingresos = pd.read_excel(FILE_PATH, sheet_name="Otros Ingresos")
    df_impuestos = pd.read_excel(FILE_PATH, sheet_name="Tabla_Impuestos")
    df_OtrasDeducciones = pd.read_excel(FILE_PATH, sheet_name="Otras deducciones")
    df_propietarios = pd.read_excel(FILE_PATH, sheet_name="Propietarios Vehiculos")


    interno = input("Ingrese el número interno del vehículo: ")
    fecha_actual = datetime.datetime.now().strftime("%Y%m%d")  # Formato YYYYMMDD

    propietarios_info = df_propietarios[df_propietarios["INTERNO"] == int(interno)]

    if not propietarios_info.empty:
        # se asegura de que la columna 'NOMBRE AFILIADO' esté correctamente convertida a cadena y luego obtener los valores únicos
        propietarios = propietarios_info["NOMBRE AFILIADO"].apply(str).unique()

        # Si hay más de un propietario, unir los nombres
        if len(propietarios) > 1:
            propietario = " - ".join(propietarios)
        else:
            propietario = propietarios[0]  # Si solo hay uno, solo mostrar ese nombre

        # Obtener la placa correcta
        placa = propietarios_info["PLACA"].values[0]
    else:
        propietario = "N/A"
        placa = "N/A"  # Asignar "N/A" directamente en caso de que no haya propietarios

    # Filtrar datos
    df_ventas_filtrado = df_ventas[df_ventas["INTERNO"] == int(interno)]
    df_deducciones_filtrado = df_deducciones[df_deducciones["INTERNO"] == int(interno)]
    df_Oingresos_filtrado = df_Oingresos[df_Oingresos["INTERNO"] == int(interno)]
    df_impuestos_filtrado = df_impuestos[df_impuestos["INTERNO"] == int(interno)]
    df_OtrasDeducciones_filtrado = df_OtrasDeducciones[df_OtrasDeducciones["INTERNO"] == int(interno)]

    # Eliminar la columna "INTERNO"
    df_ventas_filtrado = df_ventas_filtrado.drop(columns=["INTERNO"])
    df_deducciones_filtrado = df_deducciones_filtrado.drop(columns=["INTERNO"])
    df_Oingresos_filtrado = df_Oingresos_filtrado.drop(columns=["INTERNO"])
    df_impuestos_filtrado = df_impuestos_filtrado.drop(columns=["INTERNO"])
    df_OtrasDeducciones_filtrado = df_OtrasDeducciones_filtrado.drop(columns=["INTERNO"])


    # Calcular totales de las columnas relevantes en el reporte de ventas
    totales_ventas = df_ventas_filtrado[["VENTA", "VENTA_NETA", "ANTICIPO", "OFERTA", "PASAJES"]].sum(min_count=1)

    # Calcular totales para cada reporte
    totales_deducciones = df_deducciones_filtrado[["VALOR"]].sum() if not df_deducciones_filtrado.empty else None
    totales_impuestos = df_impuestos_filtrado[["VALOR", "BASE"]].sum() if not df_impuestos_filtrado.empty else None
    totales_otros_ingresos = df_Oingresos_filtrado[["VALOR"]].sum() if not df_Oingresos_filtrado.empty else None

    # Calcular saldo a pagar
    total_venta_neta = df_ventas_filtrado["VENTA_NETA"].sum()
    total_anticipo = df_ventas_filtrado["ANTICIPO"].sum()
    total_deducciones = df_deducciones_filtrado["VALOR"].sum()
    total_impuestos = df_impuestos_filtrado["VALOR"].sum()
    saldo_pagar = total_venta_neta - total_anticipo - total_deducciones - total_impuestos

    # Crear nombres de archivos temporales
    pdf_ventas = "temp_ventas.pdf"
    pdf_deducciones = "temp_deducciones.pdf"
    pdf_Oingresos = "temp_Oingresos.pdf"
    pdf_impuestos = "temp_impuestos.pdf"
    pdf_Odeducciones = "temp_Odeducciones.pdf"
    pdf_final = f"Reporte_Final_{interno}_{fecha_actual}.pdf"

    print(f"Propietario(s): {propietario}")  # Verificar qué se está almacenando

    revisado_por = input("Ingrese el nombre de quien revisó el informe: ")

    # Generar PDFs individuales
    generar_pdf(df_ventas_filtrado, pdf_ventas, "Reporte de Ventas", interno, propietario, placa, revisado_por=revisado_por, totales=totales_ventas)
    generar_pdf(df_deducciones_filtrado, pdf_deducciones, "Reporte de Deducciones", interno, propietario, placa, totales=totales_deducciones)
    generar_pdf(df_impuestos_filtrado, pdf_impuestos, "Reporte de Impuestos", interno, propietario, placa, totales=totales_impuestos)
    generar_pdf(df_Oingresos_filtrado, pdf_Oingresos, "Otros ingresos", interno, propietario, placa, totales=totales_otros_ingresos, saldo=saldo_pagar)
    generar_pdf(df_OtrasDeducciones_filtrado, pdf_Odeducciones, "Otras deducciones", interno, propietario, placa)

    # Unir PDFs en el archivo final
    unir_pdfs(pdf_final, pdf_ventas, pdf_deducciones, pdf_impuestos, pdf_Odeducciones, pdf_Oingresos)

    print(f" Reporte final generado: {pdf_final}")
    return pdf_final