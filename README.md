# Generador de Extractos Vehiculares en PDF

Este proyecto fue desarrollado como parte de una solución para automatizar la generación de extractos financieros basados en placas vehiculares, utilizando información proveniente de una base de datos simulada en Excel. El objetivo es exportar dichos extractos en formato PDF con estructura profesional.

## Tecnologías Utilizadas principales 
En los requerimientos están todas las librerias usadas en este proyecto, en este caso se usó con un .xls de prueba, pero si se desea usar con una base de datos, es importar la libreria correspondiente y crear un archivo con las credenciales de conexión. 

- Python 
- [pandas](https://pandas.pydata.org/) - para la manipulación de datos
- [reportlab](https://www.reportlab.com/) - para la creación de archivos PDF
- [PyPDF2](https://github.com/py-pdf/PyPDF2) - para combinar múltiples PDFs
- [numpy](https://numpy.org/) - soporte para cálculos y estructuras de datos

## Estructura del Proyecto

📁 extractos_vehiculares_pdf 
  
  ┣ 📄 main.py # Punto de entrada del programa 
  
  ┣ 📄 excel_to_pdf.py # Lógica para convertir Excel a PDF 
  
  ┣ 📄 pdf_merger.py # Función para combinar PDFs (ventas + deducciones + impuestos) 
  
  ┣ 📄 requirements.txt # Dependencias del proyecto 
  
  ┣ 📄 .gitignore # Archivos que no se deben versionar 
  
  ┗ 📁 DatosPrueba.xlsx # archivo simulado sin datos sensibles > ⚠️ Los archivos originales con datos sensibles han sido retirados por privacidad.

## Funcionalidades

- Lectura de datos desde archivos Excel.
- Generación de reportes financieros en PDF.
- Cálculo automático de saldo a pagar: Saldo a pagar = Venta neta - Anticipo - Deducciones - Impuestos
- Inclusión de encabezado y formato personalizado.
- Unificación de múltiples PDFs en un solo documento final.

## Cómo usar el proyecto

1. Clona el repositorio:
 ```bash
 git clone https://github.com/johnxtax/GeneradorReportesCLI.git
 cd nombre-del-repositorio

2. Crea un entorno virtual (Pycharm lo crea automaticamente) 
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

3. Instala las dependencias 
pip install -r requirements.txt

4. Ejecuta el programa principal 
python main.py

⚠️ Asegúrate de tener tus propios archivos de Excel o base de datos estructurados según el formato esperado.

## Participación en el proyecto

Este desarrollo fue parte de una propuesta técnica para una solución real de negocio. Aunque no fue seleccionado como implementación final, el proyecto quedó funcional como prueba de concepto.
##Licencia

Este proyecto se comparte con fines educativos y demostrativos. No incluye datos reales ni el logotipo oficial de ninguna empresa.

