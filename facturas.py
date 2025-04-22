import os
import tkinter as tk
from tkinter import Listbox, Button, Scrollbar, messagebox, PhotoImage
import webbrowser
from RUTAS import ruta_absoluta

def listar_facturas():
    folder = ruta_absoluta("reporte")
    if not os.path.exists(folder):
        os.makedirs(folder)

    return [f for f in os.listdir(folder) if f.endswith(".pdf")]

def factura():
    ventana = tk.Toplevel()
    ventana.title("Listado de Facturas - INVENTARY")
    ventana.geometry("600x500")
    ventana.configure(bg="white")
    ventana.resizable(False, False)
    
    # Intentar cargar el logo
    try:
        logo_img = PhotoImage(file=ruta_absoluta("logo_proyec.png"))  # Asegúrate de que esta ruta sea correcta
        logo_img = logo_img.subsample(4, 4)
        logo_label = tk.Label(ventana, image=logo_img, bg="#1C3557")
        logo_label.image = logo_img
        logo_label.pack(side="left", padx=(20, 10), pady=5)
    except Exception as e:
        print(f"Error al cargar el logo: {e}")  # Imprime el error en la consola
        tk.Label(ventana, text="📦", bg="#1C3557", fg="white", font=("Segoe UI", 25)).pack(side="left", padx=20)

    # Encabezado visual estilo INVENTARY
    header = tk.Frame(ventana, bg="#1C3557", height=70)
    header.pack(fill="x")

    tk.Label(header, text="INVENTARY-FACTURAS", bg="#1C3557", fg="white",
             font=("Segoe UI", 20, "bold")).pack(side="left", pady=10)

    # Centrar ventana
    w, h = 600, 500
    x = (ventana.winfo_screenwidth() // 2) - (w // 2)
    y = (ventana.winfo_screenheight() // 2) - (h // 2)
    ventana.geometry(f"{w}x{h}+{x}+{y}")

    # Listbox para mostrar las facturas
    listbox = Listbox(ventana, width=50, height=15, font=("Segoe UI", 10),
                      bg="white", fg="black", bd=1, relief="solid", highlightthickness=0)
    listbox.pack(padx=20, pady=(20, 10))

    # Insertar facturas
    facturas = listar_facturas()
    for factura_item in facturas:
        listbox.insert("end", factura_item)
        
    scroll_y = Scrollbar(listbox, orient="vertical", command=listbox.yview)
    listbox.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    listbox.pack(fill="both", expand=True)

    # Función abrir factura
    def abrir_factura():
        seleccion = listbox.curselection()
        if seleccion:
            factura_seleccionada = listbox.get(seleccion)
            filepath = ruta_absoluta(os.path.join("reporte", factura_seleccionada))
            if os.path.exists(filepath):
                webbrowser.open(filepath)
            else:
                messagebox.showerror("Error", "No se pudo encontrar el archivo de la factura.")
        else:
            messagebox.showwarning("Selección", "Por favor selecciona una factura.")

    # Botón abrir
    abrir_btn = Button(ventana, text="Abrir Factura", command=abrir_factura,
                       bg="#0A74DA", fg="white", font=("Segoe UI", 10, "bold"),
                       relief="flat", padx=10, pady=5)
    abrir_btn.pack(pady=(5, 20))

    ventana.mainloop()
