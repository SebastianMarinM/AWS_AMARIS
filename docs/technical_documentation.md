# Documentación Técnica: Data Lake Comercialización de Energía

## 🧩 Descripción General
Este documento describe la arquitectura y componentes implementados en AWS para construir un Data Lake orientado a una comercializadora de energía. Se utilizó CloudFormation como IaC para el despliegue de la infraestructura.

---

## ⚙️ Glue Jobs
- Cada script ETL transforma archivos CSV en formato Parquet y los almacena particionados por fecha (`year/month/day`).
- Los Glue Jobs fueron configurados con triggers automáticos desde S3.
- `raw-to-processed`: Limpieza de columnas, tipos de datos, particionado y cambio de formato.
- `processed-to-curated`: Enriquecimiento y validación de datos.

---

## 🧾 Catálogo de Datos (Glue Data Catalog)
- Gestionado mediante Crawlers de Glue.
- Crawlers programados o manuales detectan esquemas en las zonas `raw`, `processed` y `curated`.
- Bases de datos separadas para cada capa (`energy_trading_raw_db`, `..._processed_db`, `..._curated_db`).

---

## 🏗️ Infraestructura CloudFormation
- `s3`: Buckets versionados para cada capa (`raw`, `processed`, `curated`).
- `glue`: Bases de datos, Crawlers, Jobs, Roles.
- `lakeformation`: Registro de ubicaciones, permisos y control de acceso.
- `athena`: Workgroups y ubicación de resultados en S3.
- `redshift`: Redshift Serverless, rol IAM y esquema externo con Glue Catalog.

---

## 🔍 Athena
- Consultas SQL ejecutadas directamente sobre los datos curados en S3.
- Integración opcional mediante script Python usando `boto3` y `AthenaClient`.

---

## 📊 Redshift (Spectrum)
- Redshift Serverless configurado para consultar directamente datos en S3 (sin copiar).
- Esquema externo creado con:
  ```sql
  CREATE EXTERNAL SCHEMA curated
  FROM data catalog
  DATABASE 'energy_trading_dev_db'
  IAM_ROLE 'arn:aws:iam::<account_id>:role/AmazonRedshift-CommandsAccessRole-...'
  CREATE EXTERNAL DATABASE IF NOT EXISTS;
