# Deep Agent Platform Prototype

This workspace now contains a working scaffold for a multi-agent platform inspired by the system design notes and the vibecode-style layered architecture.

## Current implementation
- A router agent that classifies requests into business intelligence or machine learning intents.
- A dedicated BI agent with environment-aware planning and query generation.
- BI tool abstractions for Power BI, Tableau, Looker, and Qlik.
- A workflow graph runner with branching, concurrency, summarization, and tuning-point output.
- A lightweight HTTP API entrypoint for routing and workflow execution.
- A test suite covering the router, BI agent, workflow graph, and API surface.

## Current status versus the system design
The implementation now covers the core agent orchestration layer and the BI workflow layer from the design notes. The next major gaps are:
1. A data connector layer for real warehouse and file sources.
2. An ML agent and model-training workflow.
3. Evaluation, observability, and governance hooks.
4. Deployment scaffolding for Docker/Kubernetes or cloud-based hosting.

## Architecture guidance
For the phased implementation plan and the recommended repository structures for different application types and environments, see [docs/architecture/implementation_blueprints.md](docs/architecture/implementation_blueprints.md).

For dataset-oriented architecture guidance, including recommended datasets and storage patterns for different data products, see [docs/architecture/data_product_datasets.md](docs/architecture/data_product_datasets.md).

For the starter SQL schema and connector abstraction that support the current prototype, see [docs/architecture/sql_schema_and_connectors.md](docs/architecture/sql_schema_and_connectors.md).

For the remaining subagents and tool registry scaffolding, see [docs/architecture/subagents_and_tools.md](docs/architecture/subagents_and_tools.md).

## How to run
- Run the test suite:
  - `python -m unittest discover -s tests -v`
- Start the API server:
  - `python -m app.api`
