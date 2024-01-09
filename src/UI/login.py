import tkinter as tk
from src.res.Colors import verde, rojo, rojo_oscuro
from src.db.models import Usuario
from src.UC.usercases import verifyUser, internetOn
import src.UI.splashScreen as info
class Login:
    def __init__(self, root):
        root.overrideredirect(False)
        self.root = root
        self.root.update()
        x = int(root.winfo_screenwidth() * 0.25)
        y = int(root.winfo_screenheight() * 0.05)
        self.root.geometry(f"500x700+{x}+{y}")

    
    def loginFrame(self):
        self.frame2 = tk.Frame(self.root, width=500, height=700, bg=verde)
        self.frame2.grid(row=0, column=0)

        self.frame2.tkraise()
        self.frame2.pack_propagate(False)
        self.root.title("Inicio de Sesión")

        etiqueta_usuario = tk.Label(self.frame2, text="Usuario:", bg=verde, fg="white", font=("Arial", 24))
        etiqueta_usuario.pack(pady=(100, 0))

        self.entrada_usuario = tk.Entry(self.frame2, font=("Arial", 20))
        self.entrada_usuario.pack(pady=(0, 50))

        etiqueta_contraseña = tk.Label(self.frame2, text="Contraseña:", bg=verde, fg="white", font=("Arial", 24))
        etiqueta_contraseña.pack()

        self.entrada_contraseña = tk.Entry(self.frame2, show="*", font=("Arial", 20))
        self.entrada_contraseña.pack()

        boton_iniciar_sesion = tk.Button(self.frame2,
                                         text="Iniciar Sesión", font=("Arial", 20),
                                         fg="white", activeforeground=verde,
                                         bg=rojo, activebackground=rojo_oscuro,
                                         cursor="hand2",
                                         command=self.iniciar_sesion)
        boton_iniciar_sesion.pack(pady=(100, 50))

        self.etiqueta_estado = tk.Label(self.frame2, text="")
        self.etiqueta_estado.pack()

        etiqueta_info = tk.Label(self.frame2, text="")
        etiqueta_info.pack()

        print("iniciando ventana 2")

    def iniciar_sesion(self):
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_contraseña.get()

        if internetOn():
            if verifyUser(Usuario(nickname=usuario, password=contraseña)):
                print("usuario correcto")
                self.etiqueta_estado.config(text="Inicio de sesión Correcto")
                # self.frame2.destroy()
                self.goToFrame1()
            else:
                self.etiqueta_estado.config(text="contraseña o usuario incorrecto")
        else:
            self.etiqueta_estado.config(text="Conectate a internet para continuar")

    def goToFrame1(self):
        self.frame2.destroy()
        frame1 = info.SplashScreen(self.root)
        frame1.splashFrame()