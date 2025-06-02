# Arquitectura del Data Lake para Comercializadora de Energía

## Descripción General
Este documento describe la arquitectura completa del sistema de Data Lake implementado para la comercializadora de energía, incluyendo todos los componentes, flujos de datos, recursos desplegados con CloudFormation y consideraciones de seguridad.

![Arquitectura](./diagrams/architecture.png)

## Componentes Principales

### 1. Capa de Almacenamiento (S3)

#### Raw Zone (Bronze)
- **Propósito**: Almacenamiento de datos crudos en formato CSV.
- **Estructura**:
  ```
  s3://energy-trading-datalake-dev/raw/
  ├── providers/
  ├── clients/
  └── transactions/
  ```
- **Retención**: 90 días

#### Processed Zone (Silver)
- **Propósito**: Almacena datos transformados y validados en formato Parquet.
- **Optimizaciones**:
  - Compresión Snappy
  - Particionamiento por fecha (año/mes/día)

#### Curated Zone (Gold)
- **Propósito**: Datos agregados para análisis.
- **Formato**: Parquet optimizado para Athena

### 2. Procesamiento de Datos

#### AWS Glue

- **Crawlers**:
  - `raw-data-crawler`: Detecta esquemas en zona raw
  - `processed-data-crawler`: Detecta esquemas en zona processed

- **Jobs ETL**:
  1. `raw-to-processed`: Limpieza básica, conversión a Parquet, particionado
  2. `processed-to-curated`: Agregación y KPIs
  3. `curated-to-redshift` : Carga incremental a Redshift

#### Lake Formation
- Catálogo centralizado
- Permisos gestionados con `LakeFormation::Permissions`

### 3. Análisis y Consulta

#### Athena
- Workgroups: `analysts`, `reporting`, `data-science`
- Consultas vía script Python con `boto3`

#### Amazon Redshift
- Carga desde zona curated
- Conexión JDBC definida en CloudFormation

### 4. Seguridad y Monitoreo

- IAM Roles mínimos necesarios
- S3 cifrado con SSE-KMS
- TLS en tránsito
- Logs activados:
  - S3 Access Logs
  - CloudTrail
  - Lake Formation Audit

## Infraestructura como Código

Todo el entorno se despliega con CloudFormation:
- Buckets S3
- Glue Crawlers y Jobs
- Bases de datos Glue
- Workgroups de Athena
- Roles IAM
- Lake Formation
- Conexión JDBC
- Redshift (opcional)

## Pipeline de Datos (Resumen)

1. Sistema transaccional exporta CSV → S3
2. Crawler detecta esquema y lo registra
3. Glue Job `raw-to-processed` transforma
4. Glue Job `processed-to-curated` agrega y optimiza
5. Crawler actualiza Catálogo
6. Athena consulta y Redshift carga final
