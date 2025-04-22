from sqlalchemy import  Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from tkinter import messagebox
import datetime
from conexion_bd import crear_sesion

# Configuración de SQLAlchemy
Base = declarative_base()

class Categoria(Base):
    __tablename__ = 'categoria'

    id_categoria = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String, nullable=False)
    estado = Column(String, default='activo')
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow)


# Funciones para interactuar con la base de datos
def obtener_categorias():
    session = crear_sesion()
    categorias = session.query(Categoria).filter(Categoria.estado == 'activo').all()  # Filtra solo activos
    session.close()
    return categorias

def agregar_categoria(nombre, descripcion, estado="activo"):
    session = crear_sesion()
    nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion, estado=estado)
    session.add(nueva_categoria)
    session.commit()
    session.close()

def actualizar_categoria(id_categoria, nombre, descripcion, estado):
    session = crear_sesion()
    categoria = session.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
    if categoria:
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        categoria.estado = estado
        session.commit()
    else:
        messagebox.showwarning("Advertencia", "Categoría no encontrada.")
    session.close()


def eliminar_categoria(id_categoria):
    session = crear_sesion()
    categoria = session.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
    if categoria:
        categoria.estado = 'inactivo'
        session.commit()
        messagebox.showinfo("Eliminación", "Categoría eliminada exitosamente.")
    else:
        messagebox.showwarning("Advertencia", "Categoría no encontrada.")
    session.close()

