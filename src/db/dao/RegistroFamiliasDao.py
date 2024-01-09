from src.db.models import RegistroFamilias, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(RegistroFamilias).all()
    session.close()
    return registros_db


def getById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(RegistroFamilias).filter_by(idRegistroFam=id).first()
    session.close()
    # if not pais_db:
    #     pais_db = RegistroNombres(nickname = "", nombre = "", apellido = "", password = "", estado = "", tipo = "")
    return registros_db

def getNumTotal():
    Session = sessionmaker(bind=engine)
    session = Session()
    total_familias  = session.query(func.IFNULL(func.max(RegistroFamilias.numFamilia), 0).label('totalFam')).scalar()
    session.close()
    return total_familias

def getAllNumFam():
    Session = sessionmaker(bind=engine)
    session = Session()
    resultados = session.query(
        RegistroFamilias.numFamilia,
        func.count(RegistroFamilias.numFamilia).label('conteo')
    ).group_by(RegistroFamilias.numFamilia).all()
    session.close()
    return resultados

def getByNumFam(numFam):
    Session = sessionmaker(bind=engine)
    session = Session()
    resultados = session.query(RegistroFamilias).filter_by(numFamilia=numFam)
    session.close()
    return resultados

def getFamForPin():
    Session = sessionmaker(bind=engine)
    session = Session()
    resultados = session.query(
        RegistroFamilias.nacionalidad.label('nacionalidad'),
        func.count(RegistroFamilias.nombre).label('totales'),
        RegistroFamilias.sexo.label('sexo'),
        RegistroFamilias.adulto.label('adulto'),
        RegistroFamilias.numFamilia.label('familia'),
    ).group_by(
        RegistroFamilias.numFamilia,
        RegistroFamilias.nacionalidad,
        RegistroFamilias.adulto,
        RegistroFamilias.sexo
    ).order_by(
        RegistroFamilias.nacionalidad.desc(),
        RegistroFamilias.adulto.desc(),
        RegistroFamilias.sexo.desc()
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
    registro_a_actualizar = session.query(RegistroFamilias).filter_by(idRegistroFam=registros_info.idRegistroFam).first()
    if registro_a_actualizar:
        registro_a_actualizar.nacionalidad = registros_info.nacionalidad
        registro_a_actualizar.iso3 = registros_info.iso3
        registro_a_actualizar.nombre = registros_info.nombre
        registro_a_actualizar.apellidos = registros_info.apellidos
        registro_a_actualizar.parentesco = registros_info.parentesco
        registro_a_actualizar.numFamilia = registros_info.numFamilia
        registro_a_actualizar.fechaNacimiento = registros_info.fechaNacimiento
        registro_a_actualizar.sexo = registros_info.sexo
        registro_a_actualizar.embarazo = registros_info.embarazo
        session.commit()
    session.close()

def deleteById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    registro_a_eliminar = session.query(RegistroFamilias).filter_by(idRegistroFam=id).first()
    if registro_a_eliminar:
        session.delete(registro_a_eliminar)
        session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(RegistroFamilias).all()
    for dato in registros_db:
        session.delete(dato)
    session.commit()
    session.close()