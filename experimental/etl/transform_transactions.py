import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import (
    current_timestamp, date_format, col,
    year, month, dayofmonth
)

# Leer argumentos
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'database_name', 'table_name'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Leer datos desde Glue Data Catalog (raw)
datasource = glueContext.create_dynamic_frame.from_catalog(
    database=args['database_name'],
    table_name=args['table_name']
)

# Convertir a DataFrame para transformaciones con Spark
df = datasource.toDF()

# Añadir timestamp de procesamiento
df = df.withColumn("processing_timestamp", current_timestamp())
df = df.withColumn("processing_date", date_format("processing_timestamp", "yyyy-MM-dd"))

# Validación ligera de columnas antes de aplicar transformaciones
required_columns = [
    "transaction_type", "energy_type", "quantity_kwh", "price_per_kwh", "transaction_date"
]

for col_name in required_columns:
    if col_name not in df.columns:
        raise Exception(f"Column '{col_name}' is missing from the source data.")

# Cast de columnas
df = df.withColumn("transaction_type", col("transaction_type").cast("string"))
df = df.withColumn("energy_type", col("energy_type").cast("string"))
df = df.withColumn("quantity_kwh", col("quantity_kwh").cast("double"))
df = df.withColumn("price_per_kwh", col("price_per_kwh").cast("double"))

# Calcular campo derivado total_amount
df = df.withColumn("total_amount", col("quantity_kwh") * col("price_per_kwh"))

# Extraer año, mes, día para particionar
df = df.withColumn("year", year(col("transaction_date")))
df = df.withColumn("month", month(col("transaction_date")))
df = df.withColumn("day", dayofmonth(col("transaction_date")))

# Convertir de nuevo a DynamicFrame
dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

# Guardar en S3 como Parquet particionado
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={
        "path": "s3://your-energy-trading-datalake/processed/transactions/",
        "partitionKeys": ["year", "month", "day"]
    },
    format="parquet"
)

job.commit()
