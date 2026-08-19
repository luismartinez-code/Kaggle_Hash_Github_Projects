# Data products and datasets

This document maps common data products to recommended datasets, storage patterns, and architecture choices.

## 1. Data product categories

### A. Operational analytics
Purpose: monitor business activity and operational health.

Recommended datasets:
- transactional events
- customer activity logs
- order and fulfillment records
- support tickets
- service health metrics

Recommended storage:
- relational warehouse for core facts
- event tables for recent activity
- time-series store for metrics

Recommended architecture:
- batch + near-real-time ingestion
- BI agent for KPI exploration
- semantic layer for metrics and dimensions

### B. Customer 360
Purpose: create a unified view of customer behavior and value.

Recommended datasets:
- CRM profiles
- purchase history
- support interactions
- web/app telemetry
- marketing engagement events

Recommended storage:
- star schema or customer mart
- graph store for relationship mapping
- vector store for embeddings and similarity search

Recommended architecture:
- entity resolution pipeline
- graph-based knowledge layer
- recommendation and churn analysis agents

### C. Product analytics
Purpose: understand how users interact with products.

Recommended datasets:
- feature usage logs
- product events
- funnel events
- experiment results
- retention cohorts

Recommended storage:
- event warehouse
- feature store
- analytics tables

Recommended architecture:
- event streaming pipeline
- experiment analysis workflow
- BI and ML agents working together

### D. Financial intelligence
Purpose: support planning, forecasting, and exception analysis.

Recommended datasets:
- ledger transactions
- invoices and payments
- budgets and forecasts
- cash flow records
- exchange rate snapshots

Recommended storage:
- warehouse with financial dimensions
- historical archive store
- secure encrypted storage

Recommended architecture:
- governed reporting layer
- approval workflows for sensitive analyses
- forecasting and anomaly detection agents

### E. Supply chain and operations
Purpose: optimize logistics, inventory, and fulfillment.

Recommended datasets:
- inventory movements
- shipment events
- warehouse transfers
- supplier data
- incident logs

Recommended storage:
- operational data store
- warehouse for historical analysis
- time-series metrics store

Recommended architecture:
- streaming ingest for live status
- forecasting and root-cause analysis agents
- alerting and exception workflows

### F. Healthcare or regulated analytics
Purpose: support clinical, compliance, or operational decisions.

Recommended datasets:
- clinical records (where permitted)
- claims and billing data
- operational metrics
- audit logs
- consent and governance metadata

Recommended storage:
- secure governed warehouse
- access-controlled data lake
- immutable audit store

Recommended architecture:
- RBAC and data retention controls
- human-in-the-loop review for sensitive analysis
- approval and audit agents

## 2. Dataset patterns by workload

### Batch reporting workload
Best for: executive reporting, daily summaries, dashboards.

Dataset shape:
- aggregated fact tables
- daily and monthly partitions
- conformed dimensions

Architecture fit:
- warehouse-first design
- BI agent for natural language reporting

### Streaming analytics workload
Best for: live monitoring, anomaly detection, alerting.

Dataset shape:
- event streams
- rolling windows
- latest-state tables

Architecture fit:
- event-driven ingestion
- streaming processors
- monitoring and alerting agents

### Predictive analytics workload
Best for: churn, demand forecasting, fraud detection.

Dataset shape:
- labeled training data
- feature tables
- evaluation datasets

Architecture fit:
- feature store and model registry
- ML agent and evaluation workflow

### Search and retrieval workload
Best for: knowledge assistants and question-answering over documents.

Dataset shape:
- documents
- embeddings
- metadata and tags
- knowledge graph entities

Architecture fit:
- vector and graph retrieval
- RAG-style agent workflows

## 3. Recommended architecture by data product

| Data product | Primary datasets | Core storage | Best agent pattern |
|---|---|---|---|
| Operational analytics | transactions, events, service metrics | warehouse + time-series | BI agent + monitoring agent |
| Customer 360 | CRM, product usage, support, marketing events | warehouse + graph + vector | customer insight agent |
| Product analytics | usage events, funnels, experiments | event warehouse + feature store | BI + ML agent |
| Financial intelligence | ledger, invoices, budgets, forecasts | secure warehouse + archive | BI + approval agent |
| Supply chain | inventory, shipments, incidents | operational store + warehouse | forecasting + alert agent |
| Healthcare / regulated | claims, clinical data, audit logs | governed warehouse + audit store | compliance + BI agent |

## 4. How to optimize architecture for each dataset type

### Structured relational data
Best for:
- BI dashboards
- financial reporting
- sales and operations

Optimize by:
- using star schemas and conformed dimensions
- partitioning by date
- indexing the main join keys
- keeping semantic models simple

### Semi-structured data
Best for:
- logs
- JSON payloads
- clickstream data

Optimize by:
- storing raw and curated versions
- using schema-on-read or typed transformations
- keeping an event timeline for auditing

### Unstructured data
Best for:
- documents
- PDFs
- support conversations
- notes

Optimize by:
- chunking and embedding for retrieval
- storing metadata separately from content
- applying retrieval filters and access controls

### Graph data
Best for:
- relationship discovery
- influence analysis
- network and dependency mapping

Optimize by:
- modeling entities and relationships explicitly
- using graph traversal for explainability
- connecting graph results to BI and recommendation workflows

### Time-series data
Best for:
- telemetry
- forecasting
- anomaly detection

Optimize by:
- using high-cardinality partitioning
- storing rolling windows and aggregates
- pairing with forecasting and alerting agents

## 5. Recommended starter datasets for this prototype
For the current prototype, the most useful starter datasets are:
- sales transactions
- revenue events
- customer activity logs
- product usage events

These are sufficient to validate:
- BI reporting flows
- branch-based analysis workflows
- event-driven reasoning
- simple ML forecasting experiments
