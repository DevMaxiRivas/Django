from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfrw import PdfReader, PdfWriter, PageMerge
import io

# Registrar la fuente personalizada
pdfmetrics.registerFont(
    TTFont("CenturyGothic", r"E:\DesarrolloWeb\Django\prueba\GOTHIC.TTF")
)

# Diccionario con los reemplazos
replacements = {
    "Id-venta": "LA5443826RFTU",
    "Nombre Pasajero": "Cristian Martinez",
    "Id-ticket": "LA525",
    "Estación Salida": "Salta",
    "Estación Llegada": "San Antonio de los Cobres",
    "Id-Asiento": "14E",
    "Categoria de Asiento": "Economy",
    "Horario Espera": "13:40",
    "Horario Salida": "14:20",
    "Fecha de Emisión": "21/7/24, 17:07",
    "Enlace-al-Sitio-Web": "https://www.trenalasnubes.com.ar",
}


def replace_text(input_pdf, output_pdf, replacements):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        # Crear una nueva capa para los reemplazos en memoria
        packet = io.BytesIO()
        overlay = canvas.Canvas(packet, pagesize=letter)
        overlay.setFont("CenturyGothic", 9)

        # Aquí puedes ajustar las coordenadas según sea necesario
        for placeholder, replacement in replacements.items():
            # Aquí deberías ajustar las coordenadas (x, y) para el texto
            # Por ejemplo, estos valores son solo ilustrativos
            x, y = 100, 750
            overlay.drawString(x, y, replacement)

        overlay.save()
        packet.seek(0)

        # Leer el PDF de la capa desde el buffer de memoria
        overlay_pdf = PdfReader(packet)
        merger = PageMerge(page)
        merger.add(overlay_pdf.pages[0]).render()

        writer.addpage(page)

    writer.write(output_pdf)


replace_text("base2.pdf", "Boleto_Modificado2.pdf", replacements)
