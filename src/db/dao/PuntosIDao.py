from src.db.models import PuntosInter, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(PuntosInter).all()
    session.close()
    return paises_db

def getById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    pais_db = session.query(PuntosInter).filter_by(idPuntosI=id).first()
    session.close()
    return pais_db

def insert(paises_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    for dato in paises_info:
        session.add(dato)
    session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(PuntosInter).all()
    for dato in paises_db:
        session.delete(dato)
    session.commit()
    session.close()