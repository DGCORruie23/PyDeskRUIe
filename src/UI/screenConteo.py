import tkinter as tk
from tkinter import ttk
from src.res.Dimens import tLetra, cLetra, mLetra
from src.res.Colors import verde, rojo
from src.db.dao.RegistroConteoRDao import insert as insertCR
from src.db.dao.PaisDao import getAll as getAllPais
from src.db.models import DatosConteoR
from ttkwidgets.autocomplete import AutocompleteCombobox

class ConteoScreen:
    def __init__(self, root_root, root, opc_paises):
        self.w = 500
        self.h = 700
        x = int((root.winfo_screenwidth() - self.w) * 0.5)
        y = int((root.winfo_screenheight() - self.h) * 0.5)
        root.geometry(f"{self.w}x{self.h}+{x}+{y}")
        root.title("Ventana captura")
        self.root = root
        self.opc_paises = opc_paises
        self.root_padre = root_root

    def registroFrame(self):
        self.registro_frame = tk.Frame(self.root, width=self.w, height=self.h, bg=verde)
        self.registro_frame.pack(fill=tk.BOTH, padx=10)
        self.registro_frame.pack_propagate(False)

        # imageA = Image.open('src/res/drawable/account_circle.png')
        # width_i, height_i = imageA.size
        # imageA = imageA.resize((width_i // 2, height_i // 2))
        # accon = ImageTk.PhotoImage(imageA)
        # logo_accon = tk.Label(self.registro_frame, image=accon, background=verde)
        # logo_accon.image = accon
        # logo_accon.pack()

        # Variable para almacenar la nacionalidad seleccionada
        self.opcion_nacionalidad = tk.StringVar()

        # Crear el Combobox en el diálogo
        combo_box = AutocompleteCombobox(
            self.registro_frame, width=25,
            font=tLetra,
            textvariable=self.opcion_nacionalidad,
            completevalues=self.opc_paises,
            # state="readonly",
        )
        combo_box.pack(padx=20, pady=(40,20))

        # combo_box.set("Ingresa Nacionalidad")

        self.nombre_var = tk.StringVar()
        self.apellidos_var = tk.StringVar()

        self.ASH_var = tk.StringVar()
        self.ASMNE_var = tk.StringVar()
        self.ASME_var = tk.StringVar()
        self.MSH_var = tk.StringVar()
        self.MSMNE_var = tk.StringVar()
        self.MSME_var = tk.StringVar()

        self.nf_var = tk.StringVar()

        self.AAH_var = tk.StringVar()
        self.AAMNE_var = tk.StringVar()
        self.AAME_var = tk.StringVar()
        self.MAH_var = tk.StringVar()
        self.MAMNE_var = tk.StringVar()
        self.MAME_var = tk.StringVar()

        s = ttk.Style()
        s.configure('new.TFrame', background=verde)

        # Crear etiquetas y campos de entrada
        label_adultosN = tk.Label(self.registro_frame, text="Adultos No acompañados:", font=tLetra)
        label_adultosN.pack(pady=(0, 5))

        frame_AS = ttk.Frame(self.registro_frame, style='new.TFrame')
        frame_AS.pack(padx=10, pady=(0,10))

        frame_MS = ttk.Frame(frame_AS, style='new.TFrame')
        frame_MS.pack(side="left", padx=10, pady=10)
        label_MS = tk.Label(frame_MS, text="Hombres", font=cLetra)
        label_MS.pack(side=tk.TOP , pady=(0, 10))
        entry_MS = tk.Entry(frame_MS, textvariable=self.ASH_var, width=7, font=tLetra, justify="center")
        entry_MS.pack(side=tk.TOP, padx=10)

        frame_FNES = ttk.Frame(frame_AS, style='new.TFrame')
        frame_FNES.pack(side="left", padx=10, pady=10)
        label_FNES = tk.Label(frame_FNES, text="Mujeres No Embarazadas", font=mLetra)
        label_FNES.pack(side=tk.TOP, pady=(0, 10))
        entry_FNES = tk.Entry(frame_FNES, textvariable=self.ASMNE_var, width=7, font=tLetra, justify="center")
        entry_FNES.pack(side=tk.TOP, padx=10)

        frame_FES = ttk.Frame(frame_AS, style='new.TFrame')
        frame_FES.pack(side="left", padx=10, pady=10)
        label_FES = tk.Label(frame_FES, text="Mujeres Embarazadas", font=cLetra)
        label_FES.pack(side=tk.TOP, pady=(0, 10))
        entry_FES = tk.Entry(frame_FES, textvariable=self.ASME_var, width=7, font=tLetra, justify="center")
        entry_FES.pack(side=tk.TOP, padx=10)


        label_NNAs = tk.Label(self.registro_frame, text="Menores No Acompañados:", font=tLetra)
        label_NNAs.pack(pady=(0, 10))
        frame_NNAS = ttk.Frame(self.registro_frame, style='new.TFrame')
        frame_NNAS.pack(padx=10, pady=(0, 0))

        frame_MMS = ttk.Frame(frame_NNAS, style='new.TFrame')
        frame_MMS.pack(side="left", padx=10, pady=10)
        label_MMS = tk.Label(frame_MMS, text="Hombres", font=cLetra)
        label_MMS.pack(side=tk.TOP, pady=(0, 10))
        entry_MMS = tk.Entry(frame_MMS, textvariable=self.MSH_var, width=7, font=tLetra, justify="center")
        entry_MMS.pack(side=tk.TOP, padx=10)

        frame_FMNES = ttk.Frame(frame_NNAS, style='new.TFrame')
        frame_FMNES.pack(side="left", padx=10, pady=10)
        label_FMNES = tk.Label(frame_FMNES, text="Mujeres No Embarazadas", font=mLetra)
        label_FMNES.pack(side=tk.TOP, pady=(0, 10))
        entry_FMNES = tk.Entry(frame_FMNES, textvariable=self.MSMNE_var, width=7, font=tLetra, justify="center")
        entry_FMNES.pack(side=tk.TOP, padx=10)

        frame_FES = ttk.Frame(frame_NNAS, style='new.TFrame')
        frame_FES.pack(side="left", padx=10, pady=10)
        label_FES = tk.Label(frame_FES, text="Mujeres Embarazadas", font=cLetra)
        label_FES.pack(side=tk.TOP, pady=(0, 10))
        entry_FES = tk.Entry(frame_FES, textvariable=self.MSME_var, width=7, font=tLetra, justify="center")
        entry_FES.pack(side=tk.TOP, padx=10)

        frame_NF = ttk.Frame(self.registro_frame, style='new.TFrame')
        frame_NF.pack(padx=10, pady=(5, 5))
        label_NF = tk.Label(frame_NF, text="Nucleos Familiares", font=tLetra)
        label_NF.pack(side=tk.TOP, pady=5)
        entry_NF = tk.Entry(frame_NF, textvariable=self.nf_var, width=5, font=tLetra)
        entry_NF.pack(side=tk.TOP, pady=5)

        label_adultosA = tk.Label(self.registro_frame, text="Adultos Acompañados:", font=tLetra)
        label_adultosA.pack(pady=(0, 5))

        frame_AA = ttk.Frame(self.registro_frame, style='new.TFrame')
        frame_AA.pack(padx=10, pady=(0, 10))

        frame_MA = ttk.Frame(frame_AA, style='new.TFrame')
        frame_MA.pack(side="left", padx=10, pady=10)
        label_MA = tk.Label(frame_MA, text="Hombres", font=cLetra)
        label_MA.pack(side=tk.TOP, pady=(0, 10))
        entry_MA = tk.Entry(frame_MA, textvariable=self.AAH_var, width=7, font=tLetra, justify="center")
        entry_MA.pack(side=tk.TOP, padx=10)

        frame_FNEA = ttk.Frame(frame_AA, style='new.TFrame')
        frame_FNEA.pack(side="left", padx=10, pady=10)
        label_FNEA = tk.Label(frame_FNEA, text="Mujeres No Embarazadas", font=mLetra)
        label_FNEA.pack(side=tk.TOP, pady=(0, 10))
        entry_FNEA = tk.Entry(frame_FNEA, textvariable=self.AAMNE_var, width=7, font=tLetra, justify="center")
        entry_FNEA.pack(side=tk.TOP, padx=10)

        frame_FEA = ttk.Frame(frame_AA, style='new.TFrame')
        frame_FEA.pack(side="left", padx=10, pady=10)
        label_FEA = tk.Label(frame_FEA, text="Mujeres Embarazadas", font=cLetra)
        label_FEA.pack(side=tk.TOP, pady=(0, 10))
        entry_FEA = tk.Entry(frame_FEA, textvariable=self.AAME_var, width=7, font=tLetra, justify="center")
        entry_FEA.pack(side=tk.TOP, padx=10)

        label_NAs = tk.Label(self.registro_frame, text="Menores Acompañados:", font=tLetra)
        label_NAs.pack(pady=(0, 10))
        frame_NA = ttk.Frame(self.registro_frame, style='new.TFrame')
        frame_NA.pack(padx=10, pady=(0, 10))

        frame_MMA = ttk.Frame(frame_NA, style='new.TFrame')
        frame_MMA.pack(side="left", padx=10, pady=10)
        label_MMA = tk.Label(frame_MMA, text="Hombres", font=cLetra)
        label_MMA.pack(side=tk.TOP, pady=(0, 10))
        entry_MMA = tk.Entry(frame_MMA, textvariable=self.MAH_var, width=7, font=tLetra, justify="center")
        entry_MMA.pack(side=tk.TOP, padx=10)

        frame_FMNEA = ttk.Frame(frame_NA, style='new.TFrame')
        frame_FMNEA.pack(side="left", padx=10, pady=10)
        label_FMNEA = tk.Label(frame_FMNEA, text="Mujeres No Embarazadas", font=mLetra)
        label_FMNEA.pack(side=tk.TOP, pady=(0, 10))
        entry_FMNEA = tk.Entry(frame_FMNEA, textvariable=self.MAMNE_var, width=7, font=tLetra, justify="center")
        entry_FMNEA.pack(side=tk.TOP, padx=10)

        frame_FEA = ttk.Frame(frame_NA, style='new.TFrame')
        frame_FEA.pack(side="left", padx=10, pady=10)
        label_FEA = tk.Label(frame_FEA, text="Mujeres Embarazadas", font=cLetra)
        label_FEA.pack(side=tk.TOP, pady=(0, 10))
        entry_FEA = tk.Entry(frame_FEA, textvariable=self.MAME_var, width=7, font=tLetra, justify="center")
        entry_FEA.pack(side=tk.TOP, padx=10)

        botonG = tk.Button(self.registro_frame, text="Guardar", bg=rojo, fg="white", font=("Arial", 14), command=self.guardar)
        botonG.pack(pady=(20, 10))

        self.root.protocol('WM_DELETE_WINDOW', self.cerrarVentana)

    def guardar(self):
        paises = getAllPais()
        nacionalidadN = ""
        iso3N = ""
        AS_H = 0
        AS_MNE = 0
        AS_ME = 0

        NNA_H = 0
        NNA_MNE = 0
        NNA_ME = 0

        NuFam = 0
        AA_H = 0
        AA_MNE = 0
        AA_ME = 0

        NA_H = 0
        NA_MNE = 0
        NA_ME = 0

        nacionalidadN = self.opcion_nacionalidad.get()
        for pais in paises:
            # print(pais.nombre_pais, nacionalidadN)
            if pais.nombre_pais == nacionalidadN:
                iso3N = pais.iso3

        AS_H = 0 if self.ASH_var.get() == "" else int(self.ASH_var.get())
        AS_MNE = 0 if self.ASMNE_var.get() == "" else int(self.ASMNE_var.get())
        AS_ME = 0 if self.ASME_var.get() == "" else int(self.ASME_var.get())

        NNA_H = 0 if self.MSH_var.get() == "" else int(self.MSH_var.get())
        NNA_MNE = 0 if self.MSMNE_var.get() == "" else int(self.MSMNE_var.get())
        NNA_ME = 0 if self.MSME_var.get() == "" else int(self.MSME_var.get())

        NuFam = 0 if self.nf_var.get() == "" else int(self.nf_var.get())
        AA_H = 0 if self.AAH_var.get() == "" else int(self.AAH_var.get())
        AA_MNE = 0 if self.AAMNE_var.get() == "" else int(self.AAMNE_var.get())
        AA_ME = 0 if self.AAME_var.get() == "" else int(self.AAME_var.get())

        NA_H = 0 if self.MAH_var.get() == "" else int(self.MAH_var.get())
        NA_MNE = 0 if self.MAMNE_var.get() == "" else int(self.MAMNE_var.get())
        NA_ME = 0 if self.MAME_var.get() == "" else int(self.MAME_var.get())

        # apellidosN = self.apellidos_var.get()
        # fechaNacimiento = f"{self.dia_var.get()}-{self.mes_var.get()}-{self.anio_var.get()}"
        # sexoN = self.generoM_var.get()
        #
        # fecha_nacimientoA = datetime.strptime(fechaNacimiento, "%d-%m-%Y")
        # ahora = date.today()
        # edadA = ahora.year - fecha_nacimientoA.year - (
        #             (ahora.month, ahora.day) < (fecha_nacimientoA.month, fecha_nacimientoA.day))
        #
        # adultoN = False if edadA < 18 else True


        registros = []
        registros.append(DatosConteoR(
            nacionalidad= nacionalidadN,
            iso3 = iso3N,
            AS_hombres = AS_H,
            AS_mujeresNoEmb = AS_MNE,
            AS_mujeresEmb = AS_ME,
            NNAsS_hombres = NNA_H,
            NNAsS_mujeresNoEmb = NNA_MNE,
            NNAsS_mujeresEmb = NNA_ME,
            Nucleos_Familiares = NuFam,
            AA_hombres = AA_H,
            AA_mujeresNoEmb = AA_MNE,
            AA_mujeresEmb = AA_ME,
            NNAsA_hombres = NA_H,
            NNAsA_mujeresNoEmb = NA_MNE,
            NNAsA_mujeresEmb = NA_ME,
        ))
        insertCR(registros)

        self.root.destroy()
        self.root_padre.update()
        self.root_padre.deiconify()

        # wn = contenedor.ContenedorScreen(self.root_padre)
        # wn.contenedorFrame()
        #
        # self.root.destroy()
        # # self.root.withdraw()
        # self.root_padre.deiconify()
        # self.root_padre.update()

    def cerrarVentana(self):
        self.root.destroy()
        self.root_padre.update()
        self.root_padre.deiconify()
        # wn = contenedor.RecyConteo(self.root_padre, self.root, self.opc_paises)
        # wn.RConteoFrame()




