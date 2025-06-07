import pandas as pd
import time
import requests
import json
import random
import os
# from  config import *
from sqlalchemy import create_engine, text


# Credenciales API guardadas en github en sus variables de entorno
API_KEY = os.environ['API_KEY']
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
HOST = os.environ['HOST']
PORT = os.environ['PORT']   
DATABASE = os.environ['DATABASE']

# API_KEY = API_KEY
# USER = USER
# PASSWORD = PASSWORD
# HOST = HOST
# PORT = PORT   
# DATABASE = DATABASE


# Funciones
# Funcion para obtener los datos de las estadicticas del canal
# Esta funcion recibe el api_key y el channel_id y devuelve un diccionario con las estadisticas del canal
def get_stats(API_KEY,channel_id):
    
    url_channel_stats = 'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id='+channel_id+'&key='+API_KEY
    response_channels = requests.get(url_channel_stats)
    channel_stats = json.loads(response_channels.content)
    channel_stats = channel_stats['items'][0]['statistics']
    date = pd.to_datetime('today').strftime("%Y-%m-%d")

    data_channel = {

            'Date':date,
            'Total_Views':int(float(channel_stats['viewCount'])),
            'Subscribers':int(float(channel_stats['subscriberCount'])),
            'Video_count':int(float(channel_stats['videoCount']))
                        }

    return data_channel


# Funcion para obtener los datos de las estadisticas de varios canales 
def channels_stats(df,API_KEY):
    
    date = []
    views = []
    suscriber = []
    video_count = []
    channel_name = []
    
    tiempo = [1,2.5,2]
    
    for i in range(len(df)):
        
        stats_temp = get_stats(API_KEY,df['Channel_id'][i])
        
        channel_name.append(df['Channel_name'][i])
        date.append(stats_temp['Date'])
        views.append(stats_temp['Total_Views'])
        suscriber.append(stats_temp['Subscribers'])
        video_count.append(stats_temp['Video_count'])
     
    time.sleep(random.choice(tiempo))
    
    data = {
        
        'Channel_name':channel_name,
        'Subscribers':suscriber,
        'Video_count':video_count,
        'Total_Views':views,
        'Createt_at':date,
    }
    
    df_channels = pd.DataFrame(data)
    
    
    
    return df_channels 


# Funcion para guaradr los datos en un archivo csv
def guardar_csv(df, carpeta='channel_files'):
    # Crear carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Obtener fecha actual en formato YYYY-MM-DD
    fecha = pd.to_datetime('today').strftime("%Y-%m-%d")

    # Crear nombre de archivo
    nombre_archivo = f"youtube_stats_{fecha}.csv"

    # Ruta completa
    ruta_completa = os.path.join(carpeta, nombre_archivo)

    # Guardar DataFrame en CSV
    df.to_csv(ruta_completa, index=False, encoding='utf-8')

    print(f"Archivo guardado en: {ruta_completa}")



# guardar los datos en mysql
# Esta funcion recibe el df y la fecha y guarda los datos en mysql
def guardar_en_mysql(df, fecha):
    engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    tabla = 'youtube_stats'

    with engine.connect() as conn:
        stmt = text(f"DELETE FROM {tabla} WHERE Createt_at = :fecha")
        conn.execute(stmt, {"fecha": fecha})
        conn.commit()  # Esto es importante para que se apliquen los cambios

    df.to_sql(tabla, con=engine, if_exists='append', index=False)
    print(f"Datos guardados en MySQL para la fecha: {fecha}")
    

def guardar_procesar_segunda_tabla_en_mysql(df):
    # 1. Conexión a MySQL
    engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    tabla = 'youtube_stats'

    with engine.begin() as conn:
       
        # 3. Leer tabla original
        df_total = pd.read_sql(f"SELECT * FROM {tabla}", conn)

        # 4. Ordenar por canal y fecha
        df_total = df_total.sort_values(by=["Channel_name", "Createt_at"])

        # 5. Calcular columnas nuevas por canal
        df_total["Nuevos_Subscribers"] = df_total.groupby("Channel_name")["Subscribers"].diff().fillna(0).astype(int)
        df_total["Nuevas_Views"] = df_total.groupby("Channel_name")["Total_Views"].diff().fillna(0).astype(int)
        df_total["Nuevos_Videos"] = df_total.groupby("Channel_name")["Video_count"].diff().fillna(0).astype(int)

        # 6. Solo mantener columnas necesarias para la nueva tabla
        df_procesado = df_total[["id", "Channel_name","Nuevos_Subscribers", "Nuevas_Views", "Nuevos_Videos", "Createt_at"]]

        # 7. Truncar tabla destino
        conn.execute(text("TRUNCATE TABLE youtube_stats_procesada"))

        # 8. Insertar los datos procesados
        insert_query = """
            INSERT INTO youtube_stats_procesada (id, Channel_name, Nuevos_Subscribers, Nuevas_Views, Nuevos_Videos, Createt_at)
            VALUES (:id, :Channel_name, :Nuevos_Subscribers, :Nuevas_Views, :Nuevos_Videos, :Createt_at)
        """
        for _, row in df_procesado.iterrows():
            conn.execute(text(insert_query), row.to_dict())

    print("Datos procesados e insertados correctamente en youtube_stats_procesada.")


    
################### Crear df de canalas para analizar ###################

channels_name  =  ['Marciaylanube','TodoCode','PeladoNerd',
                   'Codigofacilito', 'Platzi', 'EDteam',
                   'Soy Dalto', 'midudev', 'freeCodeCamp',
                   'Valen Werle']
channels_id  =  ['UCWYUbW_Lw5EQC0WybxInObA','UCz0EXCSvMwYKruljsZjCOzw',
                 'UCrBzBOMcUVV8ryyAU_c6P5g','UCLXRGxAzeaLDGaOphqapzmg',
                 'UC55-mxUj5Nj3niXFReG44OQ', 'UCP15FVAA2UL-QOcGhy7-ezA',
                 'UCtoo4_P6ilCj7jwa4FmA5lQ','UC8LeXCWOalN8SxlrPcG-PaQ',
                 'UC8butISFwT-Wl7EV0hUK0BQ', 'UCyurPWRyQdR3S0OgPIa8MPA']

channels = {
    'Channel_name':channels_name,
    'Channel_id':channels_id}



if __name__ == "__main__":
   
    df_channels = pd.DataFrame(channels)

    print(df_channels)


    df = channels_stats(df_channels,API_KEY)
    print(df)

    guardar_csv(df, carpeta='channel_files')
    print("Archivo guardado correctamente")

    guardar_en_mysql(df, df['Createt_at'][0])
    print("Datos guardados en MySQL correctamente")
    
    guardar_procesar_segunda_tabla_en_mysql(df)

