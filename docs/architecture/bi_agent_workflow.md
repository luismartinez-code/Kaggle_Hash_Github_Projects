# BI Agent Workflow Evaluation

## Recommendation
Use a hybrid design:
- a simple chain for deterministic BI tasks such as intent detection, metric extraction, query generation, and result explanation
- a graph for more complex business workflows that require branching, retries, approvals, or multi-source reasoning

This is the best fit for the current platform because the BI agent needs both predictable execution and flexible orchestration.

## Why a chain is useful
A chain is appropriate when the task flow is mostly linear:
1. receive request
2. detect intent
3. select environment and dialect
4. generate query or semantic model plan
5. execute query
6. explain results

Benefits:
- easy to test
- easier to debug
- deterministic outputs for common business questions
- low operational overhead

## Why a graph is useful
A graph is appropriate when the workflow can branch based on context:
- if data source is SQL, route to SQL query generation
- if data source is semantic model, route to semantic layer tooling
- if the request is ambiguous, ask for clarification
- if the result is incomplete, trigger a retry or fallback agent
- if the request requires finance, operations, and sales context, combine multiple agent paths

Benefits:
- supports conditional execution
- handles retries and fallbacks
- allows multi-agent collaboration
- scales better as the platform grows

## Proposed graph structure
### Nodes
- RouterNode
  - classifies the request into BI, ML, or general intent
- ContextNode
  - gathers metadata such as environment, dialect, dataset, and filters
- PlanningNode
  - extracts metrics, dimensions, and desired outputs
- ExecutionNode
  - generates and runs the relevant query or semantic model request
- ValidationNode
  - checks for missing context or invalid output
- ExplanationNode
  - summarizes findings for the end user
- EscalationNode
  - routes to a human review or a specialized agent when confidence is low

### Edges
- RouterNode -> ContextNode
- ContextNode -> PlanningNode
- PlanningNode -> ExecutionNode
- ExecutionNode -> ValidationNode
- ValidationNode -> ExplanationNode
- ValidationNode -> EscalationNode (on failure or ambiguity)

## Suggested implementation style
Use a graph engine such as:
- LangGraph for Python-based orchestration
- Semantic Kernel for a more structured agent workflow
- custom lightweight graph runner if the initial scope remains small

For the initial version, keep the graph small and implement the transitions explicitly in code.

## Recommended decision
For this project:
- implement the first version as a chain for core BI tasks
- add graph-style branching once the workflow needs retries, clarifications, or multi-tool orchestration

## Practical architecture for this repo
### Phase 1: chain-based MVP
- RouterAgent -> BIAgent -> BITools
- deterministic flow for analytics questions
- unit tests around each step

### Phase 2: graph-based expansion
- add a workflow orchestrator that can branch between:
  - SQL query generation
  - semantic model generation
  - dashboard publishing
  - explanation and review

## Design principles
- keep deterministic steps explicit
- use graph orchestration only where branching is required
- preserve traceability for each node
- support human-in-the-loop approvals for sensitive reports

## Summary
A chain is better for the initial BI MVP, while a graph is better for enterprise-scale orchestration. The right approach is a hybrid: chain for the common path, graph for the exceptional path.
