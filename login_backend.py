from tkinter import messagebox
import traceback
from sqlalchemy import  Column, String, Integer, Date, select
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
import bcrypt
from conexion_bd import crear_sesion
from principal import abrir_menu

# Crear base declarativa
Base = declarative_base()

# Modelo de la tabla
class registro_usuario(Base):
    __tablename__ = 'registro_usuarios'
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False)
    contraseña = Column(String(64), nullable=False)
    Email=Column(String(50), nullable=False)
    estado = Column(String(20))
    fecha_registro = Column(Date)
    id_rol = Column(Integer)

# Función para iniciar sesión sin hashear la contraseña
def iniciar_sesion(usuario_entry, contraseña_entry):
    sesion = crear_sesion()
    if sesion is None:
        return

    try:
        usuario_input = usuario_entry.get()
        contraseña_input = contraseña_entry.get()

        stmt = select(registro_usuario).where(registro_usuario.usuario == usuario_input)
        resultado = sesion.execute(stmt).scalar_one_or_none()

        if resultado and bcrypt.checkpw(contraseña_input.encode('utf-8'), resultado.contraseña.encode('utf-8')):
            messagebox.showinfo("Inicio de sesión", f"Bienvenido {usuario_input}")
            abrir_menu(resultado.id_rol)
        else:
            messagebox.showerror("Inicio de sesión", "Usuario o contraseña incorrectos")

    except Exception as e:
        traceback.print_exc()  # 🔍 Esto imprime el error completo en consola
        messagebox.showerror("Error durante la autenticación", str(e))
    finally:
        sesion.close()



def registrar_usuario(usuario_entry, contraseña_entry,Email_entry, estado_entry, id_rol_entry):
    sesion = crear_sesion()
    if sesion is None:
        return

    try:
        usuario_input = usuario_entry.get().strip()
        contraseña_input = contraseña_entry.get().strip()
        Email_input = Email_entry.get().strip()
        estado_input = estado_entry.get().strip()
        id_rol_input= id_rol_entry.get().strip()

        if not usuario_input or not contraseña_input:
            messagebox.showerror("Error", "Usuario y contraseña son obligatorios")
            return

        # Convertir id_rol a entero
        try:
            id_rol_input = int(id_rol_input)
        except ValueError:
            messagebox.showerror("Error", "ID Rol debe ser un número entero")
            return

        # Verificar que el usuario no exista
        stmt = select(registro_usuario).where(registro_usuario.usuario == usuario_input)
        resultado = sesion.execute(stmt).scalar_one_or_none()

        if resultado:
            messagebox.showerror("Error", "El usuario ya existe")
            return

# Hashear la contraseña
        hashed_password = bcrypt.hashpw(contraseña_input.encode('utf-8'), bcrypt.gensalt())

        # Crear nuevo usuario con contraseña hasheada
        nuevo_usuario = registro_usuario(
            usuario=usuario_input,
            contraseña=hashed_password.decode('utf-8'),
            Email=Email_input,
            estado=estado_input,
            fecha_registro=date.today(),
            id_rol=id_rol_input
        )


        sesion.add(nuevo_usuario)
        sesion.commit()
        messagebox.showinfo("Registro exitoso", f"Usuario '{usuario_input}' registrado correctamente")

    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar el usuario: {e}")
    finally:
        sesion.close()

    