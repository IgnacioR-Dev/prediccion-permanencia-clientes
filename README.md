# Prediccion-Churn-Telco

Este proyecto desarrolla un modelo de machine learning orientado a la detección y predicción de la permanencia de clientes en una empresa de telecomunicaciones. El objetivo principal es identificar patrones de comportamiento que permitan anticipar el riesgo de abandono (churn) y fortalecer estrategias de retención.

## Componentes del sistema

Puede variar según las necesidades del proyecto.

- Scripts de procesamiento: ingesta, validación, limpieza y transformación de datos.
- Base de datos PostgreSQL: para la carga y consulta estructurada de los datasets.
- Modelo de IA (scikit-learn): clasificación binaria para predicción de churn (continuidad o cancelación del servicio de telecomunicaciones).
- Metabase: dashboard de visualización de resultados.
- Documentación: diseño técnico completo + planificación.

## Estructura del repositorio

```
prediccion-churn-telco/
├── README.md
├── docs/
│   ├── G1_documento_justificacion_arquitectura_v1.pdf
│   ├── G1_documento_planificacion_proyecto_v1.pdf
│   └── G1_documento_diseño_tecnico_v1.1.0.pdf
├── src/
│   ├── data/
│   │   ├── 02_Base_Customer-Churn.csv
│   │   └── init.sql
│   ├── db/
│   │   └── conexion.py
│   ├── ml/
│   │   ├── pipeline/
│   │   │   ├── ingesta_datos.py
│   │   │   └── validador.py
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
├── .env
├── .gitignore
└── docker-compose.yml
```

## Cómo ejecutar el sistema

### Requisitos previos

* Docker y Docker Desktop instalados.
* Archivo `.env` configurado con las variables de entorno (ver sección -Variables de entorno- más abajo).
* Dependencias del proyecto instaladas - sigue las instrucciones a continuación:

¡Antes de instalar las dependencias, se recomienda crear un entorno virtual aislado para evitar conflictos con el sistema!

---
### Creación del entorno virtual 🐍:

#### 🪟 Windows

```bash
python -m venv venv
```

Activar entorno:

```bash
.\venv\Scripts\activate
```

Si aparece un error de permisos:

```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```
---

#### 🐧 Linux / macOS

```bash
python3 -m venv venv
```

Activar entorno:

```bash
source venv/bin/activate
```
---

### Instalación de dependencias 📦 

Con el entorno virtual activado:

```bash
pip install -r src/ml/requirements.txt
```

### Variables de entorno
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=db
DB_PORT=5432
DB_NAME=tu_nombre_bd
```

### Levantar el sistema
```bash
docker-compose up
```

Esto levantará automáticamente:
1. La base de datos PostgreSQL con la tabla `datos` creada.
2. El pipeline de ingesta que carga los 7043 registros del CSV.
3. Un reporte por consola con los resultados de la validación inicial de los datos (quality check).

### Bajar el sistema
```bash
docker-compose down
```

Para eliminar también los volúmenes de datos:
```bash
docker-compose down -v
```

## Pipeline implementado

### Etapa 1 — Ingesta de datos 
- Lectura del CSV `02_Base_Customer-Churn.csv`
- Renombrado de columnas al español
- Transformación de columnas booleanas (Yes/No → True/False)
- Carga a PostgreSQL en la tabla `datos`

### Etapa 1.5 - Validación inicial de datos mediante clase personalizada
- Definición de tipos de datos y dominios válidos por columna
- Validación de nulos, duplicados y consistencia de valores
- Detección de outliers en variables numéricas mediante IQR
- Cálculo de score de calidad por columna y global del dataset
- Generación de reporte detallado de calidad de datos

### Próximas etapas
- Etapa 2: Transformación de datos (se contempla feature engineering)
- Etapa 3: Entrenamiento del modelo
- Etapa 4: Visualización con Metabase

## Tecnologías utilizadas 

Puede ser modificado conforme las necesidades del proyecto:

- Python 3.12
- Pandas / Numpy / Scikit-learn
- PostgreSQL 15
- SQLAlchemy
- Docker / Docker Compose
- Git / GitHub
- Flask
- Render


## Documentación del proyecto

- [Justificación de Arquitectura (V1)](docs/G1_documento_justificacion_arquitectura_v1.pdf)
- [Planificación del Proyecto (V1)](docs/G1_documento_planificacion_proyecto_v1.pdf)
- [Diseño Técnico (V1)](docs/G1_documento_diseño_tecnico_v1.1.0.pdf)

## Equipo de desarrollo

- Ignacio Rodríguez
- Francisco Fierro
- Ronald Cerda

