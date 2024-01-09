from src.db.models import Mensaje, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    mensaje_db = session.query(Mensaje).all()
    session.close()
    return mensaje_db

def getById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    mensaje_db = session.query(Mensaje).filter_by(idMsg=id).first()
    session.close()
    return mensaje_db

def insert(mensajes_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_save_objects(mensajes_info)
    session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    mensaje_db = session.query(Mensaje).all()
    for dato in mensaje_db:
        session.delete(dato)
    session.commit()
    session.close()