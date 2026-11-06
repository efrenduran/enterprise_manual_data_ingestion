# enterprise_manual_data_ingestion
Enterprise-grade data ingestion pipeline that automates data ingestion, transformation and validation workflows. Built to showcase best practices in data engineering, including orchestration, incremental loading, lineage, and analytics-ready data delivery.

## Arquitetura

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                INGESTION CONTROL LAYER                                       │
│                                                                                              │
│  Config Driven Framework                                                                     │
│  Control Tables                                                                              │
│  Watermark Management                                                                        │
│  Last Successful Load                                                                        │
│  Dynamic Scheduling                                                                          │
│  Retry Framework                                                                             │
│  Backfill Framework                                                                          │
│  SLA Management                                                                              │
│  Domain Ownership                                                                            │
│  Data Contracts                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   SOURCE SYSTEMS                                             │
│                                                                                              │
│  Azure Blob │ SFTP │ APIs │ SharePoint │ Vendor Files │ Event Streams │ Kafka │ SAP          │
│  Salesforce │ Oracle │ SQL Server │ CSV │ JSON │ XML │ Parquet │ CDC Sources                 │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  LANDING / DROP ZONE                                         │
│                                                                                              │
│  Original Files                                                                              │
│  Immutable Storage                                                                           │
│  File Versioning                                                                             │
│  Archive Retention                                                                           │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 FILE VALIDATION GATE                                         │
│                                                                                              │
│  Filename Validation                                                                         │
│  File Size Validation                                                                        │
│  Checksum Validation                                                                         │
│  Duplicate Detection                                                                         │
│  Compression Validation                                                                      │
│  Encoding Validation                                                                         │
│  Header Validation                                                                           │
│  Delimiter Validation                                                                        │
│  Record Count Validation                                                                     │
│  Schema Drift Detection                                                                      │
│  Data Contract Validation                                                                    │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                             STAGING / PRE-PROCESSING LAYER                                   │
│                                                                                              │
│  Databricks Processing                                                                       │
│  ZIP Extraction                                                                              │
│  File Inventory                                                                              │
│  Metadata Collection                                                                         │
│  Source Profiling                                                                            │
│  Technical Lineage Generation                                                                │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                             METADATA & LINEAGE CAPTURE                                       │
│                                                                                              │
│  Source Metadata                                                                             │
│  Load Metadata                                                                               │
│  Column Metadata                                                                             │
│  Dataset Registration                                                                        │
│  OpenLineage Integration                                                                     │
│  Purview / Unity Catalog Registration                                                        │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   RAW LAYER (L0)                                             │
│                                                                                              │
│  Immutable Copy                                                                              │
│  Full History Preservation                                                                   │
│                                                                                              │
│  Technical Columns                                                                           │
│    ingestion_id                                                                              │
│    batch_id                                                                                  │
│    ingestion_timestamp                                                                       │
│    source_file                                                                               │
│    source_system                                                                             │
│    source_row_number                                                                         │
│    record_hash                                                                               │
│    processing_timestamp                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     MACRO DQ LAYER                                           │
│                                                                                              │
│  Historical Volume Comparison                                                                │
│  Missing File Detection                                                                      │
│  Unexpected Growth Detection                                                                 │
│  Unexpected Reduction Detection                                                              │
│  SLA Compliance                                                                              │
│  Source vs Target Reconciliation                                                             │
│  Statistical Distribution Validation                                                         │
│  Anomaly Detection                                                                           │
│  Freshness Validation                                                                        │
│  Timeliness Validation                                                                       │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     MICRO DQ LAYER                                           │
│                                                                                              │
│  Not Null                                                                                    │
│  Unique                                                                                      │
│  Accepted Values                                                                             │
│  Regex                                                                                       │
│  Data Type Validation                                                                        │
│  Date Validation                                                                             │
│  Referential Integrity                                                                       │
│  Cross Table Validation                                                                      │
│  Business Rules                                                                              │
│  Great Expectations Rules                                                                    │
│  DQ Scoring                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                           ┌────────────────────┴────────────────────┐
                           ▼                                         ▼

             ┌──────────────────────────────┐       ┌──────────────────────────────┐
             │         QUARANTINE           │       │          VALID DATA          │
             │                              │       │                              │
             │ Invalid Data                 │       │ Approved Records             │
             │ Rejected Rows                │       │ DQ Passed                    │
             │ Error Classification         │       │ Ready For Processing         │
             │ Reprocessing Queue           │       │                              │
             └──────────────────────────────┘       └──────────────────────────────┘
                                                                 │
                                                                 ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                CDC / INCREMENTAL ENGINE                                      │
│                                                                                              │
│  Watermark Processing                                                                        │
│  Last Load Retrieval                                                                         │
│  Incremental Filter                                                                          │
│  CDC Processing                                                                              │
│  Hash Comparison                                                                             │
│  Delta Detection                                                                             │
│  Insert Detection                                                                            │
│  Update Detection                                                                            │
│  Delete Detection                                                                            │
│  Idempotency Enforcement                                                                     │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   CURATED LAYER (L1)                                         │
│                                                                                              │
│  Type Casting                                                                                │
│  Deduplication                                                                               │
│  Standardization                                                                             │
│  Business Naming                                                                             │
│  Cleansing                                                                                   │
│  Surrogate Key Generation                                                                    │
│  Domain Segregation                                                                          │
│  Data Product Creation                                                                       │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                            BUSINESS ENRICHMENT LAYER (L2)                                    │
│                                                                                              │
│  Customer Join                                                                               │
│  Product Join                                                                                │
│  Calendar Join                                                                               │
│  Geographic Join                                                                             │
│  Financial Join                                                                              │
│  Reference Data Integration                                                                  │
│  MDM Matching                                                                                │
│  Golden Record Resolution                                                                    │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                HISTORICAL MANAGEMENT                                         │
│                                                                                              │
│  SCD Type 1                                                                                  │
│  SCD Type 2                                                                                  │
│  SCD Type 3                                                                                  │
│  Effective Dating                                                                            │
│  Version Control                                                                             │
│  Temporal Tables                                                                             │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                              RECONCILIATION FRAMEWORK                                        │
│                                                                                              │
│  Source Count vs Target Count                                                                │
│  Control Totals                                                                              │
│  Financial Balancing                                                                         │
│  Revenue Validation                                                                          │
│  Completeness Validation                                                                     │
│  Multi-Hop Reconciliation                                                                    │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 BUSINESS DATA MARTS                                          │
│                                                                                              │
│  Fact Tables                                                                                 │
│  Dimensions                                                                                  │
│  KPI Aggregations                                                                            │
│  Semantic Models                                                                             │
│  Data Products                                                                               │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
                                                │
                                                ▼

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  ANALYTICS CONSUMPTION                                       │
│                                                                                              │
│  Power BI                                                                                    │
│  Tableau                                                                                     │
│  Executive Dashboards                                                                        │
│  Self-Service Analytics                                                                      │
│  Machine Learning                                                                            │
│  Feature Store                                                                               │
│  Reverse ETL                                                                                 │
└──────────────────────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
OBSERVABILITY
═══════════════════════════════════════════════════════════════════════════════

Pipeline Health
Execution Time
Rows Processed
Failed Records
Cost Per Run
Resource Consumption
SLA Monitoring
DQ Trend Monitoring

═══════════════════════════════════════════════════════════════════════════════
DATA GOVERNANCE
═══════════════════════════════════════════════════════════════════════════════

Data Catalog
Business Glossary
Data Stewardship
Data Ownership
Data Classification
Certification
Lineage

═══════════════════════════════════════════════════════════════════════════════
SECURITY & PRIVACY
═══════════════════════════════════════════════════════════════════════════════

RBAC
ABAC
Secrets Management
PII Discovery
PII Masking
Column Encryption
Row Level Security
Data Retention Policies

═══════════════════════════════════════════════════════════════════════════════
METRICS & KPIs
═══════════════════════════════════════════════════════════════════════════════

DQ Score
Freshness Score
Completeness Score
Pipeline Reliability
Mean Time To Recovery
SLA Compliance
Cost Efficiency

═══════════════════════════════════════════════════════════════════════════════
ALERTING & INCIDENT MANAGEMENT
═══════════════════════════════════════════════════════════════════════════════

Teams Alerts
Slack Alerts
Email Alerts
PagerDuty
On-Call Escalation
Auto Ticket Creation

═══════════════════════════════════════════════════════════════════════════════
AUTOMATED RECOVERY FRAMEWORK
═══════════════════════════════════════════════════════════════════════════════

Auto Retry
Auto Reprocessing
Backfill Framework
Checkpoint Recovery
Replay Failed Loads
Disaster Recovery

═══════════════════════════════════════════════════════════════════════════════
DATA MESH ENABLEMENT
═══════════════════════════════════════════════════════════════════════════════

Domain-Oriented Data Products
Federated Governance
Self-Service Platform
Cross-Domain Contracts
Domain Ownership