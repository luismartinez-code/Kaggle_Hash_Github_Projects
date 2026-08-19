import unittest

from app.agents.router_agent import RouterAgent


class RouterAgentTests(unittest.TestCase):
    def test_routes_business_intelligence_requests(self):
        agent = RouterAgent()
        plan = agent.route_request("Summarize the sales trend for the last quarter")

        self.assertEqual(plan["intent"], "business_intelligence")
        self.assertEqual(plan["agents"], ["bi_agent", "data_agent"])

    def test_routes_machine_learning_requests(self):
        agent = RouterAgent()
        plan = agent.route_request("Train a classifier to predict churn")

        self.assertEqual(plan["intent"], "machine_learning")
        self.assertIn("ml_agent", plan["agents"])


if __name__ == "__main__":
    unittest.main()
