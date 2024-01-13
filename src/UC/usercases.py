from src.db.dao import PaisDao, MunicipioDao, FuerzaDao , PuntosIDao, UsuarioDao
from src.db.dao import MensajeDao, RegistroFamiliasDao, RegistroNombresDao
from src.db.dao import PuntosInfoDao, RescateCompDao, MensajeDao, RegistroConteoRDao, RegistroConteoRCompDao
from src.api.apisService import getAllPaisesApi, getAllMunicipiosApi, getAllFuerzaApi
from src.api.apisService import verifyUserApi, enviarRescate, enviarRescateConteo ,getAllPuntosIApi
from src.db.models import PuntosInfo, RescateComp, Mensaje, DatosConteoRComp
from datetime import datetime
import requests

def getAllPaisesUC():
    PaisDao.deleteAll()
    PaisDao.insert(getAllPaisesApi())

def getPaisesUC():
    return PaisDao.getAll()

def getAllMunicipiosUC():
    MunicipioDao.deleteAll()
    MunicipioDao.insert(getAllMunicipiosApi())

def getAllFuerzaUC():
    FuerzaDao.deleteAll()
    FuerzaDao.insert(getAllFuerzaApi())

def getAllPuntosIUC():
    PuntosIDao.deleteAll()
    PuntosIDao.insert(getAllPuntosIApi())

def verifyUser(datos):
    user = verifyUserApi(datos)

    if user.password == "ok":
        user.password = datos.password
        UsuarioDao.update(user)
        return True
    else:
        return False
    
def updateUser():
    userI = UsuarioDao.getById(1)
    user = verifyUserApi(userI)
    # print(user.nombre == "noInternet")
    # print(userI.nombre)

    if user.password == "ok" or (user.nombre == "noInternet" and userI.nombre != ""):
        return True
    else:
        return False
    
def getMensajesUC():
    mensajesI = MensajeDao.getAll()
    return mensajesI


def getDataUC():

    oficinasOR = []
    municipios_or = []
    fuerza_or = []
    puntosI_or = []
    
    usuario_db = UsuarioDao.getById(1)
    fuerzaAll_db = FuerzaDao.getAll()
    paises_db = PaisDao.getAll()
    municipios_db = MunicipioDao.getAll()
    puntoI_db = PuntosIDao.getAll()

    for item_municipios in municipios_db:
        if item_municipios.estado not in oficinasOR:
            oficinasOR.append(item_municipios.estado)

    # print(oficinasOR)

    or_agente = oficinasOR[int(usuario_db.estado) - 1]

    for item_fuerza in fuerzaAll_db:
        if item_fuerza.oficinaR == or_agente:
            fuerza_or.append(item_fuerza)

    for item_municipios in municipios_db:
        if item_municipios.estado == or_agente:
            municipios_or.append(item_municipios)

    for item_puntosI in puntoI_db:
        if item_puntosI.estadoPunto == or_agente:
            puntosI_or.append(item_puntosI)

    return or_agente, usuario_db, fuerza_or, paises_db, municipios_or, puntosI_or

def getIsos():
    return RegistroNombresDao.getAllIso()

def getNumFamilias():
    return RegistroFamiliasDao.getAllNumFam()

def getRegsByIso(iso):
    return RegistroNombresDao.getByIso(iso)

def getRegsByNumFam(numFam):
    return RegistroFamiliasDao.getByNumFam(numFam)

def getNacbyIso(iso):
    return PaisDao.getNacByIso(iso)

def getTotalFamilias():
    return RegistroFamiliasDao.getNumTotal()

def getCachePunto():
    punto = PuntosInfoDao.getById(1)
    if punto:
        print("existe")
        return punto
    else:
        print("no existe")
        aux = PuntosInfo(idTP=1, tipo_punto="Tipo de Punto", nombre_punto="Nombre del Punto")
        auxL = []
        auxL.append(aux)
        PuntosInfoDao.insert(auxL)
        return aux

def sendRescates(datosRescate):
    rescateN = RegistroNombresDao.getAll()
    rescateF = RegistroFamiliasDao.getAll()

    lista_ingresos = []

    for datosR in rescateN:
        lista_ingresos.append(convResComp(datosRescate, datosR, 0))
    for datosRF in rescateF:
        lista_ingresos.append(convResComp(datosRescate, datosRF, 1))


    #-------------- ingreso de datos a la tabla de rescates completos
    RescateCompDao.insert(lista_ingresos)

    #----------- Se crea el mensaje para el resumen ------------------

    numResN = len(rescateN)
    numResF = len(rescateF)
    datapin_rescTotales = numResN + numResF
    # datapin_isoTotales = getIsos()
    # datapin_numsFam = getNumFamilias()


    text_rescN = ""
    aux_txtNac = ""
    if numResN > 0:
        datosNpin = RegistroNombresDao.getNacForPin()
        for da in datosNpin:
            if da.nacionalidad != aux_txtNac:
                text_rescN = text_rescN + f"{da.nacionalidad}\n"
                aux_txtNac = da.nacionalidad
            if da.adulto and da.sexo:
                text_rescN = text_rescN + f"{da.totales} ADULTO(S) MASCULINO(S)\n"
            if da.adulto and not da.sexo:
                text_rescN = text_rescN + f"{da.totales} ADULTOS FEMENINO(S)\n"
            if not da.adulto and da.sexo:
                text_rescN = text_rescN + f"{da.totales} MENOR(ES) MASCULINO(S)\n"
            if not da.adulto and not da.sexo:
                text_rescN = text_rescN + (f"{da.totales} MENOR(ES) FEMENINO(S)\n")

    text_rescF = ""
    aux_txtFam = ""
    if numResF > 0:
        datosFpin = RegistroNombresDao.getNacForPin()
        for da in datosFpin:
            if da.nacionalidad != aux_txtNac:
                text_rescF = text_rescF + f"{da.nacionalidad}\n"
                aux_txtFam = da.nacionalidad
            if da.adulto and da.sexo:
                text_rescF = text_rescF + f"{da.totales} ADULTO(S) MASCULINO(S)\n"
            if da.adulto and not da.sexo:
                text_rescF = text_rescF + f"{da.totales} ADULTOS FEMENINO(S)\n"
            if not da.adulto and da.sexo:
                text_rescF = text_rescF + f"{da.totales} MENOR(ES) MASCULINO(S)\n"
            if not da.adulto and not da.sexo:
                text_rescF = text_rescF + (f"{da.totales} MENOR(ES) FEMENINO(S)\n")

    text_tipoResc = ""
    if datosRescate.aeropuerto:
        text_tipoResc = f"Aeropuerto: {datosRescate.puntoEstra}"
    elif datosRescate.carretero:
        text_tipoResc = f"Carretero: {datosRescate.puntoEstra}"
    elif datosRescate.casaSeguridad:
        text_tipoResc = f"Casa de Seguridad\n Municipio: {datosRescate.municipio}"
    elif datosRescate.centralAutobus:
        text_tipoResc = f"Central de Autobús: {datosRescate.puntoEstra}"
    elif datosRescate.ferrocarril:
        text_tipoResc = f"Ferrocarril: {datosRescate.puntoEstra}"
    elif datosRescate.hotel:
        text_tipoResc = f"Hotel \n Municipio: {datosRescate.municipio}"
    elif datosRescate.puestosADispo:
        text_tipoResc = f"Puestos a Disposición \n Por: "
    elif datosRescate.voluntarios :
        text_tipoResc = f"Voluntarios"
    else:
        pass

    pin_str = (
        f"OR: {datosRescate.oficinaRepre}\n" +
        f"Fecha: {datosRescate.fecha}\n" +
        # f"Hora: {datosRescate.hora}\n"+
        f"Agente: {datosRescate.nombreAgente}\n"+
        f"\n"+
        f"No. de Rescatados: {datapin_rescTotales}\n"+
        f"\n"+
        f"{text_tipoResc}\n"+
        f"\n"+
        f"{text_rescN}\n"+
        f"\n"+
        f"{text_rescF}\n"+
        f"\n"
    )

    list_msg = []
    list_msg.append(Mensaje(mensaje=pin_str))

    #----------- Ingreso del mensaje en la tabla
    MensajeDao.insert(list_msg)

    # ---------- Se eliminan los datos de las tablas anteriores
    RegistroNombresDao.deleteAll()
    RegistroFamiliasDao.deleteAll()

    #-------- Se envia la información al server

    if internetOn():
        respuestaAPI = enviarRescate(RescateCompDao.getAll())

        if respuestaAPI == "ok":
            RescateCompDao.deleteAll()


def sendConteo():
    datosPunto = PuntosInfoDao.getById(1)
    oficinaR, userInfo, fuerzaInfo, paises, municipios, puntosInt = getDataUC()
    now = datetime.now()
    datosConteo = RegistroConteoRDao.getAll()
    dataBase = baseConteoComp()

    dataBase.oficinaRepre = oficinaR
    dataBase.fecha = f"{now.strftime('%d-%m-%Y')}"
    dataBase.hora = f"{now.strftime('%H:%M')}"
    dataBase.nombreAgente = f"{userInfo.nombre} {userInfo.apellido}"

    if datosPunto.tipo_punto == "Aeropuerto":  # ----------------------------
        dataBase.aeropuerto = True
        dataBase.puntoEstra = datosPunto.nombre_punto
    elif datosPunto.tipo_punto == "Carretero":  # ---------------------------
        dataBase.carretero = True
        dataBase.puntoEstra = datosPunto.nombre_punto
    elif datosPunto.tipo_punto == "Casa de Seguridad":  # ---------------------------
        dataBase.casaSeguridad = True
        dataBase.municipio = datosPunto.nombre_punto
    elif datosPunto.tipo_punto == "Central de Autobuses":  # ----------------
        dataBase.centralAutobus = True
        dataBase.puntoEstra = datosPunto.nombre_punto
    elif datosPunto.tipo_punto == "Ferrocarril":  # ------------------------
        dataBase.ferrocarril = True
        dataBase.puntoEstra = datosPunto.nombre_punto
    elif datosPunto.tipo_punto == "Hotel":  # -------------------------------
        dataBase.hotel = True
        dataBase.municipio = datosPunto.nombre_punto
    elif datosPunto.tipo_punto == "Puestos a Disposicion":  # ---------------
        dataBase.puestosADispo = True
        dataBase.puntoEstra = datosPunto.nombre_punto
    elif datosPunto.tipo_punto == "Voluntarios":
        dataBase.voluntarios = True
    else:
        pass

    lista_conteo = []

    for data in datosConteo:
        lista_conteo.append(convResConteo(dataBase, data))

    RegistroConteoRCompDao.insert(lista_conteo)

    # ---------------- Generamos e insertamos el mensaje del conteo Rapido ---------------

    datosComp = RegistroConteoRDao.getAll()

    nuTotal = 0

    text_rescN = ""
    text_rescF = ""

    rescatesTotales = 0

    if len(datosComp) > 0:
        for da in datosComp:
            solos = da.AS_hombres + da.AS_mujeresNoEmb + da.AS_mujeresEmb + da.NNAsS_hombres + da.NNAsS_mujeresNoEmb + da.NNAsS_mujeresEmb
            acomp = da.AA_hombres + da.AA_mujeresNoEmb + da.AA_mujeresEmb + da.NNAsA_hombres + da.NNAsA_mujeresNoEmb + da.NNAsA_mujeresEmb

            rescatesTotales = rescatesTotales + solos + acomp

            if solos > 0:
                text_rescN = text_rescN + f"{da.nacionalidad}\n"
                if da.AS_hombres > 0:
                    text_rescN = text_rescN + f"{da.AS_hombres} ADULTO(S) MASCULINO(S)\n"
                if da.AS_mujeresNoEmb > 0:
                    text_rescN = text_rescN + f"{da.AS_mujeresNoEmb} ADULTO(S) FEMENINO(S)\n"
                if da.AS_mujeresEmb > 0:
                    text_rescN = text_rescN + f"{da.AS_mujeresEmb} ADULTO(S) FEMENINO(S) EMBARAZADO(S)\n"

                if da.NNAsS_hombres > 0:
                    text_rescN = text_rescN + f"{da.NNAsS_hombres} MENOR(ES) MASCULINO(S)\n"
                if da.NNAsS_mujeresNoEmb > 0:
                    text_rescN = text_rescN + f"{da.NNAsS_mujeresNoEmb} MENOR(ES) FEMENINO(S)\n"
                if da.NNAsS_mujeresEmb > 0:
                    text_rescN = text_rescN + f"{da.NNAsS_mujeresEmb} MENOR(ES) FEMENINO(S) EMBARAZADO(S)\n"

                text_rescN = text_rescN + "\n"

            if acomp > 0:
                if da.Nucleos_Familiares > 0:
                    nuTotal = nuTotal + da.Nucleos_Familiares

                    text_rescF = text_rescF + f"Nucleos Familiares de {da.nacionalidad}\n\n"

                    if da.AA_NNAs_hombres > 0:
                        text_rescF = text_rescF + f"{da.AA_hombres} ADULTO(S) MASCULINO(S)\n"
                    if da.AA_NNAs_mujeresNoEmb > 0:
                        text_rescF = text_rescF + f"{da.AA_mujeresNoEmb} ADULTO(S) FEMENINO(S)\n"
                    if da.AA_NNAs_mujeresEmb > 0:
                        text_rescF = text_rescF + f"{da.AA_mujeresEmb} ADULTO(S) FEMENINO(S) EMBARAZADO(S)\n"

                    if da.NNAsA_hombres > 0:
                        text_rescF = text_rescF + f"{da.NNAsA_hombres} MENOR(ES) MASCULINO(S)\n"
                    if da.NNAsA_mujeresNoEmb > 0:
                        text_rescF = text_rescF + f"{da.NNAsA_mujeresNoEmb} MENOR(ES) FEMENINO(S)\n"
                    if da.NNAsA_mujeresEmb > 0:
                        text_rescF = text_rescF + f"{da.NNAsA_mujeresEmb} MENOR(ES) FEMENINO(S) EMBARAZADO(S)\n"

                    text_rescF = text_rescF + "\n"

    text_rescF = ""
    aux_txtFam = ""

    text_tipoResc = ""
    if datosPunto.tipo_punto == "Aeropuerto":
        text_tipoResc = f"Aeropuerto: {datosPunto.nombre_punto}"
    elif datosPunto.tipo_punto == "Carretero":
        text_tipoResc = f"Carretero: {datosPunto.nombre_punto}"
    elif datosPunto.tipo_punto == "Casa de Seguridad":
        text_tipoResc = f"Casa de Seguridad\n Municipio: {datosPunto.nombre_punto}"
    elif datosPunto.tipo_punto == "Central de Autobuses":
        text_tipoResc = f"Central de Autobús: {datosPunto.nombre_punto}"
    elif datosPunto.tipo_punto == "Ferrocarril":
        text_tipoResc = f"Ferrocarril: {datosPunto.nombre_punto}"
    elif datosPunto.tipo_punto == "Hotel":
        text_tipoResc = f"Hotel \n Municipio: {datosPunto.nombre_punto}"
    elif datosPunto.tipo_punto == "Puestos a Disposicion":
        text_tipoResc = f"Puestos a Disposición \n Por: "
    elif datosPunto.tipo_punto == "Voluntarios":
        text_tipoResc = f"Voluntarios"
    else:
        pass

    pin_str = (
            f"OR: {dataBase.oficinaRepre}\n" +
            f"Fecha: {dataBase.fecha}\n" +
            # f"Hora: {datosRescate.hora}\n"+
            f"Agente: {dataBase.nombreAgente}\n" +
            f"\n" +
            f"No. de Rescatados: {rescatesTotales}\n" +
            f"\n" +
            f"{text_tipoResc}\n" +
            f"\n" +
            f"{text_rescN}\n" +
            f"\n" +
            f"{text_rescF}\n" +
            f"\n")
    # ----- Se eliminan los datos anteriores
    RegistroConteoRDao.deleteAll()

    list_msg = []
    list_msg.append(Mensaje(mensaje=pin_str))

    # ----------- Ingreso del mensaje en la tabla
    MensajeDao.insert(list_msg)

    # -------- Se envia la información al server

    if internetOn():
        respuestaAPI = enviarRescateConteo(RegistroConteoRCompDao.getAll())

        if respuestaAPI == "ok":
            RegistroConteoRCompDao.deleteAll()



    # print(pin_str)
def convResComp(resInfo, resDato, tipo):

    aux_parentesco = ""
    aux_numFam = 0

    born = datetime.strptime(resDato.fechaNacimiento, "%d-%m-%Y")
    today = datetime.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    aux_edad = age

    if tipo == 1:
        aux_parentesco = resDato.parentesco
        aux_numFam = resDato.numFamilia

    res = RescateComp(
            oficinaRepre= resInfo.oficinaRepre,
            fecha=resInfo.fecha,
            hora=resInfo.hora,
            nombreAgente=resInfo.nombreAgente,

            aeropuerto=resInfo.aeropuerto,
            carretero=resInfo.carretero,
            tipoVehic=resInfo.tipoVehic,
            lineaAutobus=resInfo.lineaAutobus,
            numeroEcono=resInfo.numeroEcono,
            placas=resInfo.placas,
            vehiculoAseg=resInfo.vehiculoAseg,

            casaSeguridad=resInfo.casaSeguridad,
            centralAutobus=resInfo.centralAutobus,

            ferrocarril=resInfo.ferrocarril,
            empresa=resInfo.empresa,

            hotel=resInfo.hotel,
            nombreHotel=resInfo.nombreHotel,

            puestosADispo=resInfo.puestosADispo,
            juezCalif=resInfo.juezCalif,
            reclusorio=resInfo.reclusorio,
            policiaFede=resInfo.policiaFede,
            dif=resInfo.dif,
            policiaEsta=resInfo.policiaEsta,
            policiaMuni=resInfo.policiaMuni,
            guardiaNaci=resInfo.guardiaNaci,
            fiscalia=resInfo.fiscalia,
            otrasAuto=resInfo.otrasAuto,

            voluntarios=resInfo.voluntarios,
            otro=resInfo.otro,

            presuntosDelincuentes=resInfo.presuntosDelincuentes,
            numPresuntosDelincuentes=resInfo.numPresuntosDelincuentes,

            municipio=resInfo.municipio,
            puntoEstra=resInfo.puntoEstra,

            nacionalidad=resDato.nacionalidad,
            iso3=resDato.iso3,
            nombre=resDato.nombre,
            apellidos=resDato.apellidos,
            noIdentidad=resDato.noIdentidad,
            parentesco=aux_parentesco,
            fechaNacimiento=resDato.fechaNacimiento,
            sexo=resDato.sexo,
            embarazo=resDato.embarazo,
            numFamilia=aux_numFam,

            edad=aux_edad,
        )
    return res

def convResConteo(resInfo, rapidoInfo):

    res = DatosConteoRComp(
        oficinaRepre=resInfo.oficinaRepre,
        fecha=resInfo.fecha,
        hora=resInfo.hora,
        nombreAgente=resInfo.nombreAgente,

        aeropuerto=resInfo.aeropuerto,
        carretero=resInfo.carretero,
        tipoVehic=resInfo.tipoVehic,
        lineaAutobus=resInfo.lineaAutobus,
        numeroEcono=resInfo.numeroEcono,
        placas=resInfo.placas,
        vehiculoAseg=resInfo.vehiculoAseg,

        casaSeguridad=resInfo.casaSeguridad,
        centralAutobus=resInfo.centralAutobus,

        ferrocarril=resInfo.ferrocarril,
        empresa=resInfo.empresa,

        hotel=resInfo.hotel,
        nombreHotel=resInfo.nombreHotel,

        puestosADispo=resInfo.puestosADispo,
        juezCalif=resInfo.juezCalif,
        reclusorio=resInfo.reclusorio,
        policiaFede=resInfo.policiaFede,
        dif=resInfo.dif,
        policiaEsta=resInfo.policiaEsta,
        policiaMuni=resInfo.policiaMuni,
        guardiaNaci=resInfo.guardiaNaci,
        fiscalia=resInfo.fiscalia,
        otrasAuto=resInfo.otrasAuto,

        voluntarios=resInfo.voluntarios,
        otro=resInfo.otro,

        presuntosDelincuentes=resInfo.presuntosDelincuentes,
        numPresuntosDelincuentes=resInfo.numPresuntosDelincuentes,

        municipio=resInfo.municipio,
        puntoEstra=resInfo.puntoEstra,

        nacionalidad=rapidoInfo.nacionalidad,
        iso3=rapidoInfo.iso3,
        AS_hombres=rapidoInfo.AS_hombres,
        AS_mujeresNoEmb=rapidoInfo.AS_mujeresNoEmb,
        AS_mujeresEmb=rapidoInfo.AS_mujeresEmb,
        NNAsS_hombres=rapidoInfo.NNAsS_hombres,
        NNAsS_mujeresNoEmb=rapidoInfo.NNAsS_mujeresNoEmb,
        NNAsS_mujeresEmb=rapidoInfo.NNAsS_mujeresEmb,
        Nucleos_Familiares=rapidoInfo.Nucleos_Familiares,
        AA_NNAs_hombres=rapidoInfo.AA_hombres,
        AA_NNAs_mujeresNoEmb=rapidoInfo.AA_mujeresNoEmb,
        AA_NNAs_mujeresEmb=rapidoInfo.AA_mujeresEmb,
        NNAsA_hombres=rapidoInfo.NNAsA_hombres,
        NNAsA_mujeresNoEmb=rapidoInfo.NNAsA_mujeresNoEmb,
        NNAsA_mujeresEmb=rapidoInfo.NNAsA_mujeresEmb,
    )
    return res

def baseConteoComp():
    a = DatosConteoRComp(
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
        AS_hombres=0,
        AS_mujeresNoEmb=0,
        AS_mujeresEmb=0,
        NNAsS_hombres=0,
        NNAsS_mujeresNoEmb=0,
        NNAsS_mujeresEmb=0,
        Nucleos_Familiares=0,
        AA_NNAs_hombres=0,
        AA_NNAs_mujeresNoEmb=0,
        AA_NNAs_mujeresEmb=0,
        NNAsA_hombres=0,
        NNAsA_mujeresNoEmb=0,
        NNAsA_mujeresEmb=0,
    )
    return a

def internetOn():
    try:
        # Intentar hacer una solicitud a una URL conocida
        response = requests.get("https://www.google.com", timeout=5)  # Por ejemplo a Google

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Conexión a Internet exitosa")
            return True
        else:
            print("No se pudo conectar al sitio web")
            return False
    except requests.ConnectionError:
        print("No hay conexión a Internet")
        return False