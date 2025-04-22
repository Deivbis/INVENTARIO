from sqlalchemy import create_engine
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
import pymysql
pymysql.install_as_MySQLdb()


def crear_sesion():
    try:
        engine = create_engine("mysql+pymysql://root:@localhost/inventary?charset=utf8mb4")
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None