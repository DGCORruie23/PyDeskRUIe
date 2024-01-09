from src.db.models import RegistroNombres, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(RegistroNombres).all()
    session.close()
    return registros_db


def getById(id):
    
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(RegistroNombres).filter_by(idRegistroNom=id).first()
    session.close()

    # if not pais_db:
    #     pais_db = RegistroNombres(nickname = "", nombre = "", apellido = "", password = "", estado = "", tipo = "")

    return registros_db

def getAllIso():
    Session = sessionmaker(bind=engine)
    session = Session()
    resultados = session.query(
        RegistroNombres.iso3,
        func.count(RegistroNombres.iso3).label('conteo')
    ).group_by(RegistroNombres.iso3).all()
    return resultados

def getByIso(iso):
    Session = sessionmaker(bind=engine)
    session = Session()
    registros = session.query(RegistroNombres).filter_by(iso3=iso)
    session.close()
    return registros

def getNacForPin():
    Session = sessionmaker(bind=engine)
    session = Session()
    resultados = session.query(
        RegistroNombres.nacionalidad.label('nacionalidad'),
        func.count(RegistroNombres.nombre).label('totales'),
        RegistroNombres.sexo.label('sexo'),
        RegistroNombres.adulto.label('adulto'),
    ).group_by(
        RegistroNombres.nacionalidad,
        RegistroNombres.adulto,
        RegistroNombres.sexo
    ).order_by(
        RegistroNombres.nacionalidad.desc(),
        RegistroNombres.adulto.desc(),
        RegistroNombres.sexo.desc()
    ).all()

    session.close()

    return resultados


def insert(registros_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_save_objects(registros_info)
    session.commit()
    session.close()

def update(registros_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    registro_a_actualizar = session.query(RegistroNombres).filter_by(idRegistroNom=registros_info.idRegistroNom).first()
    if registro_a_actualizar:
        # print("entro actualizar")
        registro_a_actualizar.nacionalidad = registros_info.nacionalidad
        registro_a_actualizar.iso3 = registros_info.iso3
        registro_a_actualizar.nombre = registros_info.nombre
        registro_a_actualizar.apellidos = registros_info.apellidos
        registro_a_actualizar.fechaNacimiento = registros_info.fechaNacimiento
        registro_a_actualizar.sexo = registros_info.sexo
        registro_a_actualizar.embarazo = registros_info.embarazo
        print(registro_a_actualizar.nacionalidad)
        session.commit()
    session.close()

def deleteById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    registro_a_eliminar = session.query(RegistroNombres).filter_by(idRegistroNom=id).first()
    if registro_a_eliminar:
        session.delete(registro_a_eliminar)
        session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(RegistroNombres).all()
    for dato in registros_db:
        session.delete(dato)
    session.commit()
    session.close()
