from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Union
import copy
import concurrent.futures
import time

from app.agents.data.data_agent import DataAgent
from app.agents.knowledge.knowledge_agent import KnowledgeAgent
from app.agents.ml.ml_agent import MLAgent
from app.tools.registry import ToolRegistry


@dataclass
class WorkflowNode:
    name: str
    handler: Callable[[dict], dict]


@dataclass
class WorkflowGraph:
    nodes: Dict[str, WorkflowNode] = field(default_factory=dict)
    edges: Dict[str, List[str]] = field(default_factory=dict)

    def add_node(self, name: str, handler: Callable[[dict], dict]) -> None:
        self.nodes[name] = WorkflowNode(name=name, handler=handler)
        self.edges.setdefault(name, [])

    def add_edge(self, source: str, target: str) -> None:
        self.edges.setdefault(source, []).append(target)

    def run(self, start_node: str, initial_state: Optional[dict] = None) -> dict:
        state = initial_state or {}
        current = start_node
        visited = []

        while current in self.nodes:
            visited.append(current)
            state = self.nodes[current].handler(state)
            next_nodes = self.edges.get(current, [])
            if not next_nodes:
                break

            next_node = state.get("next_node")
            if next_node in self.nodes:
                current = next_node
            else:
                current = next_nodes[0]

        state["visited_nodes"] = visited
        return state


class GraphRunner:
    """Simple graph runner for BI workflows with scenario-based and parallel branches."""

    def __init__(self) -> None:
        self.graph = WorkflowGraph()
        self._register_default_nodes()

    def _register_default_nodes(self) -> None:
        self.graph.add_node("router", self._router_handler)
        self.graph.add_node("context", self._context_handler)
        self.graph.add_node("plan", self._plan_handler)
        self.graph.add_node("execute", self._execute_handler)
        self.graph.add_node("validate", self._validate_handler)
        self.graph.add_node("explain", self._explain_handler)
        self.graph.add_node("escalate", self._escalate_handler)

        self.graph.add_edge("router", "context")
        self.graph.add_edge("context", "plan")
        self.graph.add_edge("plan", "execute")
        self.graph.add_edge("execute", "validate")
        self.graph.add_edge("validate", "explain")
        self.graph.add_edge("validate", "escalate")

    def _router_handler(self, state: dict) -> dict:
        request = str(state.get("request", "")).lower()
        registry = ToolRegistry()
        state["tool_names"] = [tool.name for tool in registry.list_tools()]

        if "train" in request or "predict" in request or "forecast" in request:
            state["intent"] = "machine_learning"
            state["subagent_plans"] = [MLAgent().plan_model_workflow(str(state.get("request", "")))]
            state["tool_names"] = [tool.name for tool in registry.get_by_category("ml")]
        elif "sales" in request or "revenue" in request:
            state["intent"] = "business_intelligence"
            state["subagent_plans"] = [DataAgent().plan_data_access(str(state.get("request", "")))]
            state["tool_names"] = [tool.name for tool in registry.get_by_category("bi")]
        elif "relationship" in request or "document" in request or "knowledge" in request:
            state["intent"] = "knowledge_retrieval"
            state["subagent_plans"] = [KnowledgeAgent().plan_retrieval(str(state.get("request", "")))]
            state["tool_names"] = [tool.name for tool in registry.get_by_category("knowledge")]
        else:
            state["intent"] = "general"
            state["subagent_plans"] = []
        return state

    def _context_handler(self, state: dict) -> dict:
        state.setdefault("environment", "powerbi")
        state.setdefault("dialect", "DAX")
        state.setdefault("source_type", "warehouse")
        return state

    def _plan_handler(self, state: dict) -> dict:
        state.setdefault("metrics", ["overview"])
        if "sales" in str(state.get("request", "")).lower():
            state["metrics"] = ["sales"]
        if "revenue" in str(state.get("request", "")).lower():
            state["metrics"].append("revenue")
        return state

    def _execute_handler(self, state: dict) -> dict:
        state["execution"] = "query_generated"
        state.setdefault("tool_names", [])
        return state

    def _validate_handler(self, state: dict) -> dict:
        request = str(state.get("request", "")).lower()
        if "urgent" in request or "approval" in request:
            state["route_to"] = "escalate"
            state["next_node"] = "escalate"
        else:
            state["route_to"] = "explain"
            state["next_node"] = "explain"
        return state

    def _explain_handler(self, state: dict) -> dict:
        state["result"] = "Report prepared for review"
        return state

    def _escalate_handler(self, state: dict) -> dict:
        state["result"] = "Escalated for human review"
        return state

    def run(self, request: str) -> dict:
        state = {"request": request}
        return self.graph.run("router", state)

    def run_parallel(
        self,
        request: str,
        max_workers: Optional[int] = None,
        summarize: bool = False,
    ) -> Union[List[dict], dict]:
        state = {"request": request}
        branch_specs = [
            ("sales", "sales_report"),
            ("revenue", "revenue_report"),
            ("customer", "customer_report"),
        ]

        selected_specs = [spec for spec in branch_specs if spec[0] in request.lower()]
        if not selected_specs:
            selected_specs = [("overview", "default_report")]

        if max_workers is None:
            max_workers = len(selected_specs) or 1

        results: List[dict] = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self._execute_parallel_branch, self._build_parallel_state(state, keyword, branch_name))
                for keyword, branch_name in selected_specs
            ]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        results.sort(key=lambda item: item.get("branch_name", ""))

        if summarize:
            return {
                "branches": results,
                "summary": self._summarize_parallel_results(results),
                "key_results": self._extract_tuning_points(results),
            }

        return results

    def _build_parallel_state(self, state: dict, keyword: str, branch_name: str) -> dict:
        branch_state = copy.deepcopy(state)
        branch_state["branch_name"] = branch_name
        branch_state["branch_type"] = "parallel"
        branch_state["metrics"] = [keyword]
        return branch_state

    def _summarize_parallel_results(self, results: List[dict]) -> str:
        branch_names = [result.get("branch_name", "unknown") for result in results]
        metrics = sorted({metric for result in results for metric in result.get("metrics", [])})
        metric_text = ", ".join(metrics) if metrics else "overview"
        return f"Completed {len(results)} parallel branches: {', '.join(branch_names)}. Metrics: {metric_text}"

    def _extract_tuning_points(self, results: List[dict]) -> List[dict]:
        tuning_points: List[dict] = []
        for result in results:
            branch_name = result.get("branch_name", "unknown")
            metrics = result.get("metrics", [])
            tuning_points.append(
                {
                    "branch": branch_name,
                    "metric": metrics[0] if metrics else "overview",
                    "status": "completed",
                    "focus": f"Tune {branch_name} for {metrics[0] if metrics else 'overview'}",
                }
            )
        return tuning_points

    def _execute_parallel_branch(self, state: dict) -> dict:
        time.sleep(0.2)
        state = self.graph.run("router", state)
        state["parallel_branch_completed"] = True
        return state
