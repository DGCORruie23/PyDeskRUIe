from src.db.models import Usuario, Base, engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(Usuario).all()
    session.close()
    return paises_db


def getById(id):
    
    Session = sessionmaker(bind=engine)
    session = Session()
    pais_db = session.query(Usuario).filter_by(idUser=id).first()
    session.close()
    

    if not pais_db:
        pais_db = Usuario(nickname = "", nombre = "", apellido = "", password = "", estado = "", tipo = "")

    return pais_db

def insert(paises_info):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.bulk_save_objects(paises_info)
    # for dato in paises_info:
    #     session.add(dato)
    session.commit()
    session.close()

def update(user_info):
    Session = sessionmaker(bind=engine)
    session = Session()

    usuario_exist = session.query(Usuario).filter(Usuario.idUser == 1).first()
    
    if not usuario_exist:
        session.add(user_info)
    else:
        usuario_exist.nickname = user_info.nickname
        usuario_exist.nombre = user_info.nombre
        usuario_exist.apellido = user_info.apellido
        usuario_exist.password = user_info.password
        usuario_exist.estado = user_info.estado
        usuario_exist.tipo = user_info.tipo

    session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    paises_db = session.query(Usuario).all()
    for dato in paises_db:
        session.delete(dato)
    session.commit()
    session.close()