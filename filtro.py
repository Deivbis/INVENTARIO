# producto_frontend.py
import tkinter as tk
from tkinter import Scrollbar, ttk, messagebox
from filtro_backend import buscar_productos, obtener_categorias
from PIL import ImageTk, Image
from RUTAS import ruta_absoluta

def filtro_busqueda():
    def actualizar_treeview(productos):
        for row in tree.get_children():
            tree.delete(row)
        for index,producto in enumerate(productos):
            color = "par" if index % 2 == 0 else "impar"
            if producto.cantidad_stock < producto.stock_minimo:
                color = "salmon"
            tree.insert("", "end", values=(
                producto.id, producto.nombre, producto.precio, producto.categoria,
                producto.cantidad_stock, producto.stock_minimo, producto.id_proveedor,
                producto.estado, producto.fecha_registro.strftime("%Y-%m-%d")
            ),tag=(color,))
        tree.tag_configure("par", background="#f4f6f8")
        tree.tag_configure("impar", background="white")
        tree.tag_configure("salmon", background="salmon")
        
    def buscar():
        try:
            productos = buscar_productos(
                id_busqueda=id_var.get(),
                nombre_busqueda=nombre_var.get(),
                categoria_filtro=categoria_cb.get()
            )
            actualizar_treeview(productos)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    # ---- Ventana principal ----
    root = tk.Toplevel()
    root.title("Buscar Productos - Inventary")
    root.geometry("1000x650")
    root.configure(bg="#ffffff")
    root.iconphoto(False, ImageTk.PhotoImage(file=ruta_absoluta("logo_proyec.png")))
    root.resizable(False, False)

    # ---- Cabecera ----
    header = tk.Frame(root, bg="#1f3a5f", height=70)
    header.pack(side="top", fill="x")

    logo_img = Image.open(ruta_absoluta("logo_proyec.png"))
    logo_img = logo_img.resize((50, 50))
    logo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(header, image=logo, bg="#1f3a5f")
    logo_label.image = logo
    logo_label.pack(side="left", padx=20)

    title = tk.Label(header, text="Buscar Productos", bg="#1f3a5f", fg="white", font=("Segoe UI", 18, "bold"))
    title.pack(side="left", padx=10)

    # ---- Panel de búsqueda ----
    filtro_frame = tk.Frame(root, bg="white")
    filtro_frame.pack(pady=30)

    id_var = tk.StringVar()
    nombre_var = tk.StringVar()

    tk.Label(filtro_frame, text="ID:", font=("Segoe UI", 11), bg="white").grid(row=0, column=0, padx=10, pady=10)
    ttk.Entry(filtro_frame, textvariable=id_var, width=20).grid(row=0, column=1, padx=10)

    tk.Label(filtro_frame, text="Nombre:", font=("Segoe UI", 11), bg="white").grid(row=0, column=2, padx=10)
    ttk.Entry(filtro_frame, textvariable=nombre_var, width=20).grid(row=0, column=3, padx=10)

    tk.Label(filtro_frame, text="Categoría:", font=("Segoe UI", 11), bg="white").grid(row=0, column=4, padx=10)
    categoria_cb = ttk.Combobox(filtro_frame, values=obtener_categorias(), state="readonly", width=20)
    categoria_cb.grid(row=0, column=5, padx=10)

    buscar_btn = tk.Button(filtro_frame, text="🔍 Buscar", bg="#007acc", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5, command=buscar)
    buscar_btn.grid(row=0, column=6, padx=15)

    # ---- Tabla de resultados ----
    tree_frame = tk.Frame(root, bg="white")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

    columns = (
        "id", "nombre", "precio", "categoria", "cantidad_stock",
        "stock_minimo", "id_proveedor", "estado", "fecha_registro"
    )
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)
    tree.pack(fill="both", expand=True)
    
    scroll_y = Scrollbar(tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    root.mainloop()
