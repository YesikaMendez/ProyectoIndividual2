import pandas as pd
from sqlalchemy import create_engine, text

# Lee el archivo Excel que está en el directorio 'data' dentro del proyecto
archivo_excel = '../data/Telefonia_movil.xlsx'

# 'sheet_name=0' lee la primera hoja (índice basado en 0)
df_hoja3 = pd.read_excel(archivo_excel, sheet_name=3)
df_hoja5 = pd.read_excel(archivo_excel, sheet_name=5)

# Eliminar columna llamada 'Periodo'
df_hoja3 = df_hoja3.drop(columns=['Periodo'], errors='ignore')

# Eliminar columna llamada 'Periodo'
df_hoja5= df_hoja5.drop(columns=['Periodo','Total de accesos pospago','Total de accesos prepago'], errors='ignore')

# Realizar un merge entre df_hoja3 y df_hoja4 usando 'año' y 'trimestre' como claves
df_merged = pd.merge(df_hoja3, df_hoja5, on=['Año', 'Trimestre'], how='inner')

# Verificar el contenido del DataFrame combinado
print("Contenido del DataFrame después del merge:")
print(df_merged.head())

# Crear una conexión a la base de datos SQL
engine = create_engine('mysql+pymysql://root:adm123@localhost:3306/internet')

# Crear la tabla 'movil_acces_ingresos' en la base de datos
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movil_acces_ingresos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            anio INT,
            trimestre INT,
            ingresos  FLOAT,
            accesos  FLOAT,
            INDEX idx_anio_trimestre (anio, trimestre)
        )
    """))

# Renombrar las columnas para que coincidan con la tabla en MySQL
df_merged = df_merged.rename(columns={
    'Año': 'anio',
    'Trimestre': 'trimestre',
    'Ingresos (miles de $)': 'ingresos',
    'Total de accesos operativos': 'accesos',

})
# Cargar los datos en la tabla de MySQL
df_merged.to_sql('movil_acces_ingresos', con=engine, if_exists='append', index=False)

print("Datos cargados exitosamente en la base de datos.")
