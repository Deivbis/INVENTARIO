from sqlalchemy import create_engine
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker


def crear_sesion():
    try:
        engine = create_engine("mysql+mysqlconnector://root:@localhost/inventary?charset=utf8mb4")
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None