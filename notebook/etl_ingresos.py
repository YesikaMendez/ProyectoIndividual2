import pandas as pd
from sqlalchemy import create_engine, text

# Lee el archivo Excel que está en el directorio 'data' dentro del proyecto
archivo_excel = '../data/Internet.xlsx'

# Verificar las hojas disponibles en el archivo Excel
xls = pd.ExcelFile(archivo_excel)
print("Hojas disponibles en el archivo Excel:", xls.sheet_names)

# 'sheet_name=14' lee la hoja en el índice 14
df_ingresos = pd.read_excel(archivo_excel, sheet_name=14)

# Imprimir los nombres de las columnas para verificar
print("Columnas en el DataFrame antes de eliminar:", df_ingresos.columns)

# Eliminar la columna en la posición 3 periodo
df_ingresos = df_ingresos.drop(df_ingresos.columns[3], axis=1)

# Crear una conexión a la base de datos SQL
engine = create_engine('mysql+pymysql://root:adm123@localhost:3306/internet')

# Crear la tabla 'ingresos' en la base de datos con un id auto_incremental
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS ingresos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            anio INT,
            trimestre INT,
            ingresos FLOAT,
            INDEX idx_anio (anio),
            INDEX idx_trimestre (trimestre)
        )
    """))

# Renombrar las columnas para que coincidan con la tabla en MySQL
df_ingresos = df_ingresos.rename(columns={
    'Año': 'anio',
    'Trimestre': 'trimestre',
    'Ingresos (miles de pesos)': 'ingresos'
})

# Cargar los datos en la tabla de MySQL
df_ingresos.to_sql('ingresos', con=engine, if_exists='append', index=False)

print("Datos cargados exitosamente en la base de datos.")
