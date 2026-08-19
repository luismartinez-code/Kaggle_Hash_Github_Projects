from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class KnowledgeAgent:
    """Agent responsible for retrieval and grounded question answering."""

    supported_sources: List[str] = field(default_factory=lambda: ["documents", "embeddings", "graph"])

    def plan_retrieval(self, request: str) -> dict[str, object]:
        lowered = request.lower()
        source = "graph" if "relationship" in lowered or "network" in lowered else "documents"
        return {
            "agent": "knowledge_agent",
            "intent": "retrieval",
            "source": source,
            "recommended_tools": ["retrieval_tool", "observability_tool"],
        }
