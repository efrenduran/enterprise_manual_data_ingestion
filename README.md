# enterprise_manual_data_ingestion
Enterprise-grade data ingestion pipeline that automates data ingestion, transformation and validation workflows. Built to showcase best practices in data engineering, including orchestration, incremental loading, lineage, and analytics-ready data delivery.

## Arquitetura

```text
Azure Blob Storage
        │
        ▼
Airflow Sensor
        │
        ▼
Databricks - Decompress ZIP
        │
        ▼
Databricks - Load CSV
        │
        ▼
Snowflake Raw Layer
        │
        ▼
dbt Transformations
        │
        ▼
Analytics Layer