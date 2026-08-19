import unittest

from app.agents.data.data_agent import DataAgent
from app.agents.ml.ml_agent import MLAgent
from app.agents.knowledge.knowledge_agent import KnowledgeAgent
from app.tools.registry import ToolRegistry


class SubagentAndToolTests(unittest.TestCase):
    def test_data_agent_plans_connector_use(self):
        agent = DataAgent()
        plan = agent.plan_data_access("Load sales data from the warehouse")

        self.assertEqual(plan["intent"], "data_access")
        self.assertEqual(plan["source"], "sql")
        self.assertIn("connector_tool", plan["recommended_tools"])

    def test_ml_agent_plans_training_workflow(self):
        agent = MLAgent()
        plan = agent.plan_model_workflow("Forecast monthly revenue")

        self.assertEqual(plan["task"], "forecasting")
        self.assertIn("model_train_tool", plan["recommended_tools"])

    def test_knowledge_agent_plans_retrieval(self):
        agent = KnowledgeAgent()
        plan = agent.plan_retrieval("Find relationship between policy and compliance")

        self.assertEqual(plan["source"], "graph")
        self.assertIn("retrieval_tool", plan["recommended_tools"])

    def test_tool_registry_contains_core_tools(self):
        registry = ToolRegistry()
        names = {tool.name for tool in registry.list_tools()}

        self.assertIn("sql_query_tool", names)
        self.assertIn("model_train_tool", names)
        self.assertIn("retrieval_tool", names)
        self.assertIn("observability_tool", names)


if __name__ == "__main__":
    unittest.main()
