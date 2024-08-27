import pandas as pd
from sqlalchemy import create_engine, text

# Lee el archivo Excel que está en el directorio 'data' dentro del proyecto
archivo_excel = '../data/Internet.xlsx'
df_penetracion_h = pd.read_excel(archivo_excel, sheet_name='Penetracion-hogares')

# Crear una conexión a la base de datos SQL
engine = create_engine('mysql+pymysql://root:adm123@localhost:3306/internet')

# Consultar la tabla 'provincia' para obtener 'id' y 'provincia'
with engine.connect() as conn:
    query = text("SELECT id, provincia FROM provincia")
    df_provincia_sql = pd.read_sql(query, conn)

# Realizar un merge con df_penetracion para obtener la columna 'fk_provincia'
df_merged = df_penetracion_h.merge(df_provincia_sql, left_on='Provincia', right_on='provincia', how='left')
df_merged = df_merged.rename(columns={'id': 'fk_provincia'})

# Eliminar cualquier columna llamada 'provincia' o 'Provincia'
df_merged = df_merged.drop(columns=['provincia', 'Provincia'], errors='ignore')

# Verificar el contenido del DataFrame después del merge
print("Contenido de df_merged:")
print(df_merged.head())

# Crear la tabla 'penetracion_hogares' en la base de datos
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS penetracion_hogares (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fk_provincia INT NOT NULL,
            anio INT,
            trimestre INT,
            accesos FLOAT,
            INDEX idx_fk_provincia (fk_provincia),
            INDEX idx_anio (anio),
            INDEX idx_trimestre (trimestre),
            FOREIGN KEY (fk_provincia) REFERENCES provincia(id)
        )
    """))

# Renombrar las columnas para que coincidan con la tabla
df_merged = df_merged.rename(columns={
        'Año': 'anio',
        'Trimestre': 'trimestre',
        'Accesos por cada 100 hogares': 'accesos'
    })

# Cargar los datos en la tabla de MySQL
df_merged.to_sql('penetracion_hogares', con=engine, if_exists='append', index=False)

print("Datos cargados exitosamente en la base de datos.")
