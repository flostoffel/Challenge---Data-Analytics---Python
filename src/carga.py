import logging
from sqlalchemy import create_engine
from env import *


def carga_data(tablas):

    #Convertir los diferentes dataframes en tablas para poder cargarlos en una base de datos SQL.


    logging.info('Comenzando con la carga de los datos...')
    # Creamos la conexión a la base de datos
    engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    # Creamos tablas vacías desde sql.file
    engine.execute(open(r"src\tablas.sql", encoding='utf-8-sig').read())

    # Cargamos los datos
    tablas[0].to_sql('tabla_unica', con=engine, if_exists='replace', index=False)
    tablas[1].to_sql('tabla_registros', con=engine, if_exists='replace', index=False)
    tablas[2].to_sql('tabla_cines', con=engine, if_exists='replace', index=False)

    logging.info('Carga de datos exitosa')

    return