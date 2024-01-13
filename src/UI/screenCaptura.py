import tkinter as tk
from tkinter import ttk, messagebox
import src.res.Strings as Texts
from datetime import datetime
from src.UI.screenRegistro import RegistroScreen
from src.UI.screenRegistroF import RegistroScreenF
from src.UI.recyclerNac import RecyNac
from src.UI.recyclerFam import RecyFam
from src.db.models import PuntosInfo, RescateComp
from src.db.dao.PuntosInfoDao import update as updatePunto
from src.UC.usercases import getIsos, getTotalFamilias, getNumFamilias, getCachePunto, sendRescates, getDataUC
from src.res.Colors import marron, marron_oscuro, black, white, verde, verde_oscuro, rojo, rojo_oscuro
from ttkwidgets.autocomplete import AutocompleteCombobox

class CapturaScreen:
    def __init__(self, root_root , root, puntosInt, fuerzaInfo, municipios, opc_paises):
        self.root = root
        self.new = root_root
        self.puntosInt = puntosInt
        self.fuerzaInfo = fuerzaInfo
        self.municipios = municipios
        self.opc_paises = opc_paises
        self.cachePunto = getCachePunto()


    def capturaFrame(self):
        self.captura_frame = tk.Frame(self.root, width=430, height=650, bg="white")
        self.captura_frame.pack(side=tk.RIGHT)
        self.captura_frame.pack_propagate(False)

        now = datetime.now()

        fechaL = tk.Label(
            self.captura_frame,
            text=f"Fecha: {now.strftime('%d-%m-%Y')}",
            bg="white", fg="black",
            font=("Arial", 15)
        )
        fechaL.pack(side=tk.TOP, fill=tk.BOTH, pady=(20, 10))

        self.horaL = tk.Label(
            self.captura_frame,
            text=f"Hora: {now.strftime('%H:%M')}",
            bg="white",
            fg="black",
            font=("Arial", 15)
        )
        self.horaL.pack(side=tk.TOP, fill=tk.BOTH, pady=(0, 0))

        tipo_rescateL = tk.Label(
            self.captura_frame,
            text=f"Tipo de Rescate",
            bg="white",
            fg="black",
            font=("Arial", 12)
        )
        tipo_rescateL.pack(side=tk.TOP, fill=tk.BOTH, pady=(20, 0))

        # Variable para almacenar la opción seleccionada
        self.opc_sel = tk.StringVar()
        # self.opc_sel.set(self.cachePunto.tipo_punto)

        # Crear la lista desplegable
        self.cb_Tipo = ttk.Combobox(
            self.captura_frame, width=30, height=10,
            font=("Arial", 12),
            textvariable=self.opc_sel,
            values=Texts.types_Puntos,
            state="readonly"
        )
        self.cb_Tipo.pack(pady=10)

        # cb_Tipo.set("Tipo de Punto")
        self.cb_Tipo.set(self.cachePunto.tipo_punto)

        self.cb_Tipo.bind("<<ComboboxSelected>>", self.poner_puntos)
        self.cb_Tipo.bind("<Return>", self.poner_puntos)

        self.tipo_rescateNombreL = tk.Label(
            self.captura_frame,
            text=f"Nombre del punto",
            bg="white",
            fg="black",
            font=("Arial", 12)
        )
        self.tipo_rescateNombreL.pack(side=tk.TOP, fill=tk.BOTH, pady=(10, 0))

        # Variable para almacenar la opción seleccionada
        self.opc_sel_nombre = tk.StringVar()
        self.opc_sel_nombre.set(self.cachePunto.nombre_punto)

        opciones_sel_nombre = [""]

        # Crear la lista desplegable
        self.cb_Tipo_nombre = AutocompleteCombobox(
            self.captura_frame, width=40,
            font=("Arial", 12),
            completevalues=opciones_sel_nombre,
            textvariable=self.opc_sel_nombre,
            # state="readonly"
        )
        self.cb_Tipo_nombre.pack(pady=10)

        # self.cb_Tipo_nombre.set("Nombre del Punto")
        self.cb_Tipo_nombre.set(self.cachePunto.nombre_punto)

        self.cb_Tipo_nombre.bind("<<ComboboxSelected>>", self.guardar_puntos)
        self.cb_Tipo_nombre.bind("<Return>", self.guardar_puntos)

        frameRecyclers = tk.Frame(self.captura_frame, width=410, height=300)
        frameRecyclers.pack(pady=10)
        frameRecyclers.pack_propagate(False)

        # ---------------------------------
        #########------------ diseño RV de Familias ----------------
        # ---------------------------------
        registros_fam = getNumFamilias()

        frameF = tk.Frame(frameRecyclers, width=200, height=200)
        frameF.pack(side=tk.RIGHT, fill=tk.BOTH)
        frameF.pack_propagate(False)

        botonF = tk.Button(
            frameF,
            text="+ Familia", font=("Arial", 12),
            bg=verde, fg=white,
            activebackground=verde_oscuro, activeforeground=white,
            command=self.mostrar_popupF
        )
        botonF.pack(pady=10)

        # Crear un canvas con una barra de desplazamiento vertical
        self.canvasF = tk.Canvas(frameF)
        scrollbarF = ttk.Scrollbar(frameF, orient="vertical", command=self.canvasF.yview)
        scrollbarF.pack(side=tk.RIGHT, fill="y")

        # Configurar el canvas
        self.canvasF.configure(yscrollcommand=scrollbarF.set)
        self.canvasF.pack(side=tk.LEFT)

        # Crear un frame interior para contener los widgets
        frame_interiorF = tk.Frame(self.canvasF)
        self.canvasF.create_window((0, 0), window=frame_interiorF, anchor="nw")

        def onClickF(p):
            self.new.withdraw()
            rvf = tk.Toplevel(self.root)
            self.vmf = RecyFam(self.new, rvf, p)
            self.vmf.RFamFrame()

        for i, valores in enumerate(registros_fam):
            tk.Label(frame_interiorF, text=f"Familia {valores.numFamilia}: ").grid(row=i, column=0)
            tk.Label(frame_interiorF, text=f"{valores.conteo}").grid(row=i, column=1)
            tk.Button(frame_interiorF,text="ver",command=lambda x=valores.numFamilia: onClickF(x)).grid(row=i, column=2)

        frame_interiorF.bind("<Configure>", self.configurar_scrollF)

        btn_enviar = tk.Button(
            self.captura_frame,
            text="Enviar", font=("Arial", 12),
            bg=rojo, fg=white,
            activebackground=rojo, activeforeground=black,
            command=self.popUpEnviar
        )
        btn_enviar.pack(pady=(10, 0), padx=(0, 20), side=tk.RIGHT)

        # ---------------------------------
        #########------------ diseño RV de nacionalidad ----------------
        # ---------------------------------

        registros_iso = getIsos()

        frameN = tk.Frame(frameRecyclers, width=200, height=200)
        frameN.pack(side=tk.RIGHT, fill=tk.BOTH)
        frameN.pack_propagate(False)

        botonN = tk.Button(
            frameN,
            text="+ Nacionalidad", font=("Arial", 12),
            bg=marron_oscuro, fg=white,
            activebackground=marron, activeforeground=black,
            command=self.popUpInsert
        )
        botonN.pack(pady=10)

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

        def onClick(p):
            # self.new.withdraw()
            self.new.withdraw()
            rv = tk.Toplevel(self.root)
            self.vm = RecyNac(self.new, rv, p)
            self.vm.RNacFrame()

        # Agregar contenido al frame interior
        for i , valores in enumerate(registros_iso):
            tk.Label(frame_interiorN, text=f"{i + 1}.-{valores.iso3}").grid(row=i, column=0)
            tk.Label(frame_interiorN, text=f"{valores.conteo}").grid(row=i, column=1)
            tk.Button(frame_interiorN,text="ver", command=lambda x=valores.iso3: onClick(x)).grid(row=i, column=2)

        # Configurar el desplazamiento al añadir widgets al canvas
        frame_interiorN.bind("<Configure>", self.configurar_scrollN)

        # botonF = tk.Button(captura_frame, text="+ Familia", command=mostrar_popupF)
        # botonF.pack(pady=10)
        # tool_bar = tk.Frame(frame3, width=1300, height=100, bg=marron)
        # tool_bar.grid(row=0, column=0)

    def poner_puntos(self, event):
        opcion_seleccionada = self.opc_sel.get()
        lista_nombres = []
        self.opc_sel_nombre = ""
        self.cb_Tipo_nombre.set("")
        if opcion_seleccionada == "Aeropuerto":  # ----------------------------
            self.tipo_rescateNombreL.config(text="Nombre del punto")
            for item in self.puntosInt:
                if item.tipoPunto == "AEREOS":
                    lista_nombres.append(item.nombrePunto)
        elif opcion_seleccionada == "Carretero":  # ---------------------------
            self.tipo_rescateNombreL.config(text="Nombre del punto")
            for item in self.fuerzaInfo:
                if item.tipoP == "Carretero":
                    lista_nombres.append(item.nomPuntoRevision)
        elif opcion_seleccionada == "Casa de Seguridad": # ---------------------------
            self.tipo_rescateNombreL.config(text="Nombre del Municipio")
            for item in self.municipios:
                lista_nombres.append(item.nomMunicipio)
        elif opcion_seleccionada == "Central de Autobuses":  # ----------------
            self.tipo_rescateNombreL.config(text="Nombre del punto")
            for item in self.fuerzaInfo:
                if item.tipoP == "Central de autobús":
                    lista_nombres.append(item.nomPuntoRevision)
        elif opcion_seleccionada == "Ferrocarril":  # ------------------------
            self.tipo_rescateNombreL.config(text="Nombre del punto")
            for item in self.fuerzaInfo:
                if item.tipoP == "Ferroviario":
                    lista_nombres.append(item.nomPuntoRevision)
        elif opcion_seleccionada == "Hotel":  # -------------------------------
            self.tipo_rescateNombreL.config(text="Nombre del Municipio")
            for item in self.municipios:
                lista_nombres.append(item.nomMunicipio)
        elif opcion_seleccionada == "Puestos a Disposicion":  # ---------------
            self.tipo_rescateNombreL.config(text="Personal rescatado")
            pass
        elif opcion_seleccionada == "Voluntarios":
            self.tipo_rescateNombreL.config(text="")
            pass
        else:
            pass

        self.cb_Tipo_nombre.config(completevalues=lista_nombres)

    def configurar_scrollN(self, event):
        self.canvasN.configure(scrollregion=self.canvasN.bbox("all"), width=180, height=250)

    def configurar_scrollF(self, event):
        self.canvasF.configure(scrollregion=self.canvasF.bbox("all"), width=180, height=250)

    def mostrar_popupN(self):
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Diálogo con Combobox")

        # Lista de opciones para el Combobox

        # Variable para almacenar la opción seleccionada
        opcion_seleccionada = tk.StringVar()

        # Crear el Combobox en el diálogo
        combo_box = ttk.Combobox(
            dialogo,
            textvariable=opcion_seleccionada,
            values=self.opc_paises,
            state="readonly"
        )
        combo_box.pack(padx=20, pady=10)

        # Función para obtener la opción seleccionada en el Combobox
        def obtener_opcion():
            opcion = opcion_seleccionada.get()
            messagebox.showinfo("Opción seleccionada", f"Pais Seleccionado: {opcion}")
            dialogo.destroy()  # Cerrar el diálogo después de obtener la opción seleccionada

        # Botón para obtener la opción seleccionada
        boton = tk.Button(dialogo, text="Obtener Opción", command=obtener_opcion)
        boton.pack(pady=10)

    def mostrar_popupF(self):
        dialogo = tk.Toplevel(self.root)
        dialogo.title("Diálogo con Combobox")

        self.totalF = getTotalFamilias()
        # Lista de opciones para el Combobox
        opciones = []

        for i_opc in range(self.totalF):
            opciones.append(str(i_opc + 1))
        opciones.append("Nueva familia")

        # Variable para almacenar la opción seleccionada
        opcion_seleccionada = tk.StringVar()

        # Crear el Combobox en el diálogo
        combo_box = ttk.Combobox(
            dialogo,
            textvariable=opcion_seleccionada,
            values=opciones,
            state="readonly"
        )
        combo_box.pack(padx=20, pady=10)

        # Función para obtener la opción seleccionada en el Combobox
        def obtener_opcion():
            numFam = 0
            opcion = opcion_seleccionada.get()
            if opcion == "Nueva familia":
                numFam = self.totalF + 1
            else:
                numFam = int(opcion)
            messagebox.showinfo("Opción seleccionada", f"Familia Seleccionado: {numFam}")
            dialogo.destroy()  # Cerrar el diálogo después de obtener la opción seleccionada

            self.new.withdraw()
            ventana_secundaria = tk.Toplevel(self.root)
            self.ventanaSecundaria = RegistroScreenF(self.new, ventana_secundaria, self.opc_paises, numFam)
            self.ventanaSecundaria.registroFFrame()

        # Botón para obtener la opción seleccionada
        boton = tk.Button(dialogo, text="Obtener Opción", command=obtener_opcion)
        boton.pack(pady=10)


    def guardar_puntos(self, event):
        auxTP = self.opc_sel.get()
        auxNP = self.cb_Tipo_nombre.get()
        print(auxTP, auxNP)
        dato = PuntosInfo(
            idTP=1,
            tipo_punto=auxTP,
            nombre_punto=auxNP,
        )
        updatePunto(dato)

    def popUpInsert(self):
        self.new.withdraw()
        ventana_secundaria = tk.Toplevel(self.root)
        self.ventanaSecundaria = RegistroScreen(self.new, ventana_secundaria, self.opc_paises)
        self.ventanaSecundaria.registroFrame()

    def popUpEnviar(self):
        now = datetime.now()
        # self.horaL.config(text=f"Hora: {now.hour}:{now.minute}")
        self.horaL.config(text=f"Hora: {now.strftime('%H:%M')}")

        #-------------------------------------------
        #-------------------- Guardar datos en base -----------------
        #-------------------------------------------

        oficinaR, userInfo, fuerzaInfo, paises, municipios, puntosInt = getDataUC()
        infoResc = self.baseRescComp()

        infoResc.oficinaRepre = oficinaR
        infoResc.fecha = f"{now.day}-{now.month}-{now.year}"
        infoResc.hora = f"{now.strftime('%H:%M')}"
        infoResc.nombreAgente = f"{userInfo.apellido} {userInfo.nombre}"

        opcion_seleccionada = self.cb_Tipo.get()
        puntoE =self.cb_Tipo_nombre.get()

        if opcion_seleccionada == "Aeropuerto":  # ----------------------------
            infoResc.aeropuerto = True
            infoResc.puntoEstra = puntoE
        elif opcion_seleccionada == "Carretero":  # ---------------------------
            infoResc.carretero = True
            infoResc.puntoEstra = puntoE
        elif opcion_seleccionada == "Casa de Seguridad": # ---------------------------
            infoResc.casaSeguridad = True
            infoResc.municipio = puntoE
        elif opcion_seleccionada == "Central de Autobuses":  # ----------------
            infoResc.centralAutobus = True
            infoResc.puntoEstra = puntoE
        elif opcion_seleccionada == "Ferrocarril":  # ------------------------
            infoResc.ferrocarril = True
            infoResc.puntoEstra = puntoE
        elif opcion_seleccionada == "Hotel":  # -------------------------------
            infoResc.hotel = True
            infoResc.municipio = puntoE
        elif opcion_seleccionada == "Puestos a Disposicion":  # ---------------
            infoResc.puestosADispo = True
            infoResc.puntoEstra = puntoE
        elif opcion_seleccionada == "Voluntarios":
            infoResc.voluntarios = True
        else:
            pass

        sendRescates(infoResc)

        # ------------- LIMPIEZA ---------------------
        self.opc_sel_nombre = ""
        self.cb_Tipo_nombre.set("Nombre del Punto")
        self.opc_sel = ""
        self.cb_Tipo.set("Tipo de Punto")
        aux = PuntosInfo(idTP=1, tipo_punto="Tipo de Punto", nombre_punto="Nombre del Punto")
        updatePunto(aux)
        # self.horaL.config()

    def baseRescComp(self):
        a = RescateComp(
            oficinaRepre="",
            fecha="",
            hora="",
            nombreAgente="",

            aeropuerto=False,
            carretero=False,
            tipoVehic="",
            lineaAutobus="",
            numeroEcono="",
            placas="",
            vehiculoAseg=False,

            casaSeguridad=False,
            centralAutobus=False,

            ferrocarril=False,
            empresa="",

            hotel=False,
            nombreHotel="",

            puestosADispo=False,
            juezCalif=False,
            reclusorio=False,
            policiaFede=False,
            dif=False,
            policiaEsta=False,
            policiaMuni=False,
            guardiaNaci=False,
            fiscalia=False,
            otrasAuto=False,

            voluntarios=False,
            otro=False,

            presuntosDelincuentes=False,
            numPresuntosDelincuentes=0,

            municipio="",
            puntoEstra="",

            nacionalidad="",
            iso3="",
            nombre="",
            apellidos="",
            noIdentidad="00",
            parentesco="",
            fechaNacimiento="",
            sexo=True,
            embarazo=False,
            numFamilia=0,
            edad=0,
        )
        return a
