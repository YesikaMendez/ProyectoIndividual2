import pandas as pd
from sqlalchemy import create_engine, text

# Lee la hoja de Totales VMD
archivo_excel = '../data/Internet.xlsx'
df_totales_vmd = pd.read_excel(archivo_excel, sheet_name='Totales VMD')

# Imprimir los nombres de las columnas para verificar
print("Columnas en el DataFrame antes de eliminar:", df_totales_vmd.columns)

# Eliminar la columna en la posición 3
df_totales_vmd = df_totales_vmd.drop(df_totales_vmd.columns[3], axis=1)

# Imprimir los nombres de las columnas después de eliminar
print("Columnas en el DataFrame después de eliminar:", df_totales_vmd.columns)

# Crear una conexión a la base de datos SQL
engine = create_engine('mysql+pymysql://root:adm123@localhost:3306/internet')

# Crear la tabla 'totales_vmd' en la base de datos
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS totales_vmd (
            id INT AUTO_INCREMENT PRIMARY KEY,
            anio INT,
            trimestre INT,
            mbps_media_bajada FLOAT,
            INDEX idx_anio (anio),
            INDEX idx_trimestre (trimestre)
        )
    """))

# Renombrar las columnas para que coincidan con la tabla
df_totales_vmd = df_totales_vmd.rename(columns={
        'Año': 'anio',
        'Trimestre': 'trimestre',
        'Mbps (Media de bajada)': 'mbps_media_bajada'
    })

# Cargar los datos en la tabla de MySQL
df_totales_vmd.to_sql('totales_vmd', con=engine, if_exists='append', index=False)

print("Datos cargados exitosamente en la base de datos.")


