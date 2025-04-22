import tkinter as tk
from tkinter import PhotoImage, Scrollbar, ttk, messagebox
from datetime import datetime
from producto_backend import filtrar_productos,obtener_opciones_existentes, obtener_productos, agregar_producto_backend, eliminar_producto_backend, actualizar_producto_backend, obtener_producto_por_id
from PIL import ImageTk, Image
from RUTAS import ruta_absoluta

# === COLORES Y FUENTES ===
COLOR_FONDO = "#f4f6f8"
COLOR_BOTON = "#007acc"
COLOR_HEADER = "#1f3a5f"
COLOR_ALERTA = "salmon"
FUENTE_GENERAL = ("Segoe UI", 10)
FUENTE_TITULO = ("Segoe UI", 16, "bold")

def productos():
    def cargar_productos():
        for row in tree.get_children():
            tree.delete(row)
        productos = obtener_productos()
        for index,producto in enumerate(productos):
            color_alert= producto.cantidad_stock < producto.stock_minimo
            tag = "stock_bajo" if color_alert else ("par" if index % 2 == 0 else "impar")
            tree.tag_configure("par", background="white")
            tree.tag_configure("impar", background="#e6f2ff")  # Azul claro
            tree.tag_configure("stock_bajo", background=COLOR_ALERTA)
            tree.insert("", tk.END, tags=(tag,), values=(
                producto.id, producto.nombre, producto.precio, producto.categoria,
                producto.cantidad_stock, producto.stock_minimo, producto.id_proveedor,
                producto.estado, producto.fecha_registro.strftime("%Y-%m-%d")
            ))


    def agregar_producto():
        def guardar():
            try:
                datos = {
                    "nombre": nombre_var.get(),
                    "precio": float(precio_var.get()),
                    "categoria": int(categoria_cb.get()),
                    "cantidad_stock": int(stock_var.get()),
                    "stock_minimo": stock_minimo_var.get(),
                    "id_proveedor": int(proveedor_cb.get()),
                    "estado": estado_var.get(),
                    "fecha_registro": datetime.now()
                }
                agregar_producto_backend(datos)
                top.destroy()
                cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar: {e}")

        categorias, proveedores = obtener_opciones_existentes()
        top = tk.Toplevel(root)
        top.title("Agregar Producto")
        top.geometry("400x400")  # Ajustar tamaño para comodidad
        top.configure(bg=COLOR_FONDO)
        top.iconphoto(False, PhotoImage(file="logo_proyec.png"))
        top.resizable(False, False)

        nombre_var = tk.StringVar()
        precio_var = tk.StringVar()
        stock_var = tk.StringVar()
        stock_minimo_var = tk.StringVar()
        estado_var = tk.StringVar(value="activo")

        campos = [
            ("Nombre", nombre_var), ("Precio", precio_var), ("Categoría", None),
            ("Stock", stock_var), ("Stock Mínimo", stock_minimo_var),
            ("ID Proveedor", None), ("Estado", estado_var)
        ]

        # Crear un marco para centralizar los widgets
        frame = tk.Frame(top, bg=COLOR_FONDO)
        frame.pack(padx=20, pady=20)

        for i, (label, var) in enumerate(campos):
            tk.Label(frame, text=label, bg=COLOR_FONDO, font=FUENTE_GENERAL).grid(row=i, column=0, pady=10, sticky="w")
            if label == "Categoría":
                categoria_cb = ttk.Combobox(frame, values=categorias, state="readonly")
                categoria_cb.grid(row=i, column=1, padx=10, pady=5)
            elif label == "ID Proveedor":
                proveedor_cb = ttk.Combobox(frame, values=proveedores, state="readonly")
                proveedor_cb.grid(row=i, column=1, padx=10, pady=5)
            else:
                entry = tk.Entry(frame, textvariable=var, font=FUENTE_GENERAL, bd=2, relief="solid", width=25)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.config(justify="center")  # Centrar el texto en la entrada

        # Botón de guardar con un diseño más suave
        tk.Button(frame, text="Guardar", command=guardar, font=FUENTE_GENERAL, bg=COLOR_BOTON, fg="white", relief="flat", width=20).grid(row=7, column=0, columnspan=2, pady=20)
    
    def actualizar_producto():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un producto para actualizar")
            return
        prod_id = tree.item(selected)['values'][0]
        producto = obtener_producto_por_id(prod_id)
        categorias, proveedores = obtener_opciones_existentes()

        top = tk.Toplevel(root)
        top.title("Actualizar Producto")
        top.geometry("400x400")  # Ajustar tamaño para comodidad
        top.configure(bg=COLOR_FONDO)
        top.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))
        top.resizable(False, False)

        nombre_var = tk.StringVar(value=producto.nombre)
        precio_var = tk.StringVar(value=str(producto.precio))
        stock_var = tk.StringVar(value=str(producto.cantidad_stock))
        stock_minimo_var = tk.StringVar(value=producto.stock_minimo)
        estado_var = tk.StringVar(value=producto.estado)

        campos = [
            ("Nombre", nombre_var), ("Precio", precio_var), ("Categoría", None),
            ("Stock", stock_var), ("Stock Mínimo", stock_minimo_var),
            ("ID Proveedor", None), ("Estado", estado_var)
        ]

        # Crear un marco para centralizar los widgets
        frame = tk.Frame(top, bg=COLOR_FONDO)
        frame.pack(padx=20, pady=20)

        for i, (label, var) in enumerate(campos):
            tk.Label(frame, text=label, bg=COLOR_FONDO, font=FUENTE_GENERAL).grid(row=i, column=0, pady=10, sticky="w")
            if label == "Categoría":
                categoria_cb = ttk.Combobox(frame, values=categorias, state="readonly")
                categoria_cb.set(str(producto.categoria))
                categoria_cb.grid(row=i, column=1, padx=10, pady=5)
            elif label == "ID Proveedor":
                proveedor_cb = ttk.Combobox(frame, values=proveedores, state="readonly")
                proveedor_cb.set(str(producto.id_proveedor))
                proveedor_cb.grid(row=i, column=1, padx=10, pady=5)
            else:
                entry = tk.Entry(frame, textvariable=var, font=FUENTE_GENERAL, bd=2, relief="solid", width=25)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entry.config(justify="center")  # Centrar el texto en la entrada

        def guardar_actualizacion():
            nuevos_datos = {
                "nombre": nombre_var.get(),
                "precio": float(precio_var.get()),
                "categoria": int(categoria_cb.get()),
                "cantidad_stock": int(stock_var.get()),
                "stock_minimo": stock_minimo_var.get(),
                "id_proveedor": int(proveedor_cb.get()),
                "estado": estado_var.get()
            }
            actualizar_producto_backend(prod_id, nuevos_datos)
            top.destroy()
            cargar_productos()

    # Botón de guardar cambios
        tk.Button(frame, text="Guardar Cambios", command=guardar_actualizacion, font=FUENTE_GENERAL, bg=COLOR_BOTON, fg="white", relief="flat", width=20).grid(row=7, column=0, columnspan=2, pady=20)

    def eliminar_producto():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Selecciona un producto para eliminar")
            return
        prod_id = tree.item(selected)['values'][0]
        eliminar_producto_backend(prod_id)
        cargar_productos()
        
    # Interfaz principal
    root = tk.Toplevel()
    root.title("Gestión de Productos")
    root.geometry("950x500")
    root.configure(bg=COLOR_FONDO)
    root.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))
    root.resizable(False, False)
           
    # --- CABECERA ---
    header = tk.Frame(root, bg=COLOR_HEADER, height=60)
    header.pack(side="top", fill="x")

    try:
        logo = Image.open(ruta_absoluta("logo_proyec.png"))
        logo = logo.resize((40, 40))
        logo_img = ImageTk.PhotoImage(logo)
        tk.Label(header, image=logo_img, bg=COLOR_HEADER).pack(side="left", padx=20)
    except:
        pass  # Si no hay logo, lo ignora

    tk.Label(header, text="Gestión de Productos", font=FUENTE_TITULO, fg="white", bg=COLOR_HEADER).pack(side="left")

    # --- TREEVIEW ---
    columns = ("id", "nombre", "precio", "categoria", "cantidad_stock", "stock_minimo", "id_proveedor", "estado", "fecha_registro")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col,anchor="center", width=100)
    tree.pack(fill="both", expand=True)
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="white", relief="flat")

    scroll_y = Scrollbar(tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # --- BOTONES ---
    frame_botones = tk.Frame(root, bg=COLOR_FONDO)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Agregar Producto", command=agregar_producto, font=FUENTE_GENERAL, bg=COLOR_BOTON, fg="white", relief="flat").grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Actualizar Producto", command=actualizar_producto, font=FUENTE_GENERAL, bg=COLOR_BOTON, fg="white", relief="flat").grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Eliminar Producto", command=eliminar_producto, font=FUENTE_GENERAL, bg=COLOR_BOTON, fg="white", relief="flat").grid(row=0, column=2, padx=5)
    
        # --- FILTRO DE BÚSQUEDA ---
    frame_filtros = tk.Frame(root, bg=COLOR_FONDO)
    frame_filtros.pack(pady=10)

    tk.Label(frame_filtros, text="ID:", bg=COLOR_FONDO, font=FUENTE_GENERAL).grid(row=0, column=0, padx=5)
    filtro_id = tk.Entry(frame_filtros, width=10)
    filtro_id.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtros, text="Nombre:", bg=COLOR_FONDO, font=FUENTE_GENERAL).grid(row=0, column=2, padx=5)
    filtro_nombre = tk.Entry(frame_filtros, width=15)
    filtro_nombre.grid(row=0, column=3, padx=5)

    tk.Label(frame_filtros, text="Categoría:", bg=COLOR_FONDO, font=FUENTE_GENERAL).grid(row=0, column=4, padx=5)
    filtro_categoria = tk.Entry(frame_filtros, width=10)
    filtro_categoria.grid(row=0, column=5, padx=5)

    tk.Label(frame_filtros, text="Proveedor:", bg=COLOR_FONDO, font=FUENTE_GENERAL).grid(row=0, column=6, padx=5)
    filtro_proveedor = tk.Entry(frame_filtros, width=10)
    filtro_proveedor.grid(row=0, column=7, padx=5)

    def aplicar_filtro():
        try:
            id_val = int(filtro_id.get()) if filtro_id.get().isdigit() else None
            nombre_val = filtro_nombre.get().strip() or None
            categoria_val = int(filtro_categoria.get()) if filtro_categoria.get().isdigit() else None
            proveedor_val = int(filtro_proveedor.get()) if filtro_proveedor.get().isdigit() else None

            productos_filtrados = filtrar_productos(id=id_val, nombre=nombre_val, categoria=categoria_val, id_proveedor=proveedor_val)

            for row in tree.get_children():
                tree.delete(row)
            for index, producto in enumerate(productos_filtrados):
                color_alert = producto.cantidad_stock < producto.stock_minimo
                tag = "stock_bajo" if color_alert else ("par" if index % 2 == 0 else "impar")
                tree.insert("", tk.END, tags=(tag,), values=(
                    producto.id, producto.nombre, producto.precio, producto.categoria,
                    producto.cantidad_stock, producto.stock_minimo, producto.id_proveedor,
                    producto.estado, producto.fecha_registro.strftime("%Y-%m-%d")
                ))
        except Exception as e:
            messagebox.showerror("Error de Filtro", f"No se pudo aplicar el filtro: {e}")

    tk.Button(frame_filtros, text="🔍\nBuscar", command=aplicar_filtro, font=FUENTE_GENERAL, bg=COLOR_BOTON, fg="white", relief="flat").grid(row=0, column=8, padx=10)

    cargar_productos()
    root.mainloop()
