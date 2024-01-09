import tkinter as tk
from src.res.Colors import verde, marron, marron_oscuro, rojo, rojo_oscuro
from src.UC.usercases import getRegsByIso, getNacbyIso
from tkinter import ttk, messagebox
from datetime import datetime, date
from src.UI.editarNac import EdicionNac
from src.db.dao.RegistroNombresDao import deleteById as deleteNid
import src.UI.screenContenedor as contenedor

class RecyNac:
    def __init__(self,root_padre, root, iso):
        self.rootS = root_padre
        self.root = root
        self.root.update()
        x = int(root.winfo_screenwidth() * 0.25)
        y = int(root.winfo_screenheight() * 0.05)
        self.root.geometry(f"500x700+{x}+{y}")
        self.iso = iso

    
    def RNacFrame(self):
        self.frameNac = tk.Frame(self.root, width=500, height=700, bg=verde)
        self.frameNac.pack()

        self.frameNac.tkraise()
        self.frameNac.pack_propagate(False)
        self.root.title("Desglose por nacionalidad")

        pais_text = getNacbyIso(self.iso)

        etiqueta_usuario = tk.Label(self.frameNac, text=f"{pais_text.nombre_pais.upper()}", bg=marron, fg=verde, font=("Arial", 24))
        etiqueta_usuario.pack(pady=(50, 10))

        # obtener todos los registros por la ISO
        registros_iso = getRegsByIso(self.iso)

        frameN = tk.Frame(self.frameNac)
        frameN.pack()

        # Crear un canvas con una barra de desplazamiento vertical
        self.canvasN = tk.Canvas(frameN)
        scrollbarN = ttk.Scrollbar(frameN, orient="vertical", command=self.canvasN.yview)
        scrollbarN.pack(side=tk.LEFT, fill="y")

        # Configurar el canvas
        self.canvasN.configure(yscrollcommand=scrollbarN.set)
        self.canvasN.pack(side=tk.LEFT)

        # Crear un frame interior para contener los widgets
        frame_interiorN = tk.Frame(self.canvasN)
        self.canvasN.create_window((0, 0), window=frame_interiorN, anchor="nw")

        def onClickE(p):
            editS = tk.Toplevel(self.root)
            self.vm = EdicionNac(self.rootS, editS, p)
            self.vm.edicNacFrame()
            return

        def onClickD(p):
            # editS = tk.Toplevel(self.root)
            # self.vm = EdicionNac(self.rootS, editS, p)
            # self.vm.edicNacFrame()
            deleteNid(p.idRegistroNom)
            messagebox.showinfo("Alerta","Registro Eliminado")
            return

        # Agregar contenido al frame interior
        for i, valores in enumerate(registros_iso):
            # print(valores.fechaNacimiento)
            edadT = "NNA"

            edadT = "NNA" if valores.adulto < 18 else "A"
            colorB = rojo if valores.adulto < 18 else verde

            tk.Label(
                frame_interiorN,
                text=f"{edadT}",
                fg="white", bg=colorB,
            ).grid(row=i, column=0)
            tk.Label(
                frame_interiorN,
                text=f"{valores.apellidos} {valores.nombre}"
            ).grid(row=i, column=1)
            tk.Button(
                frame_interiorN,
                text="Editar",
                fg="black", activeforeground="white",
                bg=marron, activebackground=marron_oscuro,
                command=lambda i=valores: onClickE(i)
            ).grid(row=i, column=2)
            tk.Button(
                frame_interiorN,
                text="Eliminar",
                fg="white", activeforeground="black",
                bg=rojo, activebackground=rojo_oscuro,
                command=lambda i=valores: onClickD(i)
            ).grid(row=i, column=3)

        # Configurar el desplazamiento al añadir widgets al canvas
        frame_interiorN.bind("<Configure>", self.configurar_scrollN)

        self.root.protocol('WM_DELETE_WINDOW', self.cerrarVentana)

    # def goToFrame1(self):
    #     self.root.destroy()
    #     frame1 = info.SplashScreen(self.root)
    #     frame1.splashFrame()

    def configurar_scrollN(self, event):
        self.canvasN.configure(scrollregion=self.canvasN.bbox("all"), width=400, height=500)

    def cerrarVentana(self):
        self.root.destroy()
        self.rootS.deiconify()
        wn = contenedor.ContenedorScreen(self.rootS)
        wn.contenedorFrame()