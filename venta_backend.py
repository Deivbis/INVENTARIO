from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import DECIMAL
from conexion_bd import crear_sesion

# Crear la base
Base = declarative_base()

class Movimiento(Base):
    __tablename__ = 'movimientos'
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey('producto.id'))
    cantidad = Column(Integer)
    motivo = Column(String)
    fecha = Column(DateTime, default=datetime.now)

    producto = relationship("Producto")
   
class Cliente(Base):
    __tablename__ = 'cliente'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True)

    ventas = relationship('Venta', back_populates='cliente')

    def __repr__(self):
        return f"<Cliente(id_cliente={self.id_cliente}, nombre={self.nombre}, telefono={self.telefono}, correo={self.correo})>"

class Venta(Base):
    __tablename__ = 'ventas'

    id_venta = Column(Integer, primary_key=True, autoincrement=True)
    cantidad_inicial = Column(Integer, nullable=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    cantidad_actual = Column(Integer, nullable=True)
    estado = Column(String(20), default='activo')
    precio_unitario = Column(DECIMAL(10,2), nullable=True)
    fecha_registro = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    total = Column(Float, nullable=True)

    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship('DetalleVenta', back_populates='venta')

    def __repr__(self):
        return f"<Venta(id={self.id_venta}, fecha_registro={self.fecha_registro}, total={self.total}, id_cliente={self.id_cliente})>"

class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    total = Column(Float, nullable=False)  # Asegurarse de que el total nunca sea None
    id_producto = Column(Integer, ForeignKey('producto.id'), nullable=False)
    id_venta = Column(Integer, ForeignKey('ventas.id_venta'), nullable=False)
    estado = Column(String(20), default='activo')
    fecha_registro = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    venta = relationship('Venta', back_populates='detalles')
    producto = relationship('Producto', back_populates='detalles')

    def __repr__(self):
        return f"<DetalleVenta(id={self.id}, cantidad={self.cantidad}, precio_unitario={self.precio_unitario}, total={self.total}, venta_id={self.id_venta}, producto_id={self.id_producto})>"

class Producto(Base):
    __tablename__ = 'producto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    cantidad_stock = Column(Integer, nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    estado = Column(String(20), default='activo')
    fecha_registro = Column(String, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    detalles = relationship('DetalleVenta', back_populates='producto')
    movimientos = relationship('Movimiento', back_populates='producto')

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre={self.nombre}, precio={self.precio}, stock={self.cantidad_stock})>"

# Crear la sesión
SessionLocal = crear_sesion

def create_cliente(db_session, nombre, telefono=None, correo=None):
    cliente = Cliente(nombre=nombre, telefono=telefono, correo=correo)
    db_session.add(cliente)
    db_session.commit()
    db_session.refresh(cliente)
    return cliente

def obtener_o_crear_cliente(db_session, nombre, telefono=None, correo=None):
    cliente = db_session.query(Cliente).filter_by(nombre=nombre).first()
    if cliente:
        return cliente
    return create_cliente(db_session, nombre, telefono, correo)

def create_venta(db_session, id_cliente, total):
    fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    venta = Venta(id_cliente=id_cliente, total=total, fecha_registro=fecha_registro)
    db_session.add(venta)
    db_session.commit()
    db_session.refresh(venta)
    return venta

def create_detalle_venta(db_session, cantidad, precio_unitario, id_producto, id_venta):
    # Buscar el producto
    producto = db_session.query(Producto).filter_by(id=id_producto).first()
    if producto is None:
        raise ValueError("Producto no encontrado")

    if producto.cantidad_stock < cantidad:
        raise ValueError("Stock insuficiente")

    # Descontar stock
    producto.cantidad_stock -= cantidad

    # Calcular el total de esta línea
    total_linea = cantidad * precio_unitario

    # Asegurarse de que el total_linea nunca sea None o 0
    if total_linea is None or total_linea <= 0:
        raise ValueError("El total de la línea de venta es inválido")

    # Crear detalle de venta
    detalle_venta = DetalleVenta(
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        total=total_linea,
        id_producto=id_producto,
        id_venta=id_venta
    )

    db_session.add(detalle_venta)
    db_session.commit()
    db_session.refresh(detalle_venta)

    return detalle_venta

def registrar_venta_completa(db_session, nombre_cliente, productos):
    """
    productos: lista de diccionarios con keys: id_producto, cantidad
    """
    try:
        cliente = obtener_o_crear_cliente(db_session, nombre_cliente)
        total = 0
        detalles_temp = []

        # Verificar y preparar los productos
        for item in productos:
            producto = db_session.query(Producto).filter_by(id=item["id_producto"]).first()
            if producto is None or producto.cantidad_stock < item["cantidad"]:
                raise ValueError(f"Producto inválido o sin stock: {item['id_producto']}")

            subtotal = item["cantidad"] * producto.precio
            total += subtotal
            producto.cantidad_stock -= item["cantidad"]
            detalles_temp.append({
                "cantidad": item["cantidad"],
                "precio_unitario": producto.precio,
                "id_producto": producto.id
            })

        # Verificar que el total no sea 0
        if total <= 0:
            raise ValueError("El total de la venta no puede ser 0.")

        # Crear la venta
        venta = Venta(id_cliente=cliente.id_cliente, total=total, fecha_registro=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db_session.add(venta)
        db_session.flush()  # Flush para obtener el id_venta

        # Crear los detalles de venta asociados
        for detalle in detalles_temp:
            total_linea = detalle["cantidad"] * detalle["precio_unitario"]

            # Asegurarse de que el total nunca sea None o 0
            if total_linea is None or total_linea <= 0:
                raise ValueError("El total de una línea de detalle es inválido")

            detalle_venta = DetalleVenta(
                cantidad=detalle["cantidad"],
                precio_unitario=detalle["precio_unitario"],
                total=total_linea,
                id_producto=detalle["id_producto"],
                id_venta=venta.id_venta
            )
            db_session.add(detalle_venta)

        # Confirmar todo junto
        db_session.commit()

        print(f"Venta registrada con éxito: {venta.id_venta} con total {total}")
        return venta

    except Exception as e:
        db_session.rollback()
        print(f"Error al registrar la venta: {e}")
        raise e
