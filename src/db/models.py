from sqlalchemy import create_engine, Column, Integer, String, FLOAT, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///res/ruie_sqlite.db', echo=True)
# engine = create_engine('sqlite:///ruie_sqlite.db')
engine = create_engine('sqlite:///src/ruie_sqlite.db')
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    idUser = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    password = Column(String)
    estado = Column(String)
    tipo = Column(String)

class Fuerza(Base):
    __tablename__ = 'fuerza'
    idFuerza = Column(Integer, primary_key=True, autoincrement=True)
    oficinaR = Column(String)
    numPunto = Column(Integer)
    nomPuntoRevision = Column(String)
    tipoP = Column(String)
    ubicacion = Column(String)
    coordenadasTexto = Column(String)
    latitud = Column(FLOAT)
    longitud = Column(FLOAT)
    personalINM = Column(Integer)
    personalSEDENA = Column(Integer)
    personalMarina = Column(Integer)
    personalGuardiaN = Column(Integer)
    personalOTROS = Column(Integer)
    vehiculos = Column(Integer)
    seccion = Column(Integer)

class Municipio(Base):
    __tablename__ = 'municipio'
    idMunicipio = Column(Integer, primary_key=True, autoincrement=True)
    estado= Column(String)
    estadoAbr= Column(String)
    nomMunicipio= Column(String)

class Pais(Base):
    __tablename__ = 'pais'
    idPais = Column(Integer, primary_key=True, autoincrement=True)
    nombre_pais = Column(String)
    iso3 = Column(String)

class PuntosInter(Base):
    __tablename__ = 'puntosInter'
    idPuntosI = Column(Integer, primary_key=True, autoincrement=True)
    nombrePunto= Column(String)
    estadoPunto= Column(String)
    tipoPunto= Column(String)

class Mensaje(Base):
    __tablename__ = 'mensaje'
    idMsg = Column(Integer, primary_key=True, autoincrement=True)
    mensaje = Column(String)

class PuntosInfo(Base):
    __tablename__ = 'punto_info'
    idTP = Column(Integer, primary_key=True, autoincrement=True)
    tipo_punto = Column(String)
    nombre_punto = Column(String)

class RegistroNombres(Base):
    __tablename__ = 'registro_nombres'
    idRegistroNom = Column(Integer, primary_key=True, autoincrement=True)
    nacionalidad = Column(String)
    iso3 = Column(String)
    nombre = Column(String)
    apellidos = Column(String)
    noIdentidad = Column(String)
    fechaNacimiento = Column(String)
    adulto = Column(Boolean)
    sexo = Column(Boolean)
    embarazo = Column(Boolean)

class RegistroFamilias(Base):
    __tablename__ = 'registro_familias'
    idRegistroFam = Column(Integer, primary_key=True, autoincrement=True)
    nacionalidad = Column(String)
    iso3 = Column(String)
    nombre = Column(String)
    apellidos = Column(String)
    noIdentidad = Column(String)
    parentesco = Column(String)
    fechaNacimiento = Column(String)
    adulto = Column(Boolean)
    sexo = Column(Boolean)
    embarazo = Column(Boolean)
    numFamilia = Column(Integer)

class RescateComp(Base):
    __tablename__ = 'rescate_completo'

    idRescateC = Column(Integer, primary_key=True, autoincrement=True)
    oficinaRepre = Column(String)
    fecha = Column(String)
    hora = Column(String)
    nombreAgente = Column(String)

    aeropuerto = Column(Boolean)
    carretero = Column(Boolean)
    tipoVehic  = Column(String)
    lineaAutobus = Column(String)
    numeroEcono = Column(String)
    placas = Column(String)
    vehiculoAseg = Column(Boolean)
    
    casaSeguridad = Column(Boolean)
    centralAutobus = Column(Boolean)

    ferrocarril = Column(Boolean)
    empresa = Column(String)

    hotel = Column(Boolean)
    nombreHotel = Column(String)

    puestosADispo = Column(Boolean)
    juezCalif = Column(Boolean)
    reclusorio = Column(Boolean)
    policiaFede = Column(Boolean)
    dif = Column(Boolean)
    policiaEsta = Column(Boolean)
    policiaMuni = Column(Boolean)
    guardiaNaci = Column(Boolean)
    fiscalia = Column(Boolean)
    otrasAuto = Column(Boolean)
    
    voluntarios = Column(Boolean)
    otro = Column(Boolean)

    presuntosDelincuentes  = Column(Boolean)
    numPresuntosDelincuentes = Column(Integer)

    municipio = Column(String)
    puntoEstra = Column(String)

    nacionalidad = Column(String)
    iso3 = Column(String)
    nombre = Column(String)
    apellidos = Column(String)
    noIdentidad = Column(String)
    parentesco = Column(String)
    fechaNacimiento = Column(String)
    sexo = Column(Boolean)
    embarazo = Column(Boolean)
    numFamilia = Column(Integer)
    edad = Column(Integer)


Base.metadata.create_all(engine)