
# ⚡ Proyecto Data Lake para Comercialización de Energía

## 📌 Descripción General
Este proyecto implementa una arquitectura completa de Data Lake para una empresa comercializadora de energía utilizando AWS. Se ingieren archivos CSV desde sistemas operativos (clientes, proveedores, transacciones), se procesan con AWS Glue, se almacenan en S3 en múltiples zonas, se consultan mediante Athena y Redshift, y se aplica gobernanza de datos con Lake Formation.

## 📐 Arquitectura
El pipeline sigue una arquitectura en capas:

- **Zona Raw**: Archivos CSV originales ingeridos desde los sistemas fuente, particionados por fecha de carga.
- **Zona Procesada**: Datos convertidos a formato Parquet con validación básica y particionados por año/mes/día.
- **Zona Curada**: Conjuntos de datos limpios y deduplicados optimizados para analítica.
- **Acceso Analítico**:
  - **Amazon Athena**: Consultas SQL directas sobre datos en S3.
  - **Amazon Redshift Spectrum**: Consultas externas sobre datos curados vía Glue Catalog.

## 🛠 Tecnologías Utilizadas
- `Amazon S3`: Almacenamiento del Data Lake
- `AWS Glue`: ETL (Jobs + Crawlers + Catálogo)
- `Amazon Athena`: Motor de consultas serverless sobre S3
- `Amazon Redshift`: Data Warehouse + Spectrum
- `AWS Lake Formation`: Gobernanza de datos y permisos
- `AWS CloudFormation`: Infraestructura como Código (IaC)
- `Python (boto3, pandas)`: Orquestación y scripts analíticos

## 📁 Estructura del Proyecto
```
AWS_AMARIS/
├── data/
│   ├── raw/
│   ├── processed/
│   └── curated/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── QUICKSTART.md
│   └── technical_documentation.md
├── experimental/
│   ├── config/
│   ├── etl/
│   ├── scripts/
│   └── sql/
├── infrastructure/
│   ├── modules/
│   └── environments/dev/
├── scripts/
│   └── python/
│       ├── raw_to_processed.py
│       ├── processed_to_curated.py
│       └── athena_queries.py
├── test/
├── README.md
└── requirements.txt
```

## 📦 Instalación de dependencias

Antes de ejecutar los scripts, asegúrate de instalar las librerías necesarias con:

```bash
pip install -r requirements.txt
```

## 🚀 Guía de Despliegue

### Paso 1: Desplegar Infraestructura
```bash
aws cloudformation deploy --template-file infrastructure/cloudformation/modules/s3.yaml --stack-name datalake-s3
aws cloudformation deploy --template-file infrastructure/cloudformation/modules/lakeformation.yaml --stack-name datalake-lakeformation
aws cloudformation deploy --template-file infrastructure/cloudformation/modules/glue.yaml --stack-name datalake-glue
aws cloudformation deploy --template-file infrastructure/cloudformation/modules/redshift.yaml --stack-name datalake-redshift
```

### Paso 2: Ejecutar ETL Jobs
- `raw_to_processed.py`: Convierte CSV a Parquet y particiona por fecha.
- `processed_to_curated.py`: Limpia, deduplica y escribe datos curados.

### Paso 3: Actualizar Catálogo de Glue
```bash
# Ejecutar crawlers o configurar triggers luego de cada ETL
```

### Paso 4: Consultar con Athena
Usa el script `athena_queries.py` para:
- Agregar energía vendida por tipo
- Obtener los principales clientes por consumo
- Evaluar desempeño de proveedores

### Paso 5: Redshift Spectrum
```sql
CREATE EXTERNAL SCHEMA curated
FROM data catalog
DATABASE 'energy_trading_curated_db'
IAM_ROLE 'arn:aws:iam::ACCOUNT_ID:role/RedshiftSpectrumRole'
CREATE EXTERNAL DATABASE IF NOT EXISTS;

SELECT * FROM curated.clients LIMIT 10;
```

## ✅ Funcionalidades Implementadas
- ✅ Estructura en S3 con múltiples zonas y datos particionados
- ✅ Jobs de Glue con conversión de formato y particionado
- ✅ Crawlers y Catálogo de Glue por zona (`raw`, `processed`, `curated`)
- ✅ Integración con Athena vía Python (`boto3`)
- ✅ Integración con Redshift Spectrum
- ✅ Infraestructura como código con CloudFormation modular
- ✅ Roles IAM y políticas de acceso refinado a S3

## 🔒 Seguridad y Gobernanza
- Encriptación en S3 (por defecto)
- Control de acceso granular con Lake Formation
- Roles IAM para Glue, Redshift y Athena
- Particionado de datos para reducir costos de consulta

## 🧪 Pruebas
Validaciones aplicadas en scripts de transformación:
- Eliminación de registros nulos
- Deduplicación por campos clave
- Creación y verificación de particiones en S3

## 🔍 Pruebas Unitarias
El proyecto incluye una carpeta `test/` que agrupa pruebas automatizadas diseñadas como soporte adicional para validar funcionalidades críticas del pipeline:

- `test_athena_queries.py`: Simula la ejecución de una consulta en Athena usando `boto3` con mocks.
- `test_data_validation.py`: Prueba la validación de esquemas en DataFrames.
- `test_etl_jobs.py`: Valida una transformación básica con Spark.
- `conftest.py`: Define fixtures reutilizables.

> Nota: Se eliminó `test_utils.py` por no aportar validación funcional real.

## 📷 Validación, Evidencias y Mejoras Pendientes
- El pipeline fue probado completamente en AWS.
- La infraestructura fue desplegada exitosamente con CloudFormation.
- Se validaron Glue Jobs, consultas Athena y Redshift Spectrum.
- Se adjuntan capturas de evidencia en el documento entregado.

**Mejoras pendientes**:
- Control de duplicados en zona raw/processed.
- Validaciones más robustas.
- Automatizar pruebas unitarias.
- Integración CI/CD entre GitHub y AWS (entorno preparado, aún no conectado).

  ## 🧪 Carpeta `experimental/` (antes `src/`)

Durante el desarrollo del proyecto, se creó una carpeta con el nombre original `src/` que contenía scripts, transformaciones y utilidades desarrolladas como parte del proceso exploratorio y técnico.

Esta carpeta fue renombrada como `experimental/` para reflejar su propósito real: agrupar componentes que **no fueron utilizados directamente en el pipeline desplegado con CloudFormation**, pero que sirvieron para:

- Probar transformaciones modulares por dataset (`transform_customers.py`, `transform_providers.py`, etc.).
- Generar datos de ejemplo (`generate_sample_data.py`).
- Explorar consultas y vistas SQL (`analysis_queries.sql`, `create_views.sql`).
- Crear utilidades reusables para fechas, logs y S3 (`utils/`).

Debido a que el pipeline final fue **validado directamente en AWS como infraestructura desplegada por CloudFormation**, estos componentes **no fueron necesarios en la ejecución oficial**, pero reflejan el análisis previo y el soporte técnico realizado durante el desarrollo del proyecto.

Se decidió conservar esta carpeta para documentar el proceso completo y mantener trazabilidad del trabajo exploratorio realizado.

## 📄 Licencia
Licencia MIT
