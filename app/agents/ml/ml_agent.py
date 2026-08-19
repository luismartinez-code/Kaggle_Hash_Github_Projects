from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class MLAgent:
    """Agent responsible for preparing, training, and evaluating models."""

    supported_tasks: List[str] = field(default_factory=lambda: ["classification", "forecasting", "regression"])

    def plan_model_workflow(self, request: str) -> dict[str, object]:
        lowered = request.lower()
        task = "forecasting" if "forecast" in lowered else "classification"
        return {
            "agent": "ml_agent",
            "intent": "model_workflow",
            "task": task,
            "recommended_tools": ["model_train_tool", "evaluate_model_tool", "deployment_tool"],
        }
