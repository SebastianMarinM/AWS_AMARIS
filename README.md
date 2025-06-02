
# ⚡ Proyecto Data Lake para Comercialización de Energía

## 📌 Descripción General
Este proyecto implementa una arquitectura completa de Data Lake para una empresa comercializadora de energía utilizando AWS. Se ingieren archivos CSV desde sistemas operativos (clientes, proveedores, transacciones), se procesan con AWS Glue, se almacenan en S3 en múltiples zonas, se consultan mediante Athena y Redshift Spectrum, y se aplica gobernanza de datos con Lake Formation.

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
│ ├── raw/ # Archivos CSV originales
│ ├── processed/ # Datos Parquet transformados
│ └── curated/ # Datos listos para análisis
├── docs/ # Documentación y diagramas
│ ├── ARCHITECTURE.md
│ ├── QUICKSTART.md
│ └── technical_documentation.md
├── experimental/ # Scripts no usados en el pipeline final
│ ├── config/
│ ├── etl/
│ ├── scripts/
│ └── sql/
├── infrastructure/
│ ├── modules/ # Plantillas CloudFormation por servicio
│ └── environments/dev/ # Stack principal
├── scripts/
│ └── python/ # ETL oficial validado en AWS
│ ├── raw_to_processed.py
│ ├── processed_to_curated.py
│ └── athena_queries.py
├── test/ # Scripts de prueba y validación
├── README.md
└── requirements.txt

```

## 🚀 Guía de Despliegue

### Paso 1: Desplegar Infraestructura
```bash
# Buckets S3
aws cloudformation deploy --template-file infrastructure/cloudformation/modules/s3.yaml --stack-name datalake-s3

# Lake Formation y permisos
aws cloudformation deploy --template-file infrastructure/cloudformation/modules/lakeformation.yaml --stack-name datalake-lakeformation

# Recursos de Glue (jobs, crawlers, roles)
aws cloudformation deploy --template-file infrastructure/cloudformation/modules/glue.yaml --stack-name datalake-glue

# Clúster Redshift
aws cloudformation deploy --template-file infrastructure/cloudformation/modules/redshift.yaml --stack-name datalake-redshift
```

### Paso 2: Ejecutar ETL Jobs
Puedes ejecutarlos desde la consola de AWS o mediante trigger:
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

-- Consulta de ejemplo
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

## 📷 Validación, Evidencias y Mejoras Pendientes

- Todo el pipeline fue probado completamente en AWS.  
- La infraestructura fue desplegada exitosamente usando plantillas de **AWS CloudFormation**, incluyendo módulos para S3, Glue, Lake Formation y Redshift.
- Se validó que cada componente se ejecutara correctamente:
  - Glue Jobs completaron con éxito.
  - Athena ejecutó consultas sobre particiones correctamente.
  - Redshift Spectrum pudo consultar datos desde la zona `curated`.
- Se adjuntan imágenes de las ejecuciones en AWS Console en el documento entregado.
- 
- **Mejoras pendientes**:
  - Agregar control de duplicados en las zonas raw/processed.
  - Optimizar validaciones de calidad de datos.
  - Automatizar ejecución de pruebas unitarias para los ETL scripts.
  - Se inició el proceso para conectar el repositorio de **GitHub con AWS** con el objetivo de automatizar despliegues directamente desde el código fuente.  
  Aunque la integración no se completó, se documentó la intención y se dejó preparado el entorno para su futura implementación como una mejora de CI/CD.


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

