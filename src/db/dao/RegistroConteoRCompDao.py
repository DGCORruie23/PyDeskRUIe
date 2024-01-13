from src.db.models import DatosConteoRComp, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(DatosConteoRComp).all()
    session.close()
    return registros_db


def getById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(DatosConteoRComp).filter_by(idRegistroCR=id).first()
    session.close()

    return registros_db

def getAllIso():
    Session = sessionmaker(bind=engine)
    session = Session()
    resultados = session.query(
        DatosConteoRComp.iso3,
        func.count(DatosConteoRComp.iso3).label('conteo')
    ).group_by(DatosConteoRComp.iso3).all()
    return resultados

def getByIso(iso):
    Session = sessionmaker(bind=engine)
    session = Session()
    registros = session.query(DatosConteoRComp).filter_by(iso3=iso)
    session.close()
    return registros

def insert(registros_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_save_objects(registros_info)
    session.commit()
    session.close()

def deleteById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    registro_a_eliminar = session.query(DatosConteoRComp).filter_by(idRegistroCR=id).first()
    if registro_a_eliminar:
        session.delete(registro_a_eliminar)
        session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(DatosConteoRComp).all()
    for dato in registros_db:
        session.delete(dato)
    session.commit()
    session.close()
