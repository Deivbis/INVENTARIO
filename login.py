from tkinter import *
from PIL import Image, ImageTk
from login_backend import iniciar_sesion, registrar_usuario
from RUTAS import ruta_absoluta



ventana_principal = Tk()
ventana_principal.title("Login")
ventana_principal.geometry("900x550")
ventana_principal.config(bg="white")
ventana_principal.resizable(0, 0)

ventana_principal.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))

img_pil = Image.open(ruta_absoluta("trasparente.png"))
img_pil = img_pil.resize((470, 560))
img = ImageTk.PhotoImage(img_pil)
label_img = Label(ventana_principal, image=img, bg="white")
label_img.place(x=0, y=0)

frame = Frame(ventana_principal, bg="white", bd=2, relief="groove")
frame.place(x=470, y=20, width=400, height=500)

Label(frame, text="Iniciar Sesión", font=("Arial", 20), bg="white", fg="#374151").place(x=118, y=40)

Label(frame, text="Usuario", font=("Arial", 15), bg="white", fg="#374151").place(x=30, y=130)
usuario = Entry(frame, font=("Arial", 15), bg="white", border=0)
usuario.place(x=30, y=170, width=340, height=30)
Frame(frame, width=340, height=2, bg="black").place(x=30, y=200)

Label(frame, text="Contraseña", font=("Arial", 15), bg="white", fg="#374151").place(x=30, y=230)
contraseña = Entry(frame, font=("Arial", 15), bg="white", show="*", border=0)
contraseña.place(x=30, y=270, width=340, height=30)
Frame(frame, width=340, height=2, bg="black").place(x=30, y=300)

boton = Button(frame, text="Iniciar Sesión", font=("Arial", 15), bg="#374151", fg="white", command=lambda: iniciar_sesion(usuario, contraseña))
boton.place(x=55, y=340, width=290, height=40)

label_img = Label(frame, text="¿No tienes cuenta?", font=("Arial", 10), bg="white", fg="#374151")
label_img.place(x=90, y=390)

def registrar():
    ventana_registro = Toplevel()
    ventana_registro.title("Registrar")
    ventana_registro.geometry("400x500")
    ventana_registro.config(bg="white")
    ventana_registro.resizable(False, False)
    ventana_registro.iconphoto(False, PhotoImage(file=ruta_absoluta("logo_proyec.png")))

    Label(ventana_registro, text="Registrarse", font=("Arial", 18, "bold"), bg="white", fg="#374151").pack(pady=30)

    Label(ventana_registro, text="Usuario", bg="white", font=("Arial", 10)).pack(anchor="w", padx=60)
    usuario_entry = Entry(ventana_registro, bd=0, font=("Arial", 12), bg="white", fg="black")
    usuario_entry.pack(padx=60, fill="x")
    Frame(ventana_registro, height=1, bg="black").pack(padx=60, fill="x", pady=(0, 10))

    Label(ventana_registro, text="Contraseña", bg="white", font=("Arial", 10)).pack(anchor="w", padx=60)
    contraseña_entry = Entry(ventana_registro, bd=0, show="*", font=("Arial", 12), bg="white", fg="black")
    contraseña_entry.pack(padx=60, fill="x")
    Frame(ventana_registro, height=1, bg="black").pack(padx=60, fill="x", pady=(0, 10))

    Label(ventana_registro, text="Email", bg="white", font=("Arial", 10)).pack(anchor="w", padx=60)
    Email_entry = Entry(ventana_registro, bd=0, font=("Arial", 12), bg="white", fg="black")
    Email_entry.pack(padx=60, fill="x")
    Frame(ventana_registro, height=1, bg="black").pack(padx=60, fill="x", pady=(0, 10))

    estado_entry = Entry(ventana_registro)
    estado_entry.insert(0, "activo")
    estado_entry.place_forget()

    id_rol_entry = Entry(ventana_registro)
    id_rol_entry.insert(0, "2")
    id_rol_entry.place_forget()

    Button(
        ventana_registro,
        text="Registrarme",
        command=lambda: registrar_usuario(usuario_entry, contraseña_entry, Email_entry, estado_entry, id_rol_entry),
        font=("Arial", 12), bg="#374151", fg="white", bd=0, padx=10, pady=5,
        activebackground="#1f2937", activeforeground="white"
    ).pack(pady=30, ipadx=10, ipady=5)

    Label(ventana_registro, text="¿Ya tienes cuenta?", bg="white", font=("Arial", 10)).pack()
    Button(ventana_registro, text="Iniciar Sesión", command=ventana_registro.destroy, font=("Arial", 10, "underline"),
           fg="#1f2937", bg="white", bd=0, cursor="hand2").pack(pady=5)

    ventana_registro.mainloop()

boton_registro = Button(frame, text="Registrate", command=lambda: registrar(), font=("Arial", 10), bg="white", fg="#374151", border=0)
boton_registro.place(x=210, y=390, width=90, height=20)

ventana_principal.mainloop()
