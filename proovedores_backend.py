from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
from conexion_bd import crear_sesion

# Configuración de la base de datos
Base = declarative_base()
session = crear_sesion()  # Crear la sesión para interactuar con la base de datos

class Proovedor(Base):
    __tablename__ = 'proovedores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(String(20), default='activo')
    fecha_registro = Column(DateTime, default=datetime.datetime.now)

# Funciones del Backend

def obtener_proveedores_activos():
    """Obtiene todos los proveedores con estado 'activo'"""
    return session.query(Proovedor).filter(Proovedor.estado == "activo").all()

def agregar_proveedor(nombre):
    """Agrega un nuevo proveedor a la base de datos"""
    nuevo_proveedor = Proovedor(nombre=nombre)
    session.add(nuevo_proveedor)
    session.commit()

def obtener_proveedor_por_id(proveedor_id):
    """Obtiene un proveedor por su ID"""
    return session.get(Proovedor, proveedor_id)

def actualizar_proveedor(proveedor_id, nombre, estado):
    """Actualiza los detalles de un proveedor"""
    proveedor = obtener_proveedor_por_id(proveedor_id)
    if proveedor:
        proveedor.nombre = nombre
        proveedor.estado = estado
        session.commit()

def eliminar_proveedor(proveedor_id):
    """Elimina un proveedor (cambia su estado a inactivo)"""
    proveedor = obtener_proveedor_por_id(proveedor_id)
    if proveedor:
        proveedor.estado = "inactivo"
        session.commit()
