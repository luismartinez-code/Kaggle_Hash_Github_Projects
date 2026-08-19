from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class DataAgent:
    """Agent responsible for data access planning and connector selection."""

    supported_sources: List[str] = field(default_factory=lambda: ["sql", "file", "api"])

    def plan_data_access(self, request: str) -> dict[str, object]:
        lowered = request.lower()
        source = "sql" if "sql" in lowered or "warehouse" in lowered else "file"
        return {
            "agent": "data_agent",
            "intent": "data_access",
            "source": source,
            "recommended_tools": ["connector_tool", "sql_query_tool"],
        }
