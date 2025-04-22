from conexion_bd import crear_sesion
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

SessionLocal = crear_sesion
Base = declarative_base()

# Definición de los modelos (Producto y Movimiento)
class Producto(Base):
    __tablename__ = 'producto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    categoria = Column(String(50), nullable=False)
    cantidad_stock = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=0)
    estado = Column(String(20), default="activo")
    fecha_registro = Column(DateTime, default=datetime.now(timezone.utc))

    movimientos = relationship("Movimiento", back_populates="producto")

class Movimiento(Base):
    __tablename__ = 'movimientos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    motivo = Column(String(50), nullable=False)  # "Aumento" o "Disminución"
    fecha = Column(DateTime, default=datetime.now(timezone.utc))

    producto = relationship("Producto", back_populates="movimientos")


# Funciones del Backend

def crear_sesion():
    return SessionLocal()

def obtener_productos():
    session = crear_sesion()
    productos = session.query(Producto).all()
    session.close()
    return productos

def verificar_stock_bajo():
    session = crear_sesion()
    productos_bajos = session.query(Producto).filter(Producto.cantidad_stock < Producto.stock_minimo).all()
    session.close()
    return productos_bajos

def actualizar_stock(producto_id, nuevo_stock):
    session = crear_sesion()
    producto = session.get(Producto, producto_id)
    if producto:
        nuevo_stock = int(nuevo_stock)
        cantidad_anterior = producto.cantidad_stock
        producto.cantidad_stock = nuevo_stock
        session.commit()
        registrar_movimiento(producto_id, cantidad_anterior, nuevo_stock, "entrada" if nuevo_stock > cantidad_anterior else "salida")
    session.close()

def actualizar_stock_minimo(producto_id, nuevo_minimo):
    session = crear_sesion()
    producto = session.query(Producto).get(producto_id)
    if producto:
        nuevo_minimo = int(nuevo_minimo)
        producto.stock_minimo = nuevo_minimo
        session.commit()
    session.close()

def registrar_movimiento(producto_id, tipo, cantidad, motivo):
    session = crear_sesion()
    cantidad_movimiento = cantidad if tipo == "entrada" else -cantidad
    movimiento = Movimiento(
        producto_id=producto_id,
        cantidad=cantidad_movimiento,
        motivo=motivo,
        fecha=datetime.now(timezone.utc)
    )
    session.add(movimiento)
    session.commit()
    session.close()
