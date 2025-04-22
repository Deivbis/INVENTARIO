# producto_backend.py
from tkinter import messagebox
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import declarative_base
from datetime import datetime
from conexion_bd import crear_sesion

Base = declarative_base()
session = crear_sesion()

class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    precio = Column(Float)
    categoria = Column(Integer)
    cantidad_stock = Column(Integer)
    stock_minimo = Column(String(10))
    id_proveedor = Column(Integer)
    estado = Column(Enum('activo', 'inactivo'))
    fecha_registro = Column(DateTime, default=datetime.now)

class Categoria(Base):
    __tablename__ = 'categoria'
    id_categoria = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    descripcion = Column(String(255))
    estado = Column(Enum('activo', 'inactivo'))
    fecha_registro = Column(DateTime, default=datetime.now)

class Proovedor(Base):
    __tablename__ = 'proovedores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    estado = Column(Enum('activo', 'inactivo'))
    fecha_registro = Column(DateTime, default=datetime.now)

def obtener_opciones_existentes():
    categorias = [str(c.id_categoria) for c in session.query(Categoria).all()]
    proveedores = [str(p.id) for p in session.query(Proovedor).all()]
    return categorias, proveedores

def obtener_productos():
    return session.query(Producto).filter(Producto.estado == 'activo').all()

def agregar_producto_backend(producto_data):
    nuevo = Producto(**producto_data)
    session.add(nuevo)
    session.commit()

def eliminar_producto_backend(prod_id):
    producto = session.get(Producto, prod_id)
    if producto:
        producto.estado = 'inactivo'
        session.commit()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
    else:
        messagebox.showerror("Error", "El producto no existe.")

def actualizar_producto_backend(prod_id, nuevos_datos):
    producto = session.get(Producto, prod_id)
    for key, value in nuevos_datos.items():
        setattr(producto, key, value)
    session.commit()

def obtener_producto_por_id(prod_id):
    return session.get(Producto, prod_id)

def filtrar_productos(id=None, nombre=None, categoria=None, id_proveedor=None):
    query = session.query(Producto)

    if id is not None:
        query = query.filter(Producto.id == id)
    if nombre:
        query = query.filter(Producto.nombre.ilike(f"%{nombre}%"))
    if categoria:
        query = query.filter(Producto.categoria == categoria)
    if id_proveedor:
        query = query.filter(Producto.id_proveedor == id_proveedor)

    return query.all()
