import tkinter as tk
from tkinter import ttk
from src.res.Dimens import tLetra
from PIL import Image, ImageTk
from src.res.Colors import verde, rojo
from src.db.dao.RegistroNombresDao import update as updateN
from src.db.dao.PaisDao import getAll as getAllPais
from src.UC.usercases import getPaisesUC
from datetime import datetime, date
from ttkwidgets.autocomplete import AutocompleteCombobox

class EdicionNac:
    def __init__(self, root_padre, root, registro):
        w = 430
        h = 650
        x = int((root.winfo_screenwidth() - w) * 0.5)
        y = int((root.winfo_screenheight() - h) * 0.5)
        root.geometry(f"{w}x{h}+{x}+{y}")
        root.title("Ventana edición")

        self.root = root
        self.root_padre = root_padre
        self.registro = registro

        opc_paises = []
        for pais in getPaisesUC():
            opc_paises.append(pais.nombre_pais)
        self.opc_paises = opc_paises

    def edicNacFrame(self):
        self.registro_frame = tk.Frame(self.root, width=430, height=650, bg=verde)
        self.registro_frame.pack()
        self.registro_frame.pack_propagate(False)

        imageA = Image.open('src/res/drawable/account_circle.png')
        width_i, height_i = imageA.size
        imageA = imageA.resize((width_i // 2, height_i // 2))
        accon = ImageTk.PhotoImage(imageA)
        logo_accon = tk.Label(self.registro_frame, image=accon, background=verde)
        logo_accon.image = accon
        logo_accon.pack()



        # Variable para almacenar la nacionalidad seleccionada
        self.opcion_nacionalidad = tk.StringVar()

        self.opcion_nacionalidad.set(self.registro.nacionalidad)

        # Crear el Combobox en el diálogo
        combo_box = AutocompleteCombobox(
            self.registro_frame, width=30,
            font=tLetra,
            textvariable=self.opcion_nacionalidad,
            completevalues=self.opc_paises,
            # state="readonly",
        )
        combo_box.pack(padx=20, pady=10)

        self.nombre_var = tk.StringVar()
        self.apellidos_var = tk.StringVar()
        self.dia_var = tk.StringVar()
        self.mes_var = tk.StringVar()
        self.anio_var = tk.StringVar()
        self.generoM_var = tk.BooleanVar()
        self.generoF_var = tk.BooleanVar()

        fe_na = datetime.strptime(self.registro.fechaNacimiento, "%d-%m-%Y")

        self.nombre_var.set(self.registro.nombre)
        self.apellidos_var.set(self.registro.apellidos)
        self.dia_var.set(str(fe_na.day))
        self.mes_var.set(str(fe_na.month))
        self.anio_var.set(str(fe_na.year))

        if(self.registro.sexo):
            self.generoM_var.set(1)
        else:
            self.generoF_var.set(1)

        # Crear etiquetas y campos de entrada
        label_nombre = tk.Label(self.registro_frame, text="Nombre:", font=tLetra)
        label_nombre.pack(pady=(0, 10))
        entry_nombre = tk.Entry(self.registro_frame, textvariable=self.nombre_var, font=tLetra)
        entry_nombre.pack(pady=(0, 20))

        label_apellidos = tk.Label(self.registro_frame, text="Apellidos:", font=tLetra)
        label_apellidos.pack(pady=(0, 10))
        entry_apellidos = tk.Entry(self.registro_frame, textvariable=self.apellidos_var, font=tLetra)
        entry_apellidos.pack(pady=(0, 20))

        label_fecha = tk.Label(self.registro_frame, text="Fecha de Nacimiento:", font=tLetra)
        label_fecha.pack(side=tk.TOP, padx=5)

        s = ttk.Style()
        s.configure('new.TFrame', background=verde)

        frame_fecha = ttk.Frame(self.registro_frame, style='new.TFrame')
        frame_fecha.pack(padx=10, pady=10)
        entry_dia = tk.Entry(frame_fecha, textvariable=self.dia_var, width=5, font=tLetra)
        entry_dia.pack(side="left", padx=10)
        entry_mes = tk.Entry(frame_fecha, textvariable=self.mes_var, width=6, font=tLetra)
        entry_mes.pack(side="left", padx=10)
        entry_anio = tk.Entry(frame_fecha, textvariable=self.anio_var, width=7, font=tLetra)
        entry_anio.pack(side="left", padx=10)

        frame_genero = ttk.Frame(self.registro_frame)
        frame_genero.pack(padx=10, pady=5)
        check_generoM = tk.Checkbutton(frame_genero, text="Hombre", variable=self.generoM_var, command=self.verificarCheckM,
                                       font=tLetra)
        check_generoM.pack(side="right", padx=5)
        check_generoF = tk.Checkbutton(frame_genero, text="Mujer", variable=self.generoF_var, command=self.verificarCheckF,
                                       font=tLetra)
        check_generoF.pack(side="right", padx=5)

        botonG = tk.Button(
            self.registro_frame,
            text="Guardar", font=("Arial", 14),
            bg=rojo, fg="white",
            command=self.actualizar
        )
        botonG.pack(pady=(50, 10))

        self.root.protocol('WM_DELETE_WINDOW', self.cerrarVentana)


    def verificarCheckM(self):
        estado_M = self.generoM_var.get()

        if estado_M:
            self.generoF_var.set(0)
        else:
            self.generoF_var.set(1)

    def verificarCheckF(self):
        estado_F = self.generoF_var.get()

        if estado_F:
            self.generoM_var.set(0)
        else:
            self.generoM_var.set(1)

    def actualizar(self):
        paises = getAllPais()
        nacionalidadN = ""
        iso3N = ""
        nombreN = ""
        apellidosN = ""
        noIdentidad = "00"
        fechaNacimiento = ""
        sexoN = True
        embarazoN = False

        nacionalidadN = self.opcion_nacionalidad.get()
        for pais in paises:
            # print(pais.nombre_pais, nacionalidadN)
            if pais.nombre_pais == nacionalidadN:
                iso3N = pais.iso3

        nombreN = self.nombre_var.get()
        apellidosN = self.apellidos_var.get()
        fechaNacimiento = f"{self.dia_var.get()}-{self.mes_var.get()}-{self.anio_var.get()}"
        sexoN = self.generoM_var.get()

        fecha_nacimientoA = datetime.strptime(fechaNacimiento, "%d-%m-%Y")
        ahora = date.today()
        edadA = ahora.year - fecha_nacimientoA.year - (
                (ahora.month, ahora.day) < (fecha_nacimientoA.month, fecha_nacimientoA.day))

        adultoN = False if edadA < 18 else True


        self.registro.nacionalidad = nacionalidadN
        self.registro.iso3 = iso3N
        self.registro.nombre = nombreN
        self.registro.apellidos = apellidosN
        self.registro.fechaNacimiento = fechaNacimiento
        self.registro.adulto = adultoN
        self.registro.sexo = sexoN
        self.registro.embarazo = embarazoN

        # registros = []
        # registros.append(RegistroNombres(
        #     nacionalidad=nacionalidadN, iso3=iso3N,
        #     nombre=nombreN, apellidos=apellidosN,
        #     noIdentidad=noIdentidad,
        #     fechaNacimiento=fechaNacimiento,
        #     sexo=sexoN,
        #     embarazo=embarazoN
        # ))
        updateN(self.registro)

        self.root.destroy()
        # self.root.withdraw()
        self.root_padre.deiconify()
        self.root_padre.update()

    def cerrarVentana(self):
        self.root.destroy()
        self.root_padre.deiconify()




