import tkinter as tk
from tkinter import ttk, messagebox
from conexion_bd import crear_sesion
from venta_backend import Cliente, Venta, Producto, DetalleVenta, Movimiento
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
from tkinter import ttk, Scrollbar
from RUTAS import ruta_absoluta


def ventas():
    SessionLocal = crear_sesion

    # ================= FUNCIONES ================= #

    def create_cliente():
        nombre = entry_cliente_nombre.get()
        telefono = entry_cliente_telefono.get()
        correo = entry_cliente_correo.get()

        if not nombre:
            messagebox.showwarning("Error", "El nombre es obligatorio.")
            return

        if telefono and not telefono.isdigit():
            messagebox.showwarning("Error", "El teléfono debe ser un número.")
            return

        db_session = SessionLocal()
        try:
            cliente = Cliente(nombre=nombre, telefono=telefono, correo=correo)
            db_session.add(cliente)
            db_session.commit()
            db_session.refresh(cliente)
            messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente.")
            cargar_clientes()
        except Exception as e:
            db_session.rollback()
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")
        finally:
            db_session.close()
            entry_cliente_nombre.delete(0, tk.END)
            entry_cliente_telefono.delete(0, tk.END)
            entry_cliente_correo.delete(0, tk.END)

    def seleccionar_cliente():
        selected = tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un cliente.")
            return
        cliente_id = tree_clientes.item(selected)["values"][0]
        entry_cliente_id.delete(0, tk.END)
        entry_cliente_id.insert(0, cliente_id)

    def registrar_venta():
        cliente_id = entry_cliente_id.get()
        if not cliente_id:
            messagebox.showwarning("Error", "Seleccione un cliente.")
            return
        try:
            cliente_id = int(cliente_id)
        except ValueError:
            messagebox.showwarning("Error", "ID de cliente inválido.")
            return

        total = 0
        detalles = []

        for child in tree_productos.get_children():
            values = tree_productos.item(child)['values']
            try:
                producto_id = int(values[0])
                precio = float(values[1])
                stock = int(values[2])
                nombre = values[3]
                cantidad = int(values[4])
            except (ValueError, IndexError):
                messagebox.showwarning("Error", "Error al procesar los datos del producto.")
                return

            if cantidad > 0:
                if cantidad > stock:
                    messagebox.showwarning("Error", f"Stock insuficiente para {nombre}.")
                    return
                total += cantidad * precio
                detalles.append((producto_id, cantidad, precio))

        if not detalles:
            messagebox.showwarning("Error", "Seleccione al menos un producto con cantidad.")
            return

        db_session = SessionLocal()
        try:
            # Registrar la venta con el cliente y el total
            venta = Venta(
                id_cliente=cliente_id,
                cantidad_inicial=sum(d[1] for d in detalles),  # Sumar las cantidades
                cantidad_actual=sum(d[1] for d in detalles),  # Se asume que la cantidad actual es la misma en la venta
                precio_unitario=detalles[0][2],  # Precio unitario de un producto (en caso de ser el mismo para todos)
                estado="activo",
                fecha_registro=datetime.now(),
                total=total
            )
            db_session.add(venta)
            db_session.commit()
            db_session.refresh(venta)

            # Registrar los detalles de la venta
            for producto_id, cantidad, precio_unitario in detalles:
                detalle = DetalleVenta(
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    total=cantidad * precio_unitario,  # Total del detalle de la venta
                    id_producto=producto_id,
                    id_venta=venta.id_venta,
                    estado="activo",
                    fecha_registro=datetime.now()
                )
                db_session.add(detalle)

                # Actualizar el stock de los productos
                producto = db_session.query(Producto).filter(Producto.id == producto_id).first()
                if producto:
                    producto.cantidad_stock -= cantidad
                    
                    movimiento = Movimiento(
                    producto_id=producto_id,
                    cantidad=cantidad,
                    motivo="Venta",
                    fecha=datetime.now()
                )
                db_session.add(movimiento)

            # Confirmar los cambios en la base de datos
            db_session.commit()
            messagebox.showinfo("Éxito", f"Venta registrada correctamente. Total: ${total:.2f}")
            cargar_productos()
            # Obtener cliente desde DB
            cliente = db_session.query(Cliente).filter(Cliente.id_cliente == cliente_id).first()

            # Obtener detalles de esta venta
            detalles_venta = db_session.query(DetalleVenta).filter(DetalleVenta.id_venta == venta.id_venta).all()

            # Generar factura PDF
            generar_factura_pdf(venta, detalles_venta, cliente)

        except Exception as e:
            db_session.rollback()
            messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")
        finally:
            db_session.close()



    def cargar_clientes():
        for i in tree_clientes.get_children():
            tree_clientes.delete(i)
        db_session = SessionLocal()
        clientes = db_session.query(Cliente).all()
        for index,cliente in enumerate(clientes):
            tag = "par" if index % 2 == 0 else "impar"
            tree_clientes.insert("", tk.END, tags=(tag,), values=(cliente.id_cliente, cliente.nombre, cliente.telefono, cliente.correo))    
        db_session.close()

    def cargar_productos():
        for i in tree_productos.get_children():
            tree_productos.delete(i)
        db_session = SessionLocal()
        productos = db_session.query(Producto).filter(Producto.estado == "activo").all()
        for index,producto in enumerate(productos):
            alerta=producto.cantidad_stock < producto.stock_minimo
            tag = "stock_bajo" if alerta else ("par" if index % 2 == 0 else "impar")
            tree_productos.insert("", tk.END, tags=(tag,), values=(producto.id, producto.precio, producto.cantidad_stock, producto.nombre, 0))
        db_session.close()

    def editar_cantidad(event):
        selected = tree_productos.selection()
        if selected:
            item = selected[0]
            values = tree_productos.item(item)['values']

            def guardar_cantidad():
                try:
                    nueva_cantidad = int(entry_popup.get())
                    if nueva_cantidad < 0:
                        messagebox.showerror("Error", "La cantidad no puede ser negativa.")
                        return
                    if nueva_cantidad > int(values[2]):
                        messagebox.showerror("Error", "No hay suficiente stock.")
                        return
                    values[4] = nueva_cantidad
                    tree_productos.item(item, values=values)
                    popup.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Cantidad inválida.")

            popup = tk.Toplevel(root)
            popup.title("Editar Cantidad")
            popup.geometry("200x100")
            popup.resizable(False, False)
            popup.iconphoto(False, tk.PhotoImage(file=ruta_absoluta("logo_proyec.png")))
            popup.config(bg="white")
            tk.Label(popup, text="Cantidad:").pack(pady=5)
            entry_popup = tk.Entry(popup)
            entry_popup.insert(0, str(values[4]))
            entry_popup.pack()
            tk.Button(popup, text="Guardar", command=guardar_cantidad).pack(pady=5)

    # ================= INTERFAZ ================= #



    def generar_factura_pdf(venta, detalles, cliente):
        # Obtener la ruta absoluta de la carpeta 'reporte'
        folder = ruta_absoluta('reporte')
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Ruta del archivo PDF dentro de la carpeta 'reporte'
        filename = f"Factura_Venta_{venta.id_venta}.pdf"
        filepath = os.path.join(folder, filename)

        # Crear el documento PDF
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Factura de Venta")

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"ID Venta: {venta.id_venta}")
        c.drawString(50, height - 100, f"Fecha: {venta.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, height - 120, f"Cliente: {cliente.nombre}")
        c.drawString(50, height - 140, f"Teléfono: {cliente.telefono}")
        c.drawString(50, height - 160, f"Correo: {cliente.correo}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 200, "Producto")
        c.drawString(250, height - 200, "Cantidad")
        c.drawString(350, height - 200, "Precio Unitario")
        c.drawString(480, height - 200, "Total")

        y = height - 220
        c.setFont("Helvetica", 11)

        for detalle in detalles:
            c.drawString(50, y, detalle.producto.nombre)
            c.drawString(250, y, str(detalle.cantidad))
            c.drawString(350, y, f"${detalle.precio_unitario:.2f}")
            c.drawString(480, y, f"${detalle.total:.2f}")
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50

        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y - 20, f"TOTAL: ${venta.total:.2f}")
        c.save()

        # Mensaje de confirmación
        messagebox.showinfo("Factura Generada", f"Factura guardada como: {filepath}")



    # Función para centrar la ventana
    def centrar_ventana(ventana, ancho, alto):
        ventana.update_idletasks()
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        x = int((screen_width / 2) - (ancho / 2))
        y = int((screen_height / 2) - (alto / 2))
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    root = tk.Toplevel()
    root.title("Venta de Productos")
    root.config(bg="#f9f9f9")
    centrar_ventana(root, 1000, 720)
    root.iconphoto(False, tk.PhotoImage(file=ruta_absoluta("logo_proyec.png")))
    root.resizable(False, False)
    
    style = ttk.Style()
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

    # ==== Frame Cliente ==== #
    frame_cliente = tk.LabelFrame(root, text="Cliente", bg="#ffffff", font=("Segoe UI", 11, "bold"), padx=10, pady=10)
    frame_cliente.pack(padx=10, pady=10, fill="x")

    for i, text in enumerate(["Nombre:", "Teléfono:", "Correo:"]):
        tk.Label(frame_cliente, text=text, bg="white", font=("Segoe UI", 10)).grid(row=0, column=i*2, padx=5, pady=5)
    
    entry_cliente_nombre = tk.Entry(frame_cliente, font=("Segoe UI", 10))
    entry_cliente_nombre.grid(row=0, column=1, padx=5)
    entry_cliente_telefono = tk.Entry(frame_cliente, font=("Segoe UI", 10))
    entry_cliente_telefono.grid(row=0, column=3, padx=5)
    entry_cliente_correo = tk.Entry(frame_cliente, font=("Segoe UI", 10))
    entry_cliente_correo.grid(row=0, column=5, padx=5)

    tk.Button(frame_cliente, text="Registrar Cliente", command=create_cliente,
              bg="#2e86de", fg="white", font=("Segoe UI", 10, "bold"), height=1).grid(row=0, column=6, padx=10)

    # ==== Treeview Clientes ==== #
    frame_clientes=tk.LabelFrame(root, text="Clientes Registrados", bg="#ffffff", font=("Segoe UI", 11, "bold"), padx=10, pady=10)
    frame_clientes.pack(padx=10, pady=10, fill="both", expand=True)
    
    tree_clientes = ttk.Treeview(frame_clientes, columns=("ID", "Nombre", "Teléfono", "Correo"), show="headings", height=5)
    for col in ("ID", "Nombre", "Teléfono", "Correo"):
        tree_clientes.heading(col, text=col)
        tree_clientes.column(col, anchor="center")
    tree_clientes.pack(fill="both", expand=True)
    
    style = ttk.Style()
    style.configure("Tree_clientes.Heading", font=("Segoe UI", 10, "bold"), background="white", fg="black")
    tree_clientes.tag_configure("par", background="white")
    tree_clientes.tag_configure("impar", background="#e6f2ff")
    
    scroll_y = Scrollbar(tree_clientes, orient="vertical", command=tree_clientes.yview)
    tree_clientes.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    

    frame_select = tk.Frame(root, bg="#f9f9f9")
    frame_select.pack(pady=5)
    
    tk.Label(frame_select, text="ID Cliente Seleccionado:", font=("Segoe UI", 10), bg="#f9f9f9").pack(side="left", padx=5)
    entry_cliente_id = tk.Entry(frame_select, width=10, font=("Segoe UI", 10))
    entry_cliente_id.pack(side="left")
    tk.Button(frame_select, text="Seleccionar Cliente", command=seleccionar_cliente,
              bg="#2e86de", fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)

    # ==== Productos ==== #
    frame_productos = tk.LabelFrame(root, text="Productos Disponibles", bg="#ffffff", font=("Segoe UI", 11, "bold"), padx=10, pady=10)
    frame_productos.pack(padx=10, pady=10, fill="both", expand=True)

    tree_productos = ttk.Treeview(frame_productos,
                                  columns=("ID","Precio", "Stock", "Nombre", "Cantidad"),
                                  show="headings", height=10, selectmode="browse")
    for col in ("ID","Precio", "Stock", "Nombre", "Cantidad"):
        tree_productos.heading(col, text=col)
        tree_productos.column(col, anchor="center")
    tree_productos.pack(fill="both", expand=True)
    
    style = ttk.Style()
    style.configure("Tree_productos.Heading", font=("Segoe UI", 10, "bold"), background="white", fg="black")
    tree_productos.tag_configure("par", background="white")
    tree_productos.tag_configure("impar", background="#e6f2ff")
    tree_productos.tag_configure("stock_bajo", background="salmon")
    
    scroll_y = Scrollbar(tree_productos, orient="vertical", command=tree_productos.yview)
    tree_productos.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    tree_productos.bind("<Double-1>", editar_cantidad)

    # ==== Botón Venta ==== #
    tk.Button(root, text="Registrar Venta", command=registrar_venta,
              height=2, bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold")).pack(pady=15)

    # Cargar datos iniciales
    cargar_clientes()
    cargar_productos()

    root.mainloop()
