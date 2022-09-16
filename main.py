from src.extraccion import *
from src.procesamiento import *
from src.carga import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

#El Programa consume datos desde 3 fuentes distintas con información cultural sobre bibliotecas, museos y salas de cines argentinos. 
#Luego los procesa y los almacena en una base de datos SQL.
#Si un error ocurre, en la pantalla se verá la frase "Un error ha ocurrido".

if __name__ == '__main__':

    try:
        logging.info('Iniciando el proceso de extraccion... ')
        directorio_csv = extraccion_data()
        tablas = procesamiento_data(directorio_csv)
        carga_data(tablas)
    except Exception as e:
        logging.error('Un error ha ocurrido')
        logging.error(e)
    else:
        logging.info('Proceso finalizado correctamente')
