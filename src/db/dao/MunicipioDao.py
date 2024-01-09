from src.db.models import Municipio, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(Municipio).all()
    session.close()
    return paises_db

def getById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    pais_db = session.query(Municipio).filter_by(idMunicipio=id).first()
    session.close()
    return pais_db

def insert(municipios_info):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.bulk_save_objects(municipios_info)

    session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(Municipio).all()
    for dato in paises_db:
        session.delete(dato)
    session.commit()
    session.close()