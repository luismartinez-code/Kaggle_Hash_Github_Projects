import unittest

from app.agents.router_agent import RouterAgent
from app.workflow.graph_runner import GraphRunner


class RouterWorkflowIntegrationTests(unittest.TestCase):
    def test_router_includes_subagent_plans(self):
        router = RouterAgent()
        result = router.route_request("Forecast monthly revenue")

        self.assertEqual(result["intent"], "machine_learning")
        self.assertTrue(result["subagent_plans"])
        self.assertIn("ml_agent", result["agents"])

    def test_graph_runner_exposes_subagent_plans(self):
        runner = GraphRunner()
        result = runner.run("Forecast monthly revenue")

        self.assertEqual(result["intent"], "machine_learning")
        self.assertIn("subagent_plans", result)
        self.assertTrue(result["subagent_plans"])


if __name__ == "__main__":
    unittest.main()
