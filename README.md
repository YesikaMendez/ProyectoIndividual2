# ProyectoIndividual2
Análisis exploratorio de los datos a una empresa prestadora de servicios de telecomunicaciones

Proyecto: Análisis Exploratorio de Datos sobre Conectividad en Argentina

1. Introducción: Este proyecto tiene como objetivo analizar la conectividad a Internet en Argentina, 
explorando diferentes aspectos como la velocidad de descarga, penetración en hogares y población, y rentabilidad de los
servicios de Internet fijo y móvil. El análisis busca identificar patrones, desigualdades regionales y oportunidades de
mejora en la infraestructura de telecomunicaciones.

2. Estructura del Proyecto:

Carpeta data/: Contiene los archivos Excel con los datos crudos de Internet, telefonía móvil, televisión y conectividad.
Carpeta notebook/: Incluye scripts de ETL (etl_*.py) para transformar y cargar los datos, y un notebook (eda.ipynb) con 
el análisis exploratorio y visualizaciones. Archivos ETL (etl_*.py): Scripts individuales para cada conjunto de datos,
transformando y cargando la información en una base de datos MySQL. eda.ipynb: Notebook que contiene el análisis
exploratorio de datos (EDA), incluyendo el análisis de valores faltantes, duplicados, distribución de datos, y la 
creación de KPIs.

3. Análisis Exploratorio de Datos (EDA):

Valores Faltantes y Duplicados: Ninguna tabla contiene valores faltantes o duplicados, lo que asegura que los datos son 
completos y fiables para el análisis. Distribución de Conexiones: Se observan disparidades significativas en la 
infraestructura de Internet entre provincias, con Buenos Aires y Capital Federal mostrando la mejor conectividad.
Evolución de la Velocidad de Internet: La velocidad de Internet ha mejorado sustancialmente en los últimos años, 
especialmente a partir de 2019. Penetración de Internet: Alta en provincias urbanas, baja en áreas rurales.

4. KPIs Calculados:

Velocidad Media Nacional: 23.19 Mbps.
Penetración en Hogares: 52.16%.
Penetración en Población: 15.54%.
KPI Financiero - Internet Fijo: 4458.85 pesos por acceso.
KPI Financiero - Internet Móvil: 1665.16 pesos por acceso.

5. Conclusiones: 

El análisis revela una clara disparidad en la infraestructura de Internet entre provincias y una 
tendencia positiva en la mejora de la velocidad de descarga. Sin embargo, la penetración de Internet en la población
general es baja, destacando la necesidad de inversión en áreas menos desarrolladas.

6. Recomendaciones:

Inversión en infraestructura en provincias rezagadas.
Programas de subsidio para aumentar la adopción de servicios de Internet.
Monitoreo continuo del desempeño y optimización de servicios móviles.

7. Futuro del Proyecto: El análisis podría ampliarse para incluir comparativas internacionales, analizar el impacto
económico de la conectividad, o evaluar políticas públicas que promuevan la igualdad digital.