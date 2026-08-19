# Remaining subagents and tools

This note defines the remaining specialist subagents and supporting tools for the platform.

## Subagents

### Data agent
Responsibility: choose connectors, inspect datasets, and prepare data for downstream analytics or ML tasks.

### ML agent
Responsibility: plan model training, evaluation, and deployment workflows.

### Knowledge agent
Responsibility: retrieve grounded information from documents, embeddings, or graph structures.

### Observability / ops agent
Responsibility: gather logs, traces, metrics, and incidents for reliability and governance.

## Core tool categories

- data tools: connector_tool, sql_query_tool
- BI tools: semantic_model_tool, dashboard_publish_tool, explain_results_tool
- ML tools: model_train_tool, evaluate_model_tool, deployment_tool
- knowledge tools: retrieval_tool
- operations tools: observability_tool

## Current scaffold
The repo now includes:
- a tool registry in [app/tools/registry.py](../../app/tools/registry.py)
- a data agent in [app/agents/data/data_agent.py](../../app/agents/data/data_agent.py)
- an ML agent in [app/agents/ml/ml_agent.py](../../app/agents/ml/ml_agent.py)
- a knowledge agent in [app/agents/knowledge/knowledge_agent.py](../../app/agents/knowledge/knowledge_agent.py)

These are intentionally lightweight placeholders that will be expanded into full tool adapters as the platform matures.
