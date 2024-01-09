from src.db.models import RescateComp, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(RescateComp).all()
    session.close()
    return registros_db


def getById(id):
    
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(RescateComp).filter_by(idRegistroNom=id).first()
    session.close()

    # if not pais_db:
    #     pais_db = RegistroNombres(nickname = "", nombre = "", apellido = "", password = "", estado = "", tipo = "")

    return registros_db

def insert(registros_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_save_objects(registros_info)
    session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(RescateComp).all()
    for dato in registros_db:
        session.delete(dato)
    session.commit()
    session.close()