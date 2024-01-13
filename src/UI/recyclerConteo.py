import tkinter as tk
from src.res.Colors import verde, marron, marron_oscuro, rojo, rojo_oscuro, white, black
from tkinter import ttk, messagebox
from src.UI.screenConteo import ConteoScreen
from src.UI.editarConteo import EdicionConteo
from src.db.dao.RegistroConteoRDao import getAll as getAllConteoR, deleteAll, deleteById as deleteCid
import src.UI.screenContenedor as contenedor
from src.UC.usercases import sendConteo
from src.db.models import DatosConteoRComp

class RecyConteo:
    def __init__(self,root_padre, root, opc_paises):
        self.rootS = root_padre
        self.root = root
        self.root.update()
        self.w = 400
        self.h = 500
        self.opc_paises = opc_paises
        x = int((root.winfo_screenwidth() - self.w) * 0.5)
        y = int((root.winfo_screenheight() - self.h - 100) * 0.5)
        self.root.geometry(f"{self.w}x{self.h}+{x}+{y}")

    
    def RConteoFrame(self):
        self.frameConteo = tk.Frame(self.root, width=self.w, height=self.h, bg=verde)
        self.frameConteo.pack()

        self.frameConteo.tkraise()
        self.frameConteo.pack_propagate(False)
        self.root.title("CONTEO RAPIDO Desglose por nacionalidad")

        datos_conteoR = getAllConteoR()

        etiqueta_conteo = tk.Label(
            self.frameConteo, text=f"Desglose por nacionalidad",
            bg=marron, fg=verde,
            font=("Arial", 24)
        )
        etiqueta_conteo.pack(pady=(50, 40))

        frameN = tk.Frame(self.frameConteo)
        frameN.pack()

        btn_enviar = tk.Button(
            self.frameConteo,
            text="ENVIAR", font=("Arial", 14),
            bg=rojo, fg=white,
            activebackground=rojo_oscuro, activeforeground=black,
            command=self.enviarConteo
        )
        btn_enviar.pack(side=tk.RIGHT, padx=(0, 60))

        btn_AddConteo = tk.Button(
            self.frameConteo,
            text="+ Nacionalidad", font=("Arial", 14),
            bg=marron_oscuro, fg=white,
            activebackground=marron, activeforeground=black,
            command=self.agregarConteo
        )
        btn_AddConteo.pack(side=tk.LEFT, padx=(60, 10), pady=(0,0))

        # Crear un canvas con una barra de desplazamiento vertical
        self.canvasN = tk.Canvas(frameN)
        scrollbarN = ttk.Scrollbar(frameN, orient="vertical", command=self.canvasN.yview)
        scrollbarN.pack(side=tk.LEFT, fill="y")

        # Configurar el canvas
        self.canvasN.configure(yscrollcommand=scrollbarN.set)
        self.canvasN.pack(side=tk.LEFT, padx=10)

        # Crear un frame interior para contener los widgets
        frame_interiorN = tk.Frame(self.canvasN)
        self.canvasN.create_window((0, 0), window=frame_interiorN, anchor="nw")

        def onClickE(p):
            editS = tk.Toplevel(self.root)
            self.vm = EdicionConteo(self.root, editS, self.opc_paises, p)
            self.vm.edicConteoFrame()
            return

        def onClickD(p):
            deleteCid(p.idRegistro)
            messagebox.showinfo("Alerta","Registro Eliminado")
            return

        # Agregar contenido al frame interior
        for i, valores in enumerate(datos_conteoR):
            # print(valores.fechaNacimiento)

            ConteoTotal = ( valores.AS_hombres +
                            valores.AS_mujeresNoEmb +
                            valores.AS_mujeresEmb +
                            valores.NNAsS_hombres +
                            valores.NNAsS_mujeresNoEmb +
                            valores.NNAsS_mujeresEmb +

                            valores.AA_hombres +
                            valores.AA_mujeresNoEmb +
                            valores.AA_mujeresEmb +
                            valores.NNAsA_hombres +
                            valores.NNAsA_mujeresNoEmb +
                            valores.NNAsA_mujeresEmb
                            )

            tk.Label(
                frame_interiorN,
                text=f"{valores.iso3} {ConteoTotal}"
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
        self.canvasN.configure(scrollregion=self.canvasN.bbox("all"), width=300, height=250)

    def cerrarVentana(self):
        self.root.destroy()
        self.rootS.deiconify()
        wn = contenedor.ContenedorScreen(self.rootS)
        wn.contenedorFrame()

    def agregarConteo(self):
        self.root.withdraw()
        ventana_secundaria = tk.Toplevel(self.root)
        self.ventanaSecundaria = ConteoScreen(self.root, ventana_secundaria, self.opc_paises)
        self.ventanaSecundaria.registroFrame()


    def enviarConteo(self):
        sendConteo()