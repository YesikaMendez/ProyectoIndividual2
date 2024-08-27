import pandas as pd
from sqlalchemy import create_engine, text

# Lee el archivo Excel que está en el directorio 'data' dentro del proyecto
archivo_excel = '../data/Internet.xlsx'
df_velocidad = pd.read_excel(archivo_excel, sheet_name='Totales Accesos por velocidad')

# Normalizar la tabla utilizando melt
df_insert = df_velocidad.melt(
    id_vars=['Año', 'Trimestre'],  # Columnas que permanecerán intactas
    value_vars=[
        'Hasta 512 kbps',
        'Entre 512 Kbps y 1 Mbps',
        'Entre 1 Mbps y 6 Mbps',
        'Entre 6 Mbps y 10 Mbps',
        'Entre 10 Mbps y 20 Mbps',
        'Entre 20 Mbps y 30 Mbps',
        'Más de 30 Mbps',
        'OTROS'
    ],  # Columnas que se transformarán en valores
    var_name='Rango_Velocidad',  # Nombre de la columna que contendrá los nombres originales de las columnas de velocidad
    value_name='Accesos'  # Nombre de la columna que contendrá los valores de accesos
)

# Verificar el contenido del DataFrame después de la normalización
print("Contenido de df_normalizado después de la normalización:")
print(df_insert.head())

from sqlalchemy import create_engine, text

# Crear una conexión a la base de datos SQL
engine = create_engine('mysql+pymysql://root:adm123@localhost:3306/internet')

# Crear la tabla 'accesos_por_velocidad' en la base de datos
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS accesos_por_velocidad (
            id INT AUTO_INCREMENT PRIMARY KEY,
            anio INT,
            trimestre INT,
            rango_velocidad VARCHAR(255),
            accesos INT,
            INDEX idx_anio (anio),
            INDEX idx_trimestre (trimestre),
            INDEX idx_rango_velocidad (rango_velocidad)
        )
    """))

# Renombrar las columnas para que coincidan con la tabla
df_insert = df_insert.rename(columns={
        'Año': 'anio',

    })

# Cargar los datos en la tabla de MySQL
df_insert.to_sql('accesos_por_velocidad', con=engine, if_exists='append', index=False)

print("Datos cargados exitosamente en la base de datos.")

