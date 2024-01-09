from src.db.models import Pais, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(Pais).all()
    session.close()
    return paises_db


def getById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    pais_db = session.query(Pais).filter_by(idPais=id).first()
    session.close()
    return pais_db

def getNacByIso(iso):
    Session = sessionmaker(bind=engine)
    session = Session()
    pais_ = session.query(Pais).filter_by(iso3=iso).first()
    session.close()
    return pais_

def getIsoByNac(nac):
    Session = sessionmaker(bind=engine)
    session = Session()
    pais_ = session.query(Pais).filter_by(nombre_pais=nac).first()
    session.close()
    return pais_

def insert(paises_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_save_objects(paises_info)
    # for dato in paises_info:
    #     session.add(dato)
    session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(Pais).all()
    for dato in paises_db:
        session.delete(dato)
    session.commit()
    session.close()