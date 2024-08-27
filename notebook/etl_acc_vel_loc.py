import pandas as pd
from sqlalchemy import create_engine, text

# Lee el archivo Excel que está en el directorio 'data' dentro del proyecto
archivo_excel = '../data/Internet.xlsx'

# 'sheet_name=0' lee la primera hoja (índice basado en 0)
df_hoja1 = pd.read_excel(archivo_excel, sheet_name=0)

# Crear una conexión a la base de datos SQL
engine = create_engine('mysql+pymysql://root:adm123@localhost:3306/internet')

# Consultar la tabla 'provincia' para obtener 'id' y 'provincia'
with engine.connect() as conn:
    query = text("SELECT id, provincia FROM provincia")
    df_provincia_sql = pd.read_sql(query, conn)

# Convertir ambas columnas a un mismo formato antes del merge
df_hoja1['Provincia'] = df_hoja1['Provincia'].str.upper()
df_provincia_sql['provincia'] = df_provincia_sql['provincia'].str.upper()

# Realizar un merge con df_hoja1 para obtener la columna 'fk_provincia'
df_merged = df_hoja1.merge(df_provincia_sql, left_on='Provincia', right_on='provincia', how='left')
df_merged = df_merged.rename(columns={'id': 'fk_provincia'})

# Convertir fk_provincia a int, manejando los NaN
df_merged['fk_provincia'] = df_merged['fk_provincia'].fillna(0).astype(int)

# Eliminar las columnas 'Provincia', 'provincia', y 'Link Indec'
df_merged = df_merged.drop(columns=['Provincia', 'provincia', 'Link Indec'])

# Imputar valores NaN en las columnas de velocidad con ceros
df_merged = df_merged.fillna(0)

# Convertir las columnas de velocidad a int
velocidad_cols = df_merged.columns[3:]  # Ajusta si hay más columnas antes de las velocidades
df_merged[velocidad_cols] = df_merged[velocidad_cols].astype(int)

# Usar melt para transformar el DataFrame
df_melted = df_merged.melt(id_vars=['fk_provincia', 'Partido', 'Localidad'],
                           var_name='velocidad',
                           value_name='conexiones')

# Convertir la columna 'conexiones' a int
df_melted['conexiones'] = df_melted['conexiones'].astype(int)

# Verificar el contenido del DataFrame después de melt
print("Contenido de df_melted:")
print(df_melted.head())

# Crear la tabla 'acc_vel_loc' si no existe
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS acc_vel_loc (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fk_provincia INT NOT NULL,
            partido VARCHAR(255),
            localidad VARCHAR(255),
            velocidad VARCHAR(255),
            conexiones INT,
            INDEX idx_fk_provincia (fk_provincia),
            INDEX idx_localidad (localidad),
            INDEX idx_partido (partido),
            INDEX idx_velocidad (velocidad)
        )
    """))

# Renombrar las columnas para que coincidan con la tabla
df_melted = df_melted.rename(columns={
        'Partido': 'partido',
        'Localidad': 'localidad',

    })
# Cargar los datos en la tabla de MySQL
df_melted.to_sql('acc_vel_loc', con=engine, if_exists='append', index=False)

print("Datos cargados exitosamente en la base de datos.")
