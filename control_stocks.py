import tkinter as tk
from tkinter import Scrollbar, messagebox, ttk, PhotoImage
from control_stock_backend import obtener_productos, actualizar_stock, registrar_movimiento
from RUTAS import ruta_absoluta

def cargar_productos(tree):
    for row in tree.get_children():
        tree.delete(row)
    productos = obtener_productos()
    for index, producto in enumerate(productos):
        
        color = "#E8F0FE" if index % 2 == 0 else "white"
        if producto.cantidad_stock <= producto.stock_minimo:
            color = "salmon"
        tree.insert("", "end", values=(
            producto.id,
            producto.precio,
            producto.cantidad_stock,
            producto.nombre,
            0
        ), tags=(color,))
    tree.tag_configure("white", background="white")
    tree.tag_configure("#E8F0FE", background="#E8F0FE")
    tree.tag_configure("salmon", background="salmon")

def modificar_stock(tree, aumentar=True):
    seleccionado = tree.focus()
    if not seleccionado:
        messagebox.showinfo("Selecciona un producto", "Por favor selecciona un producto.")
        return

    valores = tree.item(seleccionado, "values")
    producto_id = int(valores[0])
    nombre = valores[3]
    cantidad_actual = int(valores[2])
    accion = "Entrada" if aumentar else "Salida"

    ventana_popup = tk.Toplevel()
    ventana_popup.title(f"{accion} de Stock - {nombre}")
    ventana_popup.configure(bg="white")
    ventana_popup.resizable(False, False)

    ancho, alto = 350, 180
    x = (ventana_popup.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_popup.winfo_screenheight() // 2) - (alto // 2)
    ventana_popup.geometry(f"{ancho}x{alto}+{x}+{y}")

    tk.Label(
        ventana_popup,
        text=f"{accion} al stock actual ({cantidad_actual}):",
        bg="white",
        font=("Segoe UI", 11)
    ).pack(pady=(20, 5))

    entry = tk.Entry(ventana_popup, font=("Segoe UI", 11), justify="center", relief="solid", bd=1)
    entry.pack(pady=5)

    def aplicar_cambio():
        try:
            cantidad = int(entry.get())
            if cantidad < 0:
                raise ValueError("Cantidad negativa")
            nuevo_stock = cantidad_actual + cantidad if aumentar else cantidad_actual - cantidad
            if nuevo_stock < 0:
                messagebox.showerror("Error", "No puedes tener stock negativo.")
                return
            elif nuevo_stock > 0:
                messagebox.showinfo("Información", "El stock se ha actualizado correctamente.")
            actualizar_stock(producto_id, nuevo_stock)
            registrar_movimiento(producto_id, "entrada" if aumentar else "salida", cantidad,motivo=accion)
            cargar_productos(tree)
            ventana_popup.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa una cantidad válida.")

    tk.Button(
        ventana_popup,
        text="Aplicar",
        command=aplicar_cambio,
        font=("Segoe UI", 10, "bold"),
        bg="#0A74DA",
        fg="white",
        relief="flat",
        padx=10,
        pady=5
    ).pack(pady=15)

def control_stock():
    ventana = tk.Tk()
    ventana.title("Control de Stock - INVENTARY")
    ventana.configure(bg="white")
    ventana.geometry("950x600")
    ventana.resizable(False, False)

    w, h = 950, 600
    x = (ventana.winfo_screenwidth() // 2) - (w // 2)
    y = (ventana.winfo_screenheight() // 2) - (h // 2)
    ventana.geometry(f"{w}x{h}+{x}+{y}")

    # Encabezado
    header = tk.Frame(ventana, bg="#1C3557", height=70)
    header.pack(fill="x")

    try:
        logo_img = PhotoImage(file=ruta_absoluta("logo_proyec.png"))
        logo_img = logo_img.subsample(4, 4)
        logo_label = tk.Label(header, image=logo_img, bg="#1C3557")
        logo_label.image = logo_img
        logo_label.pack(side="left", padx=(20, 10), pady=5)
    except:
        tk.Label(header, text="📦", bg="#1C3557", fg="white", font=("Segoe UI", 25)).pack(side="left", padx=20)

    tk.Label(header, text="INVENTARY - Control de Stock", bg="#1C3557", fg="white",
             font=("Segoe UI", 18, "bold")).pack(side="left", pady=10)

    # Tabla
    frame_tabla = tk.LabelFrame(ventana, text="Productos", bg="white", font=("Segoe UI", 12, "bold"), bd=0)
    frame_tabla.pack(pady=(10, 0), padx=20, fill="both", expand=True)

    columnas = ("ID", "Precio", "Stock", "Nombre", "Cantidad")
    tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=20)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    font=("Segoe UI", 10),
                    rowheight=25,
                    background="white",
                    fieldbackground="white",
                    bordercolor="lightgray",
                    relief="flat")
    style.configure("Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    background="#F0F0F0",
                    borderwidth=1)
    style.map("Treeview", background=[("selected", "#D0E4FF")])

    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=160)

    # Scrollbar vertical
    scroll_y = Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    tree.pack(pady=(15, 10), padx=20, fill="both", expand=True)
    cargar_productos(tree)

    # Botones
    frame_botones = tk.Frame(ventana, bg="white")
    frame_botones.pack(pady=10)

    tk.Button(
        frame_botones, text="Entrada de Stock",
        command=lambda: modificar_stock(tree, True),
        bg="#2196F3", fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat", padx=15, pady=6
    ).pack(side="left", padx=15)

    tk.Button(
        frame_botones, text="Salida de Stock",
        command=lambda: modificar_stock(tree, False),
        bg="#1976D2", fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat", padx=15, pady=6
    ).pack(side="left", padx=15)

    ventana.mainloop()
