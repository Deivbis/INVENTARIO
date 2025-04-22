import tkinter as tk
from tkinter import Scrollbar, ttk
from tkinter import PhotoImage
from datetime import datetime, timezone
from control_stock_backend import crear_sesion
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from RUTAS import ruta_absoluta

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    cantidad_stock = Column(Integer, nullable=False)
    movimientos = relationship("Movimiento", back_populates="producto")

class Movimiento(Base):
    __tablename__ = 'movimientos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    motivo = Column(String(50), nullable=False)  
    fecha = Column(DateTime, default=datetime.now(timezone.utc))
    producto = relationship("Producto", back_populates="movimientos")

Session = crear_sesion

def ventana_movimientos(master=None):
    ventana = tk.Toplevel(master)
    ventana.title("Historial de Movimientos - INVENTARY")
    ventana.geometry("950x600")
    ventana.configure(bg="white")
    ventana.resizable(False, False)
    ventana.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))  # Cambia si es necesario

    # Centrar ventana
    w, h = 950, 600
    x = (ventana.winfo_screenwidth() // 2) - (w // 2)
    y = (ventana.winfo_screenheight() // 2) - (h // 2)
    ventana.geometry(f"{w}x{h}+{x}+{y}")

    # Encabezado
    header = tk.Frame(ventana, bg="#1C3557", height=70)
    header.pack(fill="x")

    try:
        logo_img = PhotoImage(file=ruta_absoluta("logo_proyec.png"))  # Asegúrate de que esta ruta sea correcta
        logo_img = logo_img.subsample(4, 4)
        logo_label = tk.Label(header, image=logo_img, bg="#1C3557")
        logo_label.image = logo_img
        logo_label.pack(side="left", padx=(20, 10), pady=5)
    except:
        tk.Label(header, text="📦", bg="#1C3557", fg="white", font=("Segoe UI", 25)).pack(side="left", padx=20)

    tk.Label(header, text="INVENTARY-MOVIMIENTOS", bg="#1C3557", fg="white",
             font=("Segoe UI", 20, "bold")).pack(side="left", pady=10)

    # Filtros
    frame_filtros = tk.Frame(ventana, bg="white")
    frame_filtros.pack(pady=(15, 5))

    filtro_tipo = ttk.Combobox(frame_filtros, values=["Todos", "Entrada", "Venta", "Salida"], state="readonly", width=15)
    filtro_tipo.set("Todos")
    filtro_tipo.grid(row=0, column=0, padx=10)

    entry_busqueda = tk.Entry(frame_filtros, width=30, font=("Segoe UI", 10))
    entry_busqueda.grid(row=0, column=1, padx=10)

    # Treeview con scrollbar
    frame_tree = tk.Frame(ventana, bg="white")
    frame_tree.pack(padx=15, pady=(10, 15), fill="both", expand=True)

    columnas = ("ID", "Producto", "Tipo", "Cantidad", "Motivo", "Fecha")
    tree = ttk.Treeview(frame_tree, columns=columnas, show='headings', height=20)

    scroll_y = Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    for col in columnas:
        tree.heading(col, text=col)

    tree.column("ID", width=50, anchor="center")
    tree.column("Producto", width=200, anchor="center")
    tree.column("Tipo", width=100, anchor="center")
    tree.column("Cantidad", width=80, anchor="center")
    tree.column("Motivo", width=200, anchor="center")
    tree.column("Fecha", width=170, anchor="center")

    # Botón buscar
    boton_buscar = tk.Button(frame_filtros, text="Buscar",
                             command=lambda: cargar_movimientos(filtro_tipo, entry_busqueda, tree),
                             bg="#0A74DA", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=10, pady=2)
    boton_buscar.grid(row=0, column=2, padx=10)

    # Estilos
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=26,
                    font=("Segoe UI", 10),
                    fieldbackground="white")

    style.configure("Treeview.Heading",
                    font=("Segoe UI", 10, "bold"),
                    background="white",
                    foreground="black")

    style.map("Treeview",
              background=[("selected", "#D0E4FF")])

    tree.tag_configure('par', background="#E3F2FD")
    tree.tag_configure('impar', background="white")

    # Cargar datos
    cargar_movimientos(filtro_tipo, entry_busqueda, tree)


def cargar_movimientos(filtro_tipo, entry_busqueda, tree):
    session = Session()
    filtro = filtro_tipo.get()
    busqueda = entry_busqueda.get().lower()

    query = session.query(Movimiento).join(Producto).filter(Producto.nombre.ilike(f"%{busqueda}%"))
    if filtro != "Todos":
        query = query.filter(Movimiento.motivo.ilike(f"{filtro}"))

    movimientos = query.order_by(Movimiento.fecha.desc()).all()

    # Limpiar Treeview
    for row in tree.get_children():
        tree.delete(row)

    for i, mov in enumerate(movimientos):
        tipo = "Entrada" if mov.motivo.lower() == "entrada" else "Salida"
        nombre_producto = mov.producto.nombre if mov.producto else "Desconocido"
        fecha_formateada = mov.fecha.strftime("%Y-%m-%d %H:%M") if mov.fecha else ""
        tag = 'par' if i % 2 == 0 else 'impar'
        tree.insert("", tk.END, values=(
            mov.id,
            nombre_producto,
            tipo,
            mov.cantidad,
            mov.motivo,
            fecha_formateada
        ), tags=(tag,))
    
    session.close()
