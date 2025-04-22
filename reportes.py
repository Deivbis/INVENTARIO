import os
import sys
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from venta_backend import SessionLocal, Movimiento, Venta, DetalleVenta, Producto, Cliente
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime
from RUTAS import ruta_absoluta

# Obtener nuevo ID de reporte desde archivo
def obtener_nuevo_id_reporte():
    archivo_id = 'ultimo_id_reporte.txt'

    # Si el archivo no existe, crear uno con el ID inicial de 1
    if not os.path.exists(archivo_id):
        with open(archivo_id, 'w') as f:
            f.write('1')
        return 1
    else:
        # Si el archivo existe, leer el último ID, incrementar y actualizar el archivo
        with open(archivo_id, 'r+') as f:
            ultimo_id = int(f.read())  # Leer el último ID
            nuevo_id = ultimo_id + 1   # Incrementar el ID
            f.seek(0)                  # Regresar al inicio del archivo
            f.write(str(nuevo_id))     # Guardar el nuevo ID
            f.truncate()               # Eliminar cualquier dato residual
        return nuevo_id


def generar_reporte_movimientos():
    session = SessionLocal()

    # Consultar los movimientos
    movimientos = session.query(Movimiento).order_by(Movimiento.fecha.desc()).all()

    # Consultar las ventas con detalles cargados
    ventas = session.query(Venta).options(joinedload(Venta.detalles)).all()

    # Consultar el producto más vendido
    producto_mas_vendido = session.query(
        DetalleVenta.id_producto,
        func.sum(DetalleVenta.cantidad).label('cantidad_vendida')
    ).group_by(DetalleVenta.id_producto).order_by(func.sum(DetalleVenta.cantidad).desc()).first()

    # Consultar ventas diarias, semanales y mensuales
    hoy = datetime.datetime.now()
    inicio_semana = hoy - datetime.timedelta(days=hoy.weekday())
    inicio_mes = hoy.replace(day=1)

    ventas_diarias = session.query(Venta).filter(Venta.fecha_registro >= hoy.date()).count()
    ventas_semanales = session.query(Venta).filter(Venta.fecha_registro >= inicio_semana.date()).count()
    ventas_mensuales = session.query(Venta).filter(Venta.fecha_registro >= inicio_mes.date()).count()

    # Usar la función ruta_absoluta para obtener la ruta a la carpeta 'historial'
    historial_folder = ruta_absoluta('historial')

    # Crear la carpeta si no existe
    if not os.path.exists(historial_folder):
        try:
            os.makedirs(historial_folder)
        except Exception as e:
            print(f"No se pudo crear la carpeta historial: {e}")
            return

    # Obtener ID de reporte
    nuevo_id = obtener_nuevo_id_reporte()

    # Nombre del archivo con ID + fecha y hora
    filename = f'reporte_movimientos_{nuevo_id}_{hoy.strftime("%Y%m%d_%H%M%S")}.pdf'
    pdf_filename = os.path.join(historial_folder, filename)

    # Crear el PDF
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    style = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Reporte de Movimientos y Ventas", style['Title']))
    content.append(Paragraph(f"ID de Reporte: #{nuevo_id}", style['Normal']))
    content.append(Paragraph(f"Fecha de Generación: {hoy.strftime('%Y-%m-%d %H:%M')}", style['Normal']))
    content.append(Spacer(1, 12))

    # Tabla de Movimientos
    movimientos_data = [["Producto", "Motivo", "Cantidad", "Fecha"]]
    for m in movimientos:
        producto_nombre = m.producto.nombre if m.producto else "Producto no encontrado"
        movimientos_data.append([producto_nombre, m.motivo, m.cantidad, m.fecha.strftime('%Y-%m-%d %H:%M')])

    movimientos_table = Table(movimientos_data)
    movimientos_table.setStyle(TableStyle([ 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ]))
    content.append(movimientos_table)
    content.append(Spacer(1, 12))

    # Tabla de Ventas
    ventas_data = [["Venta ID", "Cliente", "Precio Unitario", "Cantidad", "Total", "Fecha"]]
    for v in ventas:
        cliente_nombre = v.cliente.nombre if v.cliente else "Sin cliente asignado"
        for detalle in v.detalles:
            producto = session.query(Producto).filter(Producto.id == detalle.id_producto).first()
            precio_unitario = producto.precio if producto else "No disponible"
            ventas_data.append([v.id_venta, cliente_nombre, precio_unitario, detalle.cantidad, v.total, v.fecha_registro])

    ventas_table = Table(ventas_data)
    ventas_table.setStyle(TableStyle([ 
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ]))
    content.append(ventas_table)
    content.append(Spacer(1, 12))

    # Producto más vendido
    if producto_mas_vendido:
        producto = session.query(Producto).filter(Producto.id == producto_mas_vendido.id_producto).first()
        producto_mas_vendido_info = f"{producto.nombre} | Cantidad Vendida: {producto_mas_vendido.cantidad_vendida}" if producto else "Producto no disponible"
    else:
        producto_mas_vendido_info = "No disponible"

    content.append(Paragraph(f"<b>Producto más vendido:</b> {producto_mas_vendido_info}", style['Normal']))
    content.append(Spacer(1, 12))

    # Estadísticas de Ventas
    estadisticas_paragraph = Paragraph(
        f"<b>Ventas Diarias:</b> {ventas_diarias}<br/><b>Ventas Semanales:</b> {ventas_semanales}<br/><b>Ventas Mensuales:</b> {ventas_mensuales}",
        style['Normal']
    )
    content.append(estadisticas_paragraph)
    content.append(Spacer(1, 12))

    # Pie de página
    content.append(Paragraph("Generado por Sistema de Inventario | © 2025", style['Normal']))

    # Crear el PDF con manejo de errores
    try:
        doc.build(content)
        print(f"Reporte generado con éxito en: {pdf_filename}")
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
    finally:
        session.close()
