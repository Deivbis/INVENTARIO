import tkinter as tk
from tkinter import Scrollbar, ttk, messagebox
from categoria_backend import obtener_categorias, agregar_categoria, actualizar_categoria, eliminar_categoria
from tkinter import PhotoImage
from PIL import Image, ImageTk
from RUTAS import ruta_absoluta

# === COLORES Y FUENTES ===
COLOR_FONDO = "#f4f6f8"
COLOR_BOTON = "#007acc"
COLOR_HEADER = "#1f3a5f"
FUENTE_GENERAL = ("Segoe UI", 10)
FUENTE_TITULO = ("Segoe UI", 16, "bold")

def categorias():
    def centrar_ventana(ventana, ancho, alto):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def cargar_datos():
        treeview.delete(*treeview.get_children())
        categorias = obtener_categorias()
        for index, c in enumerate(categorias):
            tag = "par" if index % 2 == 0 else "impar"
            treeview.insert("", "end", tags=(tag,), values=(
                c.id_categoria, c.nombre, c.descripcion, c.estado, c.fecha_registro))

    def agregar_categoria_ui():
        ventana_agregar = tk.Toplevel(ventana)
        ventana_agregar.title("Agregar Categoría")
        centrar_ventana(ventana_agregar, 400, 300)
        ventana_agregar.resizable(False, False)
        ventana_agregar.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))
        ventana_agregar.configure(bg=COLOR_FONDO)

        tk.Label(ventana_agregar, text="Nombre:", bg=COLOR_FONDO, font=FUENTE_GENERAL).pack(pady=5)
        entry_nombre = tk.Entry(ventana_agregar, font=FUENTE_GENERAL)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_agregar, text="Descripción:", bg=COLOR_FONDO, font=FUENTE_GENERAL).pack(pady=5)
        entry_descripcion = tk.Entry(ventana_agregar, font=FUENTE_GENERAL)
        entry_descripcion.pack(pady=5)

        tk.Label(ventana_agregar, text="Estado:", bg=COLOR_FONDO, font=FUENTE_GENERAL).pack(pady=5)
        combo_estado = ttk.Combobox(ventana_agregar, values=["activo", "inactivo"], state="readonly", font=FUENTE_GENERAL)
        combo_estado.set("activo")
        combo_estado.pack(pady=5)

        def guardar():
            nombre = entry_nombre.get()
            descripcion = entry_descripcion.get()
            estado = combo_estado.get()

            if descripcion == "":
                messagebox.showerror("Error", "Debe ingresar una descripción")
                return

            agregar_categoria(nombre, descripcion, estado)
            messagebox.showinfo("Éxito", "Categoría agregada")
            cargar_datos()
            ventana_agregar.destroy()

        tk.Button(ventana_agregar, text="Guardar", command=guardar, font=FUENTE_GENERAL,
                  bg=COLOR_BOTON, fg="white", relief="flat").pack(pady=10)

    def actualizar_categoria_ui():
        seleccionado = treeview.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una categoría")
            return

        datos = treeview.item(seleccionado[0])["values"]
        categoria_id, nombre_actual, descripcion_actual, estado_actual = datos[0], datos[1], datos[2], datos[3]

        ventana_actualizar = tk.Toplevel(ventana)
        ventana_actualizar.title("Actualizar Categoría")
        centrar_ventana(ventana_actualizar, 400, 300)
        ventana_actualizar.configure(bg=COLOR_FONDO)
        ventana_actualizar.resizable(False, False)
        ventana_actualizar.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))

        tk.Label(ventana_actualizar, text="Nombre:", bg=COLOR_FONDO, font=FUENTE_GENERAL).pack(pady=5)
        entry_nombre = tk.Entry(ventana_actualizar, font=FUENTE_GENERAL)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_actualizar, text="Descripción:", bg=COLOR_FONDO, font=FUENTE_GENERAL).pack(pady=5)
        entry_descripcion = tk.Entry(ventana_actualizar, font=FUENTE_GENERAL)
        entry_descripcion.insert(0, descripcion_actual)
        entry_descripcion.pack(pady=5)

        tk.Label(ventana_actualizar, text="Estado:", bg=COLOR_FONDO, font=FUENTE_GENERAL).pack(pady=5)
        combo_estado = ttk.Combobox(ventana_actualizar, values=["activo", "inactivo"], state="readonly", font=FUENTE_GENERAL)
        combo_estado.set(estado_actual)
        combo_estado.pack(pady=5)

        def guardar():
            nuevo_nombre = entry_nombre.get()
            nueva_desc = entry_descripcion.get()
            nuevo_estado = combo_estado.get()
            actualizar_categoria(categoria_id, nuevo_nombre, nueva_desc, nuevo_estado)
            messagebox.showinfo("Éxito", "Categoría actualizada")
            cargar_datos()
            ventana_actualizar.destroy()

        tk.Button(ventana_actualizar, text="Actualizar", command=guardar, font=FUENTE_GENERAL,
                  bg=COLOR_BOTON, fg="white", relief="flat").pack(pady=10)

    def eliminar_categoria_ui():
        seleccionado = treeview.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una categoría")
            return
        datos = treeview.item(seleccionado[0])["values"]
        eliminar_categoria(datos[0])
        messagebox.showinfo("Éxito", "Categoría eliminada")
        cargar_datos()

    # --- Ventana Principal ---
    ventana = tk.Toplevel()
    ventana.title("Gestión de Categorías")
    centrar_ventana(ventana, 750, 500)
    ventana.configure(bg=COLOR_FONDO)
    ventana.resizable(False, False)
    ventana.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))

    # --- Header ---
    header = tk.Frame(ventana, bg=COLOR_HEADER, height=60)
    header.pack(side="top", fill="x")

    try:
        logo = Image.open(ruta_absoluta("logo_proyec.png"))
        logo = logo.resize((40, 40))
        logo_img = ImageTk.PhotoImage(logo)
        tk.Label(header, image=logo_img, bg=COLOR_HEADER).pack(side="left", padx=20)
    except:
        pass

    tk.Label(header, text="Gestión de Categorías", font=FUENTE_TITULO, fg="white", bg=COLOR_HEADER).pack(side="left")

    # --- Treeview ---
    columnas = ("Id_Categoria", "Nombre", "Descripcion", "Estado", "Fecha_Registro")
    treeview = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center", width=130)
    treeview.pack(fill="both", expand=True, pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="white", foreground="black")
    treeview.tag_configure("par", background="white")
    treeview.tag_configure("impar", background="#e6f2ff")
    
    scroll_y = Scrollbar(treeview, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    treeview.pack(fill="both", expand=True)

    # --- Botones ---
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Agregar", command=agregar_categoria_ui, font=FUENTE_GENERAL,
              bg=COLOR_BOTON, fg="white", relief="flat", width=15).grid(row=0, column=0, padx=10)
    tk.Button(frame_botones, text="Actualizar", command=actualizar_categoria_ui, font=FUENTE_GENERAL,
              bg=COLOR_BOTON, fg="white", relief="flat", width=15).grid(row=0, column=1, padx=10)
    tk.Button(frame_botones, text="Eliminar", command=eliminar_categoria_ui, font=FUENTE_GENERAL,
              bg=COLOR_BOTON, fg="white", relief="flat", width=15).grid(row=0, column=2, padx=10)

    cargar_datos()
    ventana.mainloop()
