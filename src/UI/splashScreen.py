import tkinter as tk
from tkinter import ttk, messagebox
from src.res.Colors import verde, marron
import src.res.Strings as Texts
from PIL import Image, ImageTk
import time
from src.UC.usercases import updateUser, getAllFuerzaUC, getAllMunicipiosUC, getAllPaisesUC, getAllPuntosIUC
from src.UC.usercases import internetOn
from src.UI.login import Login
from src.UI.screenContenedor import ContenedorScreen

class SplashScreen:
    def __init__(self, root):
        w = 500
        h = 700
        x = int((root.winfo_screenwidth() - w) * 0.5)
        y = int((root.winfo_screenheight() - h) * 0.5)
        root.geometry(f"{w}x{h}+{x}+{y}")
        self.root = root
        # self.root.geometry(f"500x700+{x}+{y}")

    
    def splashFrame(self):
        self.frame1 = tk.Frame(self.root, width=500, height=700, bg=verde)
        self.frame1.grid(row=0, column=0)

        self.root.update()
        self.frame1.tkraise()
        self.frame1.pack_propagate(False)

        # esconder la barra superior
        # self.root.overrideredirect(True)

        tk.Label(
            self.frame1,
            text=Texts.Splash_label1,
            bg=verde,
            fg="white",
            font=("Arial", 30)
        ).pack(pady=(10,25))

        tk.Label(
            self.frame1,
            text=Texts.Splash_label2,
            bg=verde,
            fg="white",
            font=("Arial", 12)
        ).pack(pady=(0,0))

        tk.Label(
            self.frame1,
            text=Texts.Splash_label3,
            bg=verde,
            fg="white",
            font=("Arial", 12)
        ).pack(pady=15)

        tk.Label(
            self.frame1,
            text=Texts.Splash_label4,
            bg=verde,
            fg=marron,
            font=("Arial", 15)
        ).pack(pady=(10,25))

        imageINM = Image.open("src/res/drawable/inami.png")
        width_i, height_i = imageINM.size
        imageINM = imageINM.resize((width_i//3, height_i//3))
        logo = ImageTk.PhotoImage(imageINM)
        logo_widget = tk.Label(self.frame1, image=logo, background=verde)
        logo_widget.image = logo
        logo_widget.pack()

        tk.Label(
            self.frame1,
            text=Texts.Splash_label5,
            bg=verde,
            fg="white",
            font=("Arial", 10)
        ).pack(pady=(20,0))

        self.etiqueta_estado = tk.Label(self.frame1, text="", bg=verde, fg=marron)
        self.etiqueta_estado.pack(pady=(10,0))

        self.barra_progreso = ttk.Progressbar(self.frame1, orient="horizontal", length=200, mode="determinate")
        self.barra_progreso.pack(pady=(0,10))

        self.comenzar_progreso()

    def comenzar_progreso(self):
        # print("antes usuario")
        movim = updateUser()
        # print(movim)
        if movim:
            connected = internetOn()

            if connected:
                self.refresh_cont(10)
                getAllPaisesUC()

                self.refresh_cont(20)
                getAllMunicipiosUC()

                self.refresh_cont(30)
                getAllPuntosIUC()

                self.refresh_cont(40)
                getAllFuerzaUC()
            else:
                self.msg_NoInternet()

            # Inicia la barra de progreso con una actualización cada 10 milisegundos
            for i in range(0, 101, 4):
                self.barra_progreso["value"] = i  # Actualiza el valor de la barra de progreso
                self.etiqueta_estado.config(text=f"Cargando... {i}%")
                self.frame1.update_idletasks()  # Actualiza la ventana para mostrar el progreso
                time.sleep(0.05)  # Simula una tarea de carga

            self.etiqueta_estado.config(text="Carga completa")
            self.goToFrame3()
        else:
            for i in range(0, 101, 4):
                self.barra_progreso["value"] = i  # Actualiza el valor de la barra de progreso
                self.etiqueta_estado.config(text=f"Cargando... {i}%")
                self.frame1.update_idletasks()  # Actualiza la ventana para mostrar el progreso
                time.sleep(0.01)  # Simula una tarea de carga

            self.etiqueta_estado.config(text="Carga completa")
            self.goToFrame2()

    def refresh_cont(self, j):
        self.barra_progreso["value"] = j  # Actualiza el valor de la barra de progreso
        self.etiqueta_estado.config(text=f"Cargando... {j}%")
        self.frame1.update_idletasks()  # Actualiza la ventana para mostrar el progreso

    def goToFrame2(self):
        print("entro")
        self.frame1.destroy()
        frame2 = Login(self.root)
        frame2.loginFrame()

    def goToFrame3(self):
        print("captura")
        frame3 = ContenedorScreen(self.root)
        frame3.contenedorFrame()

    def msg_NoInternet(self):
        icono = tk.PhotoImage(file="src/res/drawable/noInternet.png")
        messagebox.showwarning("Sin Conexión", "¡No te preocupes!😎 \n\n ¡Ingresa los rescates y se enviarán cuando tengas conexión!📶🌎🔃")

