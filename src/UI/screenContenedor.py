import tkinter as tk
from src.res.Colors import marron, rojo, black, white, verde
import src.res.Strings as Texts
from src.UC.usercases import getDataUC
from src.UI.screenCaptura import CapturaScreen
from src.UI.screenResumen import ResumenScreen
from src.UI.recyclerConteo import RecyConteo

class ContenedorScreen:
    def __init__(self, root):
        root.overrideredirect(False)
        w = 1366
        h = 768
        x = int((root.winfo_screenwidth() - w) * 0.5)
        y = int((root.winfo_screenheight() - h - 100) * 0.5)
        root.geometry(f"{w}x{h}+{x}+{y}")
        # root.geometry("1366x768+0+0")
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.title("ventana de captura")
        self.root = root

    def contenedorFrame(self):
        self.frame3 = tk.Frame(self.root, width=1366, height=768, bg=marron)
        self.frame3.grid(row=0, column=0)

        self.root.update()
        self.frame3.tkraise()
        self.frame3.pack_propagate(False)
        self.frame3.rowconfigure(0, weight=1)
        self.frame3.columnconfigure(0, weight=1)

        oficinaR, userInfo, fuerzaInfo, paises, municipios, puntosInt = getDataUC()
        self.opc_paises = []
        for item in paises:
            self.opc_paises.append(item.nombre_pais)

        self.tool_bar = tk.Frame(self.frame3, width=1300, height=100, bg=rojo)
        self.tool_bar.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.tool_bar.pack_propagate(False)

        btn_conteo = tk.Button(
            self.tool_bar,
            text="conteo\nrapido", font=("Arial", 12),
            bg=verde, fg=white,
            activebackground=marron, activeforeground=black,
            command=self.enviarConteo
        )
        btn_conteo.pack(side=tk.RIGHT, padx=(0,10))

        tk.Label(
            self.tool_bar,
            text=Texts.captura_Lres,
            bg=rojo,
            fg=marron,
            font=("Arial", 20)
        ).pack(side=tk.TOP, fill=tk.BOTH, pady=(0, 0))

        tk.Label(
            self.tool_bar,
            text= Texts.captura_Lor + oficinaR,
            bg=rojo,
            fg=marron,
            font=("Arial", 18)
        ).pack(side=tk.TOP, fill=tk.BOTH, pady=(0, 0))

        tk.Label(
            self.tool_bar,
            text=f"Agente {userInfo.nombre} {userInfo.apellido}",
            bg=rojo,
            fg=marron,
            font=("Arial", 15)
        ).pack(side=tk.TOP, fill=tk.BOTH, pady=(0, 0))

        self.area_trabajo = tk.Frame(self.frame3, width=900, height=700, bg=marron)
        self.area_trabajo.pack()
        self.area_trabajo.pack_propagate(False)

        frame_mensaje = ResumenScreen(self.area_trabajo)
        frame_mensaje.resumenFrame()

        frame_captura = CapturaScreen(self.root, self.area_trabajo, puntosInt, fuerzaInfo, municipios, self.opc_paises)
        frame_captura.capturaFrame()
        #
        # frame_registro = RegistroScreen(self.frame3, self.opc_paises)
        # frame_registro.registroFrame()
        # for widget in frame_registro.registro_frame.winfo_children():
        #     widget.destroy()

    def enviarConteo(self):
        print("enviar a conteo")
        self.root.withdraw()
        rv = tk.Toplevel(self.root)
        self.vm = RecyConteo(self.root, rv, self.opc_paises)
        self.vm.RConteoFrame()





