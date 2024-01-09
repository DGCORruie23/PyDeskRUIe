from src.db.dao import PaisDao, MunicipioDao, FuerzaDao , PuntosIDao, UsuarioDao
from src.db.dao import MensajeDao, RegistroFamiliasDao, RegistroNombresDao
from src.db.dao import PuntosInfoDao, RescateCompDao, MensajeDao
from src.api.apisService import getAllPaisesApi, getAllMunicipiosApi, getAllFuerzaApi, getAllPuntosIApi, verifyUserApi, enviarRescate
from src.db.models import PuntosInfo, RescateComp, Mensaje
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

    if internetOn():
        respuestaAPI = enviarRescate(RescateCompDao.getAll())

        if respuestaAPI == "ok":
            RescateCompDao.deleteAll()

    RegistroNombresDao.deleteAll()
    RegistroFamiliasDao.deleteAll()




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