import pandas as pd
import numpy as np
import logging
from datetime import datetime


def procesamiento_data(directorio_csv):

    #La función recibe la lista con los directorios donde se encuentran almacenados los csv. 
    #La función devuelve una lista con los 3 dataframes creados (3 tablas: tabla única, tabla de registros, tabla de cines)

    logging.info('Comenzando el procesamiento de datos...')
    tablas = []

    df_museos = pd.read_csv(directorio_csv[0],sep=",")
    df_cines = pd.read_csv(directorio_csv[1],sep=",")
    df_bibliotecas = pd.read_csv(directorio_csv[2],sep=",")

    # Seleccion de los datos de museos que nos interesan
    museos_cols = ["Cod_Loc", "IdProvincia", "IdDepartamento", "categoria", "provincia", "localidad", "nombre", "direccion",
              "CP", "telefono", "Mail", "Web", "fuente"]
    museos_seleccion = pd.DataFrame(df_museos[museos_cols])

    museos_cols_renombrado = {
                     'Cod_Loc': 'cod_localidad',
                     'IdProvincia': 'id_provincia',
                     'IdDepartamento': 'id_departamento',
                     'categoria': 'categoría',
                     'direccion': 'domicilio',
                     'CP': 'código postal',
                     'telefono': 'número de teléfono',
                     'Mail': 'mail',
                     'Web': 'web'
                    }

    museos_seleccion.rename(columns=museos_cols_renombrado, inplace=True)

    # Select de los datos de cines que nos interesan
    cines_cols = ["Cod_Loc", "IdProvincia", "IdDepartamento", "Categoría", "Provincia", "Localidad", "Nombre", "Dirección",
              "CP", "Teléfono", "Mail", "Web", "Fuente"]
    cines_seleccion = pd.DataFrame(df_cines[cines_cols])

    cines_cols_renombrado = {
                     'Cod_Loc': 'cod_localidad',
                     'IdProvincia': 'id_provincia',
                     'IdDepartamento': 'id_departamento',
                     'Categoría': 'categoría',
                     'Provincia': 'provincia',
                     'Localidad': 'localidad',
                     'Nombre': 'nombre',
                     'Dirección': 'domicilio',
                     'CP': 'código postal',
                     'Teléfono': 'número de teléfono',
                     'Mail': 'mail',
                     'Web': 'web',
                     'Fuente': 'fuente'
                    }

    cines_seleccion.rename(columns=cines_cols_renombrado, inplace=True)

    # Select de los datos de las bibliotecas que nos interesan
    bibliotecas_cols = ["Cod_Loc", "IdProvincia", "IdDepartamento", "Categoría", "Provincia", "Localidad", "Nombre", "Domicilio",
              "CP", "Teléfono", "Mail", "Web", "Fuente"]
    bibliotecas_seleccion = pd.DataFrame(df_bibliotecas[bibliotecas_cols])

    bibliotecas_cols_renombrado = {
                     'Cod_Loc': 'cod_localidad',
                     'IdProvincia': 'id_provincia',
                     'IdDepartamento': 'id_departamento',
                     'Categoría': 'categoría',
                     'Provincia': 'provincia',
                     'Localidad': 'localidad',
                     'Nombre': 'nombre',
                     'Domicilio': 'domicilio',
                     'CP': 'código postal',
                     'Teléfono': 'número de teléfono',
                     'Mail': 'mail',
                     'Web': 'web',
                     'Fuente': 'fuente'
                    }
    bibliotecas_seleccion.rename(columns=bibliotecas_cols_renombrado, inplace=True)

    # Crear un solo df con los datos de museos,cines,bibliotecas
    unico_df = pd.concat([museos_seleccion, cines_seleccion, bibliotecas_seleccion], axis=0)
    unico_df['fecha de carga'] = datetime.now().strftime('%Y-%m-%d')

    # Renombramiento de algunos valores 
    valores_renombrado = {
                 'Neuquén\xa0': 'Neuquén',
                 'Santa Fé': 'Santa Fe',
                 'Tierra del Fuego': 'Tierra del Fuego, Antártida e Islas del Atlántico Sur',
                 's/d': np.nan
                }
    unico_df.replace(valores_renombrado, inplace=True)

    #Generación de la primer tabla: Normalizar toda la información de Museos, Salas de Cine y Bibliotecas
    #Populares, para crear una única tabla.
    tabla_unica = pd.DataFrame(unico_df.drop('fuente', axis='columns'))
    tabla_unica.reset_index(drop=True, inplace=True)

    tablas.append(tabla_unica)

    # Generacion de df para la segunda tabla

    # Cantidad de registros totales por categoría
    categorias_df = unico_df.groupby(by="categoría")['mail'].count().reset_index()
    categorias_df.rename(columns={'mail': 'total por categoría'}, inplace=True)

    # Cantidad de registros totales por fuentes
    fuentes_df = unico_df.groupby(by="fuente")['mail'].count().reset_index()
    fuentes_df.rename(columns={'mail': 'total por fuente'}, inplace=True)

    # Cantidad de registros por provincia y categoría
    cols = ["provincia", "categoría", "fecha de carga"]
    prov_cat = unico_df.groupby(by=cols)['mail'].count().reset_index()
    prov_cat.rename(columns={'mail': 'total por provincia y categoría'}, inplace=True)
    prov_cat = prov_cat[["provincia", "categoría", "total por provincia y categoría", "fecha de carga"]]

    # Juntamos todo en una misma tabla
    tabla_registros = pd.concat([categorias_df, fuentes_df, prov_cat], axis=1)

    tablas.append(tabla_registros)

    # Generamos dataframe para tercer ejercicio (tabla de cines)

    # Procesamiento de los datos de cines
    cine_cols = ['Provincia', 'Pantallas', 'Butacas', 'espacio_INCAA']
    cine_seleccionado_3 = pd.DataFrame(df_cines[cine_cols])

    colsc_renombrado = {
                     'Pantallas': 'Cantidad de pantallas',
                     'Butacas': 'Cantidad de butacas',
                     'espacio_INCAA': 'Cantidad de espacios INCAA'
                    }
    cine_seleccionado_3.rename(columns=colsc_renombrado, inplace=True)

    # Reemplazo de valores
    cine_seleccionado_3.replace({0: np.nan}, inplace=True)

    # Creamos la tabla correspondiente
    data = {
            'Cantidad de pantallas': 'sum',
            'Cantidad de butacas': 'sum',
            'Cantidad de espacios INCAA': 'count'
           }
    tabla_cines = pd.DataFrame(cine_seleccionado_3.groupby(by='Provincia')[cine_seleccionado_3.columns].agg(data).reset_index())
    tabla_cines['fecha de carga'] = datetime.now().strftime('%Y-%m-%d')

    tablas.append(tabla_cines)

    logging.info('Datos procesados correctamente')

    return tablas
