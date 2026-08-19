from __future__ import annotations

from dataclasses import dataclass

from app.agents.data.data_agent import DataAgent
from app.agents.knowledge.knowledge_agent import KnowledgeAgent
from app.agents.ml.ml_agent import MLAgent
from app.tools.registry import ToolRegistry


@dataclass
class RouterAgent:
    """Routes user requests to the appropriate specialist agents."""

    def route_request(self, request: str) -> dict[str, object]:
        text = request.lower()
        registry = ToolRegistry()

        if "sales" in text or "trend" in text or "quarter" in text or "report" in text:
            data_plan = DataAgent().plan_data_access(request)
            return {
                "intent": "business_intelligence",
                "agents": ["bi_agent", "data_agent"],
                "reason": "The request is about business analysis or reporting.",
                "subagent_plans": [data_plan],
                "tools": [tool.name for tool in registry.get_by_category("bi")],
            }

        if "train" in text or "classifier" in text or "predict" in text or "model" in text or "forecast" in text:
            ml_plan = MLAgent().plan_model_workflow(request)
            data_plan = DataAgent().plan_data_access(request)
            return {
                "intent": "machine_learning",
                "agents": ["ml_agent", "data_agent"],
                "reason": "The request requires machine learning workflow execution.",
                "subagent_plans": [ml_plan, data_plan],
                "tools": [tool.name for tool in registry.get_by_category("ml")],
            }

        if "relationship" in text or "document" in text or "knowledge" in text:
            knowledge_plan = KnowledgeAgent().plan_retrieval(request)
            return {
                "intent": "knowledge_retrieval",
                "agents": ["knowledge_agent"],
                "reason": "The request requires retrieval or grounded knowledge access.",
                "subagent_plans": [knowledge_plan],
                "tools": [tool.name for tool in registry.get_by_category("knowledge")],
            }

        return {
            "intent": "general",
            "agents": ["router_agent"],
            "reason": "No specialized intent was detected.",
            "subagent_plans": [],
            "tools": [tool.name for tool in registry.get_by_category("data")],
        }
