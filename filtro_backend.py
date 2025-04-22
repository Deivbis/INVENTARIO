# producto_backend.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from conexion_bd import crear_sesion

Base = declarative_base()
session = crear_sesion()

class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    precio = Column(Float)
    categoria = Column(Integer)
    cantidad_stock = Column(Integer)
    stock_minimo = Column(Integer)
    id_proveedor = Column(Integer)
    estado = Column(String)
    fecha_registro = Column(DateTime)

def buscar_productos(id_busqueda="", nombre_busqueda="", categoria_filtro=""):
    try:
        query = session.query(Producto)

        if id_busqueda.strip().isdigit():
            query = query.filter(Producto.id == int(id_busqueda.strip()))
        
        if nombre_busqueda:
            query = query.filter(Producto.nombre.ilike(f"%{nombre_busqueda.strip().lower()}%"))
        
        if categoria_filtro and categoria_filtro.isdigit():
            query = query.filter(Producto.categoria == int(categoria_filtro))

        return query.all()
    except Exception as e:
        raise e


def obtener_categorias():
    categorias = sorted(set([
        str(p.categoria) for p in session.query(Producto.categoria).all() if p.categoria is not None
    ]))
    return categorias if categorias else ["No hay categorías"]
