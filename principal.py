import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
from Producto import productos
from movimientos import ventana_movimientos
from Proovedores import proveedores
from control_stocks import control_stock
from Categoria import categorias 
from filtro import filtro_busqueda
from venta import ventas
from  facturas import factura
from  historial import ver_historial
from reportes import generar_reporte_movimientos
from RUTAS import ruta_absoluta

# Colores personalizados estilo moderno en tonos azules
COLOR_FONDO = "#eaf3fc"
COLOR_HEADER = "#1e3a5f"
COLOR_BOTON_BG = "#ffffff"
COLOR_BOTON_FG = "#1e3a5f"
COLOR_BOTON_BORDE = "#a6c8eb"
COLOR_HOVER = "#d4e6fb"

def abrir_menu(id_rol):
    def abrir_productos():
        productos()

    def abrir_proveedores():
        proveedores()

    def abrir_stock():
        control_stock()

    def abrir_categorias():
        categorias()

    def facturas():
        factura()

    def reporte():
        ver_historial()

    def buscar():
        filtro_busqueda()
        
    def movimientos():
        ventana_movimientos()

    def vender():
        ventas()

    def generar_reporte():
        generar_reporte_movimientos()
        messagebox.showinfo("Reporte", "Reporte generado exitosamente en la carpeta 'historial'.")

    def salir():
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
            ventana.destroy()
            
            
    ventana = tk.Toplevel()
    ventana.title("Menú Principal - Sistema de Inventario")
    ventana.geometry("700x660")
    ventana.configure(bg=COLOR_FONDO)
    ventana.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))
    ventana.resizable(False, False)

    # Header con título
    header = tk.Frame(ventana, bg=COLOR_HEADER, height=60)
    header.pack(fill=tk.X)
    tk.Label(
        header,
        text="INVENTARY",
        font=("Segoe UI", 20, "bold"),
        bg=COLOR_HEADER,
        fg="white"
    ).pack(pady=15)
    
    IMG=Image.open(ruta_absoluta("logo_proyec.png"))
    IMG=IMG.resize((70, 70))
    img=ImageTk.PhotoImage(IMG)
    label_img=tk.Label(header, image=img, bg=COLOR_FONDO)
    label_img.place(x=0, y=0)

    # Mensaje de bienvenida
    tk.Label(
        ventana,
        text="Bienvenido al menú principal",
        font=("Segoe UI", 14),
        bg=COLOR_FONDO,
        fg="#3b3b3b"
    ).pack(pady=(10, 10))

    # Contenedor de botones
    contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
    contenedor.pack(padx=20, pady=5)

    if id_rol == 1: #este id es el de administrador
        ############# ID ROL 1 ADMINISTRADOR ################
        botones = [
            ("📦\nProductos", abrir_productos),
            ("📂\nCategorías", abrir_categorias),
            ("🔍\nBuscar", buscar),
            ("🧾\nVentas", vender),
            ("🏢\nProveedores", abrir_proveedores),
            ("📊\nStock", abrir_stock),
            ("📑\nFacturas", facturas),
            ("📜\nMovimientos", movimientos),
            ("📋\nReportes", reporte),
            ("🗂️\nGenerar Reporte",generar_reporte ),

            ("❌\nSalir", salir)
        ]
    elif id_rol == 2:#este id es el de empleado
        ############# ID ROL 2 EMPLEADO ################
        botones = [
            ("📦\nProductos", abrir_productos),
            ("🔍\nBuscar", buscar),
            ("🧾\nVentas", vender),
            ("📑\nFacturas", facturas),
            ("📜\nMovimientos", movimientos),
            ("❌\nSalir", salir)
        ]

    columnas = 3

    for index, (texto, comando) in enumerate(botones):
        fila = index // columnas
        columna = index % columnas

        frame = tk.Frame(contenedor, bg=COLOR_FONDO)
        frame.grid(row=fila, column=columna, padx=10, pady=10)

        btn = tk.Button(
            frame,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_BOTON_BG,
            fg=COLOR_BOTON_FG,
            width=14,
            height=5,
            relief="raised",
            command=comando,
            wraplength=100,
            justify="center",
            bd=2,
            highlightthickness=0,
            cursor="hand2",
            activebackground=COLOR_HOVER,
            activeforeground=COLOR_BOTON_FG
        )

        def on_enter(e, b=btn):
            b.config(bg=COLOR_HOVER)

        def on_leave(e, b=btn):
            b.config(bg=COLOR_BOTON_BG)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        btn.pack()
        
    
        
    ventana.mainloop()
