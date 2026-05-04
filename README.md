# FondosSMV-Project

Pipeline de datos end-to-end para análisis de fondos mutuos y de inversión peruanos, usando datos públicos de la Superintendencia del Mercado de Valores (SMV).

## Sobre el proyecto

Proyecto de portafolio que demuestra el ciclo completo de análisis de datos aplicado al sector financiero peruano:

- **Extracción** automatizada desde la API pública de la SMV
- **Almacenamiento** en SQL Server con modelo de snapshots mensuales para análisis de series de tiempo
- **Transformación** mediante vistas analíticas en T-SQL
- **Visualización** interactiva en Power BI

El caso de estudio principal es Credicorp Capital S.A. Sociedad Administradora de Fondos.

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Extracción | Python 3.10+, requests, pandas |
| Almacenamiento | SQL Server, T-SQL |
| Conexión | pyodbc |
| Visualización | Power BI Desktop, DAX |

## Arquitectura del pipeline

```
API SMV (JSON)
     ↓
Python (extracción + limpieza)
     ↓
SQL Server (snapshots mensuales)
     ↓
Vistas analíticas T-SQL
     ↓
Power BI (dashboards interactivos)
```

## Estructura del repositorio

```
FondosSMV-Project/
├── src/                 # Scripts Python de extracción y carga
├── sql/                 # DDL y vistas analíticas
├── powerbi/             # Archivo .pbix del dashboard
├── docs/                # Documentación e imágenes
└── data/                # Datos de muestra
```
