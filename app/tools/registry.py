from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List


@dataclass(frozen=True)
class ToolSpec:
    """Describes a callable tool available to agents."""

    name: str
    description: str
    category: str


class ToolRegistry:
    """Registry of built-in tools for the agent platform."""

    def __init__(self) -> None:
        self._tools: Dict[str, ToolSpec] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        self.register(ToolSpec("sql_query_tool", "Run SQL queries against a connected data source.", "data"))
        self.register(ToolSpec("semantic_model_tool", "Inspect or build semantic model definitions.", "bi"))
        self.register(ToolSpec("dashboard_publish_tool", "Publish a report or dashboard to a BI environment.", "bi"))
        self.register(ToolSpec("explain_results_tool", "Explain computed metrics and findings.", "bi"))
        self.register(ToolSpec("connector_tool", "Load data through a connector abstraction.", "data"))
        self.register(ToolSpec("model_train_tool", "Train a model from a prepared dataset.", "ml"))
        self.register(ToolSpec("evaluate_model_tool", "Evaluate model quality and performance.", "ml"))
        self.register(ToolSpec("deployment_tool", "Deploy a model or application artifact.", "ml"))
        self.register(ToolSpec("retrieval_tool", "Search documents or embeddings for grounded answers.", "knowledge"))
        self.register(ToolSpec("observability_tool", "Collect logs, metrics, and traces for monitoring.", "ops"))

    def register(self, tool: ToolSpec) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)

    def list_tools(self) -> List[ToolSpec]:
        return list(self._tools.values())

    def get_by_category(self, category: str) -> List[ToolSpec]:
        return [tool for tool in self.list_tools() if tool.category == category]
