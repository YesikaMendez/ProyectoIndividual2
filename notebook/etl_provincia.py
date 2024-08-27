import pandas as pd
from sqlalchemy import create_engine, text

# Lee el archivo Excel que está en el directorio 'data' dentro del proyecto
archivo_excel = '../data/Internet.xlsx'
df = pd.read_excel(archivo_excel, sheet_name=3)

#Dejar solo las columnas que se van a utilizar
df = df[['Provincia']].drop_duplicates()

# Crear una conexión a la base de datos SQL
engine = create_engine('mysql+pymysql://root:adm123@localhost:3306/internet')

# Crear la tabla 'penetracion_hogares' en la base de datos

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS provincia (
         id INT AUTO_INCREMENT PRIMARY KEY,
         provincia VARCHAR(250) NOT NULL
            )
        """))


df = df.rename(columns={
    'Provincia': 'provincia',
})

# Cargar los datos en la tabla de MySQL
df.to_sql('provincia', con=engine, if_exists='append', index=False)

print("Datos cargados exitosamente en la base de datos.")


