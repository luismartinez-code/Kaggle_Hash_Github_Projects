from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BIContext:
    """Runtime context for business intelligence work."""

    source_type: str = "sql"
    dialect: str = "postgresql"
    environment: str = "desktop"
    dataset_name: Optional[str] = None
    metrics: List[str] = field(default_factory=list)
    filters: List[str] = field(default_factory=list)


@dataclass
class BIAgent:
    """A BI agent that can plan reports, generate queries, and explain results."""

    context: BIContext = field(default_factory=BIContext)

    def plan_report(self, request: str) -> dict[str, object]:
        text = request.lower()
        metrics = []

        if "sales" in text:
            metrics.append("sales")
        if "revenue" in text:
            metrics.append("revenue")
        if "profit" in text:
            metrics.append("profit")
        if "customer" in text:
            metrics.append("customers")

        if not metrics:
            metrics = ["overview"]

        return {
            "intent": "report_generation",
            "metrics": metrics,
            "source_type": self.context.source_type,
            "dialect": self.context.dialect,
            "environment": self.context.environment,
            "suggested_tools": [
                "sql_query_tool",
                "semantic_model_tool",
                "dashboard_publish_tool",
                "explain_results_tool",
            ],
        }

    def generate_query(self, request: str) -> str:
        base = "SELECT * FROM analytics_fact_table"
        if "sales" in request.lower():
            return "SELECT date, SUM(sales) AS sales FROM sales_fact GROUP BY date ORDER BY date"
        if "revenue" in request.lower():
            return "SELECT date, SUM(revenue) AS revenue FROM revenue_fact GROUP BY date ORDER BY date"
        return base

    def adapt_for_environment(self, environment: str, dialect: str) -> dict[str, str]:
        return {
            "environment": environment,
            "dialect": dialect,
            "notes": "Use the appropriate driver and syntax for the selected BI environment.",
        }
