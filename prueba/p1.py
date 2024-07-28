import fitz

# Ruta al archivo de la fuente
fontfile = r"E:\DesarrolloWeb\Django\prueba\GOTHIC.TTF"

# Verificar si el archivo existe
import os

if not os.path.exists(fontfile):
    print(f"Error: El archivo de fuente {fontfile} no existe.")
else:
    # Cargar un PDF para pruebas
    doc = fitz.open("Boleto_Modificado.pdf")  # Cambia a la ruta de tu PDF
    page = doc[0]

    # Inserta texto usando la fuente personalizada
    try:
        page.insert_text((72, 72), "Ejemplo de texto", fontfile=fontfile, fontsize=12)
        doc.save("output.pdf")
        print("Texto insertado correctamente.")
    except Exception as e:
        print(f"Ocurrió un error al insertar el texto: {e}")
    finally:
        doc.close()
