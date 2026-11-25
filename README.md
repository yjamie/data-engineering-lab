# Data Engineering Lab
End to end data pipeline in Python with multiple connectors

# High-level Architecture

1. Data Sources
   2. API
   3. Flat files
2. Python Ingestion Layer
   3. Connectors: API and flat files
   4. Extraction
   5. Pagination
   6. Validation
3. Data warehouse
   4. Raw (raw) - raw tables loaded by Python
4. dbt Transformation Layer
   5. Staging (stg) - one model per source table
   6. Intermediate (int) - combines multiple staging models
   7. Marts (dim, fct) - business-oriented datasets
5. Analytics database
6. Consumption

