import os
import tkinter as tk
from tkinter import Listbox, Button, Scrollbar, messagebox, PhotoImage
import webbrowser
from RUTAS import ruta_absoluta


HISTORIAL_DIR = ruta_absoluta("historial")  

def listar_historial():
    if not os.path.exists(HISTORIAL_DIR):
        os.makedirs(HISTORIAL_DIR)
    return [f for f in os.listdir(HISTORIAL_DIR) if f.endswith(".pdf")]

def ver_historial():
    ventana = tk.Toplevel()
    ventana.title("Listado de Historial - INVENTARY")
    ventana.geometry("600x500")
    ventana.configure(bg="white")
    ventana.resizable(False, False)
    ventana.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))  # Cambia si es necesario

    # Centrar ventana
    w, h = 600, 500
    x = (ventana.winfo_screenwidth() // 2) - (w // 2)
    y = (ventana.winfo_screenheight() // 2) - (h // 2)
    ventana.geometry(f"{w}x{h}+{x}+{y}")

    # Encabezado visual estilo INVENTARY
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

    tk.Label(header, text="INVENTARY - HISTORIAL", bg="#1C3557", fg="white",
             font=("Segoe UI", 20, "bold")).pack(side="left", pady=10)

    # Listbox para mostrar el historial
    listbox = Listbox(ventana, width=50, height=15, font=("Segoe UI", 10),
                      bg="white", fg="black", bd=1, relief="solid", highlightthickness=0)
    listbox.pack(padx=20, pady=(20, 10), fill="both", expand=True)

    # Insertar archivos del historial
    historial_archivos = listar_historial()
    for historial_item in historial_archivos:
        listbox.insert("end", historial_item)

    scroll_y = Scrollbar(listbox, orient="vertical", command=listbox.yview)
    listbox.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    # Función para abrir el historial
    def abrir_historial():
        seleccion = listbox.curselection()
        if seleccion:
            historial_seleccionado = listbox.get(seleccion)
            filepath = os.path.join(HISTORIAL_DIR, historial_seleccionado)
            webbrowser.open(filepath)
        else:
            messagebox.showwarning("Selección", "Por favor selecciona un historial.")

    # Botón para abrir historial
    abrir_btn = Button(ventana, text="Abrir Historial", command=abrir_historial,
                       bg="#0A74DA", fg="white", font=("Segoe UI", 10, "bold"),
                       relief="flat", padx=10, pady=5)
    abrir_btn.pack(pady=(5, 20))

    ventana.mainloop()
