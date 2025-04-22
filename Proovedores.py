import tkinter as tk
from tkinter import Scrollbar, ttk, messagebox
from proovedores_backend import obtener_proveedores_activos, agregar_proveedor, obtener_proveedor_por_id, actualizar_proveedor, eliminar_proveedor
from tkinter import PhotoImage
from PIL import ImageTk, Image
from RUTAS import ruta_absoluta

# === COLORES Y FUENTES ===
COLOR_FONDO = "#f4f6f8"
COLOR_BOTON = "#007acc"
COLOR_HEADER = "#1f3a5f"
FUENTE_GENERAL = ("Segoe UI", 10)
FUENTE_TITULO = ("Segoe UI", 16, "bold")

def proveedores():
    def centrar_ventana(ventana, ancho, alto):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho - ancho) // 2
        y = (pantalla_alto - alto) // 2
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def cargar_datos():
        treeview.delete(*treeview.get_children())
        proveedores = obtener_proveedores_activos()
        for index, p in enumerate(proveedores):
            tag = "par" if index % 2 == 0 else "impar"
            treeview.insert("", "end", tags=(tag,), values=(p.id, p.nombre, p.estado, p.fecha_registro))

    def agregar_proveedor_ui():
        ventana_agregar = tk.Toplevel(ventana)
        ventana_agregar.title("Agregar Proveedor")
        centrar_ventana(ventana_agregar, 350, 150)
        ventana_agregar.configure(bg=COLOR_FONDO)
        ventana_agregar.resizable(False, False)
        ventana_agregar.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))

        tk.Label(ventana_agregar, text="Nombre:", bg=COLOR_FONDO, font=FUENTE_GENERAL).pack(pady=5)
        entry_nombre = tk.Entry(ventana_agregar, font=FUENTE_GENERAL)
        entry_nombre.pack(pady=5)

        def guardar():
            nombre = entry_nombre.get()
            if not nombre:
                messagebox.showerror("Error", "Nombre requerido")
                return
            agregar_proveedor(nombre)
            messagebox.showinfo("Éxito", "Proveedor agregado")
            cargar_datos()
            ventana_agregar.destroy()

        tk.Button(ventana_agregar, text="Guardar", command=guardar, font=FUENTE_GENERAL,
                  bg=COLOR_BOTON, fg="white", relief="flat").pack(pady=10)

    def actualizar_proveedor_ui():
        seleccionado = treeview.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un proveedor")
            return
        datos = treeview.item(seleccionado[0])["values"]
        proveedor = obtener_proveedor_por_id(datos[0])

        ventana_actualizar = tk.Toplevel(ventana)
        ventana_actualizar.title("Actualizar Proveedor")
        centrar_ventana(ventana_actualizar, 350, 200)
        ventana_actualizar.configure(bg=COLOR_FONDO)
        ventana_actualizar.resizable(False, False)
        ventana_actualizar.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))

        tk.Label(ventana_actualizar, text="Nombre:", bg=COLOR_FONDO, font=FUENTE_GENERAL).pack(pady=5)
        entry_nombre = tk.Entry(ventana_actualizar, font=FUENTE_GENERAL)
        entry_nombre.insert(0, proveedor.nombre)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_actualizar, text="Estado:", bg=COLOR_FONDO, font=FUENTE_GENERAL).pack(pady=5)
        estado_var = ttk.Combobox(ventana_actualizar, values=["activo", "inactivo"], font=FUENTE_GENERAL, state="readonly")
        estado_var.set(proveedor.estado)
        estado_var.pack(pady=5)

        def guardar():
            nombre = entry_nombre.get()
            estado = estado_var.get()
            actualizar_proveedor(proveedor.id, nombre, estado)
            messagebox.showinfo("Éxito", "Proveedor actualizado")
            cargar_datos()
            ventana_actualizar.destroy()

        tk.Button(ventana_actualizar, text="Guardar", command=guardar, font=FUENTE_GENERAL,
                  bg=COLOR_BOTON, fg="white", relief="flat").pack(pady=10)

    def eliminar_proveedor_ui():
        seleccionado = treeview.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un proveedor")
            return
        datos = treeview.item(seleccionado[0])["values"]
        eliminar_proveedor(datos[0])
        messagebox.showinfo("Éxito", "Proveedor eliminado")
        cargar_datos()

    # --- Ventana principal ---
    ventana = tk.Toplevel()
    ventana.title("Gestión de Proveedores")
    centrar_ventana(ventana, 700, 500)
    ventana.configure(bg=COLOR_FONDO)
    ventana.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))
    ventana.resizable(False, False)

    # --- Cabecera ---
    header = tk.Frame(ventana, bg=COLOR_HEADER, height=60)
    header.pack(side="top", fill="x")

    try:
        logo = Image.open(ruta_absoluta("logo_proyec.png"))
        logo = logo.resize((40, 40))
        logo_img = ImageTk.PhotoImage(logo)
        tk.Label(header, image=logo_img, bg=COLOR_HEADER).pack(side="left", padx=20)
    except:
        pass

    tk.Label(header, text="Gestión de Proveedores", font=FUENTE_TITULO, fg="white", bg=COLOR_HEADER).pack(side="left")

    # --- Treeview ---
    columns = ("Id_Proveedor", "Nombre", "Estado", "Fecha_Registro")
    treeview = ttk.Treeview(ventana, columns=columns, show="headings")
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center", width=150)
    treeview.pack(fill="both", expand=True, pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="white",fg="black")
    treeview.tag_configure("par", background="white")
    treeview.tag_configure("impar", background="#e6f2ff")
    
    scroll_y = Scrollbar(treeview, orient="vertical", command=treeview.yview)
    treeview.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    treeview.pack(fill="both", expand=True)

    # --- Botones ---
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Agregar", command=agregar_proveedor_ui, font=FUENTE_GENERAL,
              bg=COLOR_BOTON, fg="white", relief="flat", width=15).grid(row=0, column=0, padx=10)
    tk.Button(frame_botones, text="Actualizar", command=actualizar_proveedor_ui, font=FUENTE_GENERAL,
              bg=COLOR_BOTON, fg="white", relief="flat", width=15).grid(row=0, column=1, padx=10)
    tk.Button(frame_botones, text="Eliminar", command=eliminar_proveedor_ui, font=FUENTE_GENERAL,
              bg=COLOR_BOTON, fg="white", relief="flat", width=15).grid(row=0, column=2, padx=10)

    cargar_datos()
    ventana.mainloop()
