from src.db.models import DatosConteoR, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

def getAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(DatosConteoR).all()
    session.close()
    return registros_db

def getById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(DatosConteoR).filter_by(idRegistro=id).first()
    session.close()

    return registros_db

def getAllIso():
    Session = sessionmaker(bind=engine)
    session = Session()
    resultados = session.query(
        DatosConteoR.iso3,
        func.count(DatosConteoR.iso3).label('conteo')
    ).group_by(DatosConteoR.iso3).all()
    return resultados

def getByIso(iso):
    Session = sessionmaker(bind=engine)
    session = Session()
    registros = session.query(DatosConteoR).filter_by(iso3=iso)
    session.close()
    return registros

def getTotal():
    Session = sessionmaker(bind=engine)
    session = Session()
    resultados = session.query(
        func.ifnull(
            func.sum(
                DatosConteoR.AS_hombres + DatosConteoR.AS_mujeresNoEmb +
                DatosConteoR.AS_mujeresEmb + DatosConteoR.AA_hombres +
                DatosConteoR.AA_mujeresNoEmb + DatosConteoR.AA_mujeresEmb +
                DatosConteoR.NNAsA_hombres + DatosConteoR.NNAsA_mujeresNoEmb +
                DatosConteoR.NNAsA_mujeresEmb + DatosConteoR.NNAsS_hombres +
                DatosConteoR.NNAsS_mujeresNoEmb + DatosConteoR.NNAsS_mujeresEmb), 0)).scalar()

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
    registro_a_actualizar = session.query(DatosConteoR).filter_by(idRegistro=registros_info.idRegistro).first()
    if registro_a_actualizar:
        print("entro id")
        registro_a_actualizar.nacionalidad = registros_info.nacionalidad
        registro_a_actualizar.iso3 = registros_info.iso3
        registro_a_actualizar.AS_hombres = registros_info.AS_hombres
        registro_a_actualizar.AS_mujeresNoEmb = registros_info.AS_mujeresNoEmb
        registro_a_actualizar.AS_mujeresEmb = registros_info.AS_mujeresEmb
        registro_a_actualizar.NNAsS_hombres = registros_info.NNAsS_hombres
        registro_a_actualizar.NNAsS_mujeresNoEmb = registros_info.NNAsS_mujeresNoEmb
        registro_a_actualizar.NNAsS_mujeresEmb = registros_info.NNAsS_mujeresEmb

        registro_a_actualizar.Nucleos_Familiares = registros_info.Nucleos_Familiares
        registro_a_actualizar.AA_hombres = registros_info.AA_hombres
        registro_a_actualizar.AA_mujeresNoEmb = registros_info.AA_mujeresNoEmb
        registro_a_actualizar.AA_mujeresEmb = registros_info.AA_mujeresEmb
        registro_a_actualizar.NNAsA_hombres = registros_info.NNAsA_hombres
        registro_a_actualizar.NNAsA_mujeresNoEmb = registros_info.NNAsA_mujeresNoEmb
        registro_a_actualizar.NNAsA_mujeresEmb = registros_info.NNAsA_mujeresEmb
        print(registro_a_actualizar.nacionalidad)
        session.commit()
    session.close()

def deleteById(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    registro_a_eliminar = session.query(DatosConteoR).filter_by(idRegistro=id).first()
    if registro_a_eliminar:
        session.delete(registro_a_eliminar)
        session.commit()
    session.close()

def deleteAll():
    Session = sessionmaker(bind=engine)
    session = Session()
    registros_db = session.query(DatosConteoR).all()
    for dato in registros_db:
        session.delete(dato)
    session.commit()
    session.close()
