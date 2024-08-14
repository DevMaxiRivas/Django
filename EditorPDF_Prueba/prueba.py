from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def create_grid_pdf(output_filename):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    # Definir dimensiones de la grilla
    grid_width = width / 2
    grid_height = height / 2

    # 1. Cuadrante superior izquierdo: Logo
    # Asumiendo que tienes un archivo de logo llamado 'logo.png'
    c.drawImage(
        "logo.png",
        0,
        grid_height,
        width=grid_width,
        height=grid_height,
        preserveAspectRatio=True,
    )

    # 2. Cuadrante superior derecho: "Todo listo para tu viaje en tren..."
    c.setFont("Helvetica-Bold", 14)
    c.drawString(
        grid_width + 0.5 * inch, height - 1 * inch, "Todo listo para tu viaje en tren"
    )

    c.setFont("Helvetica", 10)
    instructions = [
        "Llega a la estación con anticipación y sigue estos pasos:",
        "1. Deja tu equipaje en el área designada",
        "2. Dirígete al control de boletos",
        "3. Busca tu andén de embarque",
        "4. Confirma tu asiento",
    ]
    for i, inst in enumerate(instructions):
        c.drawString(grid_width + 0.5 * inch, height - (1.5 + i * 0.3) * inch, inst)

    # 3. Cuadrante inferior izquierdo: "En este viaje puedes llevar..."
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.5 * inch, grid_height - 0.5 * inch, "En este viaje puedes llevar:")

    c.setFont("Helvetica", 10)
    luggage_info = [
        "1 Bolso o mochila pequeña: bajo el asiento delantero",
        "Medidas recomendadas: 45 cm x 35 cm x 20 cm",
        "",
        "1 equipaje de mano:",
        "Medidas recomendadas: 55 cm x 35 cm x 25 cm",
    ]
    for i, info in enumerate(luggage_info):
        c.drawString(0.5 * inch, grid_height - (1 + i * 0.3) * inch, info)

    # 4. Cuadrante inferior derecho: Detalles del Boleto
    c.setFillColorRGB(0.9, 0.9, 0.9)  # Color de fondo gris claro
    c.rect(grid_width, 0, grid_width, grid_height, fill=1)

    c.setFillColorRGB(0, 0, 0)  # Volver a color negro para el texto
    c.setFont("Helvetica-Bold", 12)
    c.drawString(
        grid_width + 0.5 * inch, grid_height - 0.5 * inch, "Nº de orden: LA5443826RFTU"
    )
    c.drawString(grid_width + 0.5 * inch, grid_height - 0.8 * inch, "Cristian Martinez")

    c.setFont("Helvetica", 10)
    ticket_info = [
        "Vuelo: LA525",
        "23 jul. 2024",
        "Operado por LATAM Airlines",
        "Lima -> Santiago de Chile",
        "14:40 -> 19:20",
        "Asiento: 14E",
        "Terminal: 1",
        "Grupo de embarque: 5",
    ]
    for i, info in enumerate(ticket_info):
        c.drawString(
            grid_width + 0.5 * inch, grid_height - (1.2 + i * 0.3) * inch, info
        )

    c.save()


create_grid_pdf("boleto_grilla.pdf")
