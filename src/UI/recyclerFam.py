import tkinter as tk
from src.res.Colors import verde, marron, marron_oscuro, rojo, rojo_oscuro, gris_oscuro
from src.UC.usercases import getRegsByNumFam
from tkinter import ttk, messagebox
from datetime import datetime, date
from src.UI.editarFam import EdicionFam
from src.db.dao.RegistroFamiliasDao import deleteById as deleteFid
import src.UI.screenContenedor as contenedor


class RecyFam:
    def __init__(self,root_padre, root, numFam):
        self.rootS = root_padre
        self.root = root
        self.root.update()
        x = int(root.winfo_screenwidth() * 0.25)
        y = int(root.winfo_screenheight() * 0.05)
        self.root.geometry(f"500x700+{x}+{y}")
        self.numFam = numFam

    
    def RFamFrame(self):
        self.frameFam = tk.Frame(self.root, width=500, height=700, bg=verde)
        self.frameFam.pack()

        self.frameFam.tkraise()
        self.frameFam.pack_propagate(False)
        self.root.title("Desglose por Familia")

        # pais_text = getNacbyIso(self.iso)

        etiqueta_familia = tk.Label(self.frameFam, text=f"Familia {self.numFam}", bg=marron, fg=verde, font=("Arial", 24))
        etiqueta_familia.pack(pady=(50, 10))

        # obtener todos los registros por la ISO
        registros = getRegsByNumFam(self.numFam)

        frameF = tk.Frame(self.frameFam)
        frameF.pack()

        # Crear un canvas con una barra de desplazamiento vertical
        self.canvasF = tk.Canvas(frameF)
        scrollbarF = ttk.Scrollbar(frameF, orient="vertical", command=self.canvasF.yview)
        scrollbarF.pack(side=tk.LEFT, fill="y")

        # Configurar el canvas
        self.canvasF.configure(yscrollcommand=scrollbarF.set)
        self.canvasF.pack(side=tk.LEFT)

        # Crear un frame interior para contener los widgets
        frame_interiorF = tk.Frame(self.canvasF)
        self.canvasF.create_window((0, 0), window=frame_interiorF, anchor="nw")

        def onClickE(p):
            editS = tk.Toplevel(self.root)
            self.vm = EdicionFam(self.rootS,self.root, editS, p, numFam=self.numFam)
            self.vm.edicFamFrame()
            return

        def onClickD(p):
            deleteFid(p.idRegistroFam)
            messagebox.showinfo("Alerta","Registro Eliminado")
            self.root.destroy()
            self.rootS.deiconify()
            wn = contenedor.ContenedorScreen(self.rootS)
            wn.contenedorFrame()

        # Agregar contenido al frame interior
        for i, valores in enumerate(registros):
            # print(valores.fechaNacimiento)
            edadT = "NNA"

            edadT = "NNA" if valores.adulto < 18 else "A"
            colorB = rojo if valores.adulto < 18 else verde

            tk.Label(
                frame_interiorF,
                text=f"{edadT}",
                fg="white", bg=colorB,
            ).grid(row=i, column=0)
            tk.Label(
                frame_interiorF,
                text=f"{valores.apellidos} {valores.nombre}"
            ).grid(row=i, column=1)
            tk.Label(
                frame_interiorF,
                text=f"{valores.parentesco}",
                fg=gris_oscuro,
            ).grid(row=i, column=2)
            tk.Button(
                frame_interiorF,
                text="Editar",
                fg="black", activeforeground="white",
                bg=marron, activebackground=marron_oscuro,
                command=lambda i=valores: onClickE(i)
            ).grid(row=i, column=3)
            tk.Button(
                frame_interiorF,
                text="Eliminar",
                fg="white", activeforeground="black",
                bg=rojo, activebackground=rojo_oscuro,
                command=lambda i=valores: onClickD(i)
            ).grid(row=i, column=4)

        # Configurar el desplazamiento al añadir widgets al canvas
        frame_interiorF.bind("<Configure>", self.configurar_scrollN)

        self.root.protocol('WM_DELETE_WINDOW', self.cerrarVentana)

    # def goToFrame1(self):
    #     self.root.destroy()
    #     frame1 = info.SplashScreen(self.root)
    #     frame1.splashFrame()

    def configurar_scrollN(self, event):
        self.canvasF.configure(scrollregion=self.canvasF.bbox("all"), width=400, height=500)

    def cerrarVentana(self):
        self.root.destroy()
        self.rootS.deiconify()
        wn = contenedor.ContenedorScreen(self.rootS)
        wn.contenedorFrame()