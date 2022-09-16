import requests
import logging
from pathlib import Path
from datetime import datetime
from src.url import *


def extraccion_data():

    #Descarga 3 archivos csv desde sus respectivos urls, los guarda de forma local para luego utilizarlos.
    #La función devulve una lista con los directorios en donde guarda los 3 archivos csv.

    logging.info('Comenzando con la extracción de los datos...')
    directorio_csv = []

    url_museos = museos
    csv_museos = url_museos.replace('/edit#gid=', '/export?format=csv&gid=')

    url_cines = cines
    csv_cines = url_cines.replace('/edit#gid=', '/export?format=csv&gid=')

    url_bibliotecas = bibliotecas
    csv_bibliotecas = url_bibliotecas.replace('/edit#gid=', '/export?format=csv&gid=')

    categorias_url_dict = {
                    'museos': csv_museos,
                    'cines': csv_cines,
                    'bibliotecas':  csv_bibliotecas
                      }

    # Generación de los directorios de archivos csv
    for categoria, url in categorias_url_dict.items():
        direc = Path('/Datos/' + categoria + datetime.now().strftime('/%y-%m/'))
        direc_date = categoria + datetime.now().strftime('-%d-%m-%y') + '.csv'
        final_path = direc / direc_date

        
        direc.mkdir(parents=True, exist_ok=True)

        r = requests.get(url).content

        # Se guardan los archivos csv
        with open(final_path, 'wb') as file:
            file.write(r)
            directorio_csv.append(final_path)

    logging.info('Extracción de los datos realizada de forma satisfactoria')

    return directorio_csv
