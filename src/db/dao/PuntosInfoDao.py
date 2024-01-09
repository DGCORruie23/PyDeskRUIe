from src.db.models import PuntosInfo, engine
from sqlalchemy.orm import sessionmaker

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    mensaje_db = session.query(PuntosInfo).all()
    session.close()
    return mensaje_db

def getById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    mensaje_db = session.query(PuntosInfo).filter_by(idTP=id).first()
    session.close()
    return mensaje_db

def insert(mensajes_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_save_objects(mensajes_info)
    session.commit()
    session.close()

def update(registros_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    registro_a_actualizar = session.query(PuntosInfo).filter_by(idTP=registros_info.idTP).first()
    if registro_a_actualizar:
        # print("entro actualizar")
        registro_a_actualizar.tipo_punto = registros_info.tipo_punto
        registro_a_actualizar.nombre_punto = registros_info.nombre_punto
        # print(registro_a_actualizar.nacionalidad)
        session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    mensaje_db = session.query(PuntosInfo).all()
    for dato in mensaje_db:
        session.delete(dato)
    session.commit()
    session.close()