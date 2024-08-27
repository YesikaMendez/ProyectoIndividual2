import pandas as pd
import unicodedata
from sqlalchemy import create_engine, text

# Lee el archivo Excel que está en el directorio 'data' dentro del proyecto
archivo_excel = '../data/mapa_conectividad.xlsx'

# 'sheet_name=0' lee la primera hoja (índice basado en 0)
df_hoja1 = pd.read_excel(archivo_excel, sheet_name=0)

# Crear una conexión a la base de datos SQL
engine = create_engine('mysql+pymysql://root:adm123@localhost:3306/internet')

# Consultar la tabla 'provincia' para obtener 'id' y 'provincia'
with engine.connect() as conn:
    query = text("SELECT id, provincia FROM provincia")
    df_provincia_sql = pd.read_sql(query, conn)

# Crear la tabla 'penetracion_hogares' en la base de datos

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS mapa_conectividad (
         id INT AUTO_INCREMENT PRIMARY KEY,
         fk_provincia INT NOT NULL,
         partido VARCHAR(255),
         localidad VARCHAR(255),
         poblacion INT,
         servicio varchar(255),
         presencia boolean,
         latitud FLOAT,
         longitud FLOAT,
         FOREIGN KEY (fk_provincia) REFERENCES provincia(id),
         INDEX idx_fk_provincia (fk_provincia),
         INDEX idx_prtido (partido),
         INDEX idx_localidad (localidad),
         INDEX idx_servicio (servicio)
            )
        """))




def quitar_tildes(texto):
    # Normalizar el texto a la forma NFC (composición)
    texto_normalizado = unicodedata.normalize('NFD', texto)

    # Filtrar los caracteres que no sean de la categoría "Mn" (marca no espaciada, que incluye las tildes)
    texto_sin_tildes = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')

    # Devolver el texto sin tildes
    return texto_sin_tildes

# Convertir los nombres de las provincias a minusculas y quitar tildes
df_hoja1['Provincia'] = df_hoja1['Provincia'].apply(lambda x: quitar_tildes(x).lower())
df_provincia_sql['provincia'] = df_provincia_sql['provincia'].apply(lambda x: quitar_tildes(x).lower())


# Realizar un merge con df_penetracion para obtener la columna 'fk_provincia'
df_merged = df_hoja1.merge(df_provincia_sql, left_on='Provincia', right_on='provincia', how='left')
df_merged = df_merged.rename(columns={'id': 'fk_provincia'})

# Convertir fk_provincia a int, manejando los NaN
df_merged['fk_provincia'] = df_merged['fk_provincia'].fillna(0).astype(int)

# Eliminar cualquier columna llamada 'provincia' o 'Provincia'
df_merged = df_merged.drop(columns=['provincia', 'Provincia'], errors='ignore')

df_merged = df_merged.drop(columns=['Link'], errors='ignore')

# Usar melt para transformar el DataFrame
df_melted = df_merged.melt(id_vars=['fk_provincia', 'Partido', 'Localidad','Población','Latitud','Longitud'],
                           var_name='servicio',
                           value_name='presencia')

# Convertir la columna 'presencia' a boolean
df_melted['presencia_bool'] = df_melted['presencia'].apply(lambda x: True if x == 'SI' else False)

# Eliminar la columna 'presencia'
df_melted = df_melted.drop(columns=['presencia'], errors='ignore')


# Verificar el contenido del DataFrame después de melt
print(df_melted.head())

df_melted = df_melted.rename(columns={
        'Partido': 'partido',
        'Localidad': 'localidad',
        'Población': 'poblacion',
        'Latitud': 'latitud',
        'Longitud': 'longitud',
        'presencia_bool': 'presencia',
    })
# Cargar los datos en la tabla de MySQL
df_melted.to_sql('mapa_conectividad', con=engine, if_exists='append', index=False)

print("Datos cargados exitosamente en la base de datos.")



