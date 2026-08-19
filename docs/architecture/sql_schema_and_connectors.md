# Starter SQL schema and connector interface

## 1. Starter SQL schema

```sql
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    day_of_week INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL
);

CREATE TABLE dim_customer (
    customer_id VARCHAR(64) PRIMARY KEY,
    customer_name VARCHAR(255),
    segment VARCHAR(64),
    region VARCHAR(128)
);

CREATE TABLE fact_sales (
    sale_id VARCHAR(64) PRIMARY KEY,
    date_id DATE NOT NULL,
    customer_id VARCHAR(64),
    amount DECIMAL(12, 2) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);

CREATE TABLE fact_revenue (
    revenue_id VARCHAR(64) PRIMARY KEY,
    date_id DATE NOT NULL,
    customer_id VARCHAR(64),
    revenue_amount DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(8) NOT NULL DEFAULT 'USD',
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);

CREATE TABLE fact_product_usage (
    usage_id VARCHAR(64) PRIMARY KEY,
    date_id DATE NOT NULL,
    customer_id VARCHAR(64),
    feature_name VARCHAR(128) NOT NULL,
    usage_count INT NOT NULL,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);
```

## 2. Connector interface

The connector interface is defined in [app/connectors/base.py](../..//app/connectors/base.py) and supports:

- configuration via `ConnectorConfig`
- connect / fetch / close lifecycle
- SQL and file-based implementations

### Example usage

```python
from app.connectors.base import ConnectorConfig
from app.connectors.sql_connector import SQLConnector

config = ConnectorConfig(name="analytics", connector_type="sql")
connector = SQLConnector(config)
connector.connect()
result = connector.fetch("SELECT * FROM fact_sales LIMIT 10")
print(result.rows)
connector.close()
```

## 3. Architecture fit

This schema and connector layer fit the current prototype because it provides:

- structured datasets for BI and forecasting use cases
- a reusable abstraction for future SQL, file, and cloud connectors
- a starter foundation for analytics agents and workflow orchestration
