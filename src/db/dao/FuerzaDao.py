from src.db.models import Fuerza, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(Fuerza).all()
    session.close()
    return paises_db

def getById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    pais_db = session.query(Fuerza).filter_by(idFuerza=id).first()
    session.close()
    return pais_db

def insert(paises_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_save_objects(paises_info)
    session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(Fuerza).all()
    for dato in paises_db:
        session.delete(dato)
    session.commit()
    session.close()