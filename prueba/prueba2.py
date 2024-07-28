import fitz
import re


def edit_pdf_placeholders(input_pdf, output_pdf, replacements):
    # Abrir el documento
    doc = fitz.open(input_pdf)

    # Iterar sobre cada página del documento
    for page in doc:
        # Obtener el texto de la página
        text = page.get_text()

        # Buscar todos los placeholders (texto entre corchetes)
        placeholders = re.findall(r"\[([^\]]+)\]", text)

        # Reemplazar cada placeholder encontrado
        for placeholder in placeholders:
            if placeholder in replacements:
                # Buscar el texto exacto incluyendo los corchetes
                search_text = f"[{placeholder}]"
                # Reemplazar con el nuevo texto
                instances = page.search_for(search_text)
                for inst in instances:
                    page.add_redact_annot(inst)
                    page.apply_redactions()
                    # Usar Century Gothic con tamaño 11
                    page.insert_text(
                        inst.tl,
                        replacements[placeholder],
                        fontfile=r"E:\DesarrolloWeb\Django\prueba\OpenSans-Regular.ttf",
                        fontsize=8,
                        color=(0, 0, 0),
                    )

    # Guardar el documento modificado
    doc.save(output_pdf)
    doc.close()


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

# Uso de la función
edit_pdf_placeholders("base3.pdf", "Boleto_Modificado.pdf", replacements)
