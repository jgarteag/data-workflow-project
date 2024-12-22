# Proyecto de Flujo de Datos de Bienes Raíces
## Fuente de los Datos
Los datos utilizados en este proyecto provienen de [Kaggle](https://www.kaggle.com/datasets/0e23f01c0fc5a3d7a83e20023c70534df3cbbc6c23f1baf19f2ae3961a1576d7).

![ARQ](sources/arq.png)

## Objetivo
El objetivo de este proyecto es procesar y analizar datos de bienes raíces para generar un conjunto de datos final (`final_real_estate_insumo`) con columnas adicionales calculadas. Este conjunto de datos se utilizará para análisis y obtención de información.

## Preguntas a Abordar
- ¿Cuál es el precio promedio por pie cuadrado de las casas en diferentes ciudades?
- ¿Cómo varía el precio por habitación en diferentes estados?
- ¿Cuál es la distribución de las edades de las casas en el conjunto de datos?
- ¿Cómo se comparan los precios de las casas nuevas con las casas más antiguas?

## Elección del Modelo
El modelo elegido para este proyecto implica el uso de AWS Glue para operaciones ETL (Extracción, Transformación y Carga) y Apache Spark para el procesamiento de datos. Esta elección se hizo debido a la escalabilidad y flexibilidad de estas herramientas para manejar grandes conjuntos de datos y transformaciones complejas.

## Enfoque para Diferentes Escenarios

### Si los Datos se Incrementan en 100x
- **Escalabilidad**: Aprovechar la escalabilidad de AWS Glue y Spark aumentando el número de nodos de trabajo y utilizando particionamiento para manejar conjuntos de datos más grandes de manera eficiente.
- **Almacenamiento**: Utilizar Amazon S3 para almacenamiento escalable y considerar el uso de formatos de almacenamiento columnar como Parquet para consultas eficientes.

### Si las Tuberías se Ejecutan Diariamente en una Ventana de Tiempo Específica
- **Programación**: Utilizar AWS Glue Workflows y AWS Step Functions para programar y gestionar los trabajos ETL para que se ejecuten dentro de la ventana de tiempo especificada.
- **Procesamiento Incremental**: Implementar procesamiento de datos incremental para manejar actualizaciones diarias de datos de manera eficiente.

### Si la Base de Datos Necesita Ser Accedida por Más de 100 Usuarios Funcionales
- **Concurrencia**: Utilizar Amazon Redshift o Amazon Aurora para manejar alta concurrencia y proporcionar un rendimiento rápido en las consultas.
- **Caché**: Implementar mecanismos de caché utilizando Amazon ElastiCache para reducir la carga en la base de datos.

### Si se Requiere Hacer Analítica en Tiempo Real
- **Procesamiento en Tiempo Real**: Utilizar AWS Kinesis o Apache Kafka para la ingesta y procesamiento de datos en tiempo real.
- **Analítica de Streaming**: Implementar analítica de streaming utilizando Apache Spark Streaming o AWS Kinesis Data Analytics.

## Parámetros del Workflow
Las siguientes son las propiedades de ejecución predeterminadas para el workflow:

| Clave                  | Valor                                      |
|------------------------|--------------------------------------------|
| S3_BUCKET              | data-engineer-juanmgart                    |
| PATH_RAW_DATA          | rawData/housing_data/raw_data.parquet      |
| TABLE_NAME             | final_real_estate_insumo                   |
| DATABASE_NAME          | trusted_data                               |
| OUTPUT_TABLE_PATH_S3   | myownbucket-juanmgart/output               |
| GLUE_CATALOG           | AwsDataCatalog                             |

## Estructura del Proyecto
El script principal del proyecto es `DataWkflow-Job.py`, que incluye las siguientes funciones:
- `read_parquet_s3(bucket: str, key: str) -> DataFrame`: Lee un archivo Parquet desde S3.
- `data_cleaning(df: DataFrame) -> DataFrame`: Limpia los datos eliminando valores nulos y duplicados.
- `calculate_final_df(df: DataFrame) -> DataFrame`: Calcula columnas adicionales para el conjunto de datos final.
- `save_to_s3(df: DataFrame, bucket: str, key: str) -> None`: Guarda el conjunto de datos final en S3.

