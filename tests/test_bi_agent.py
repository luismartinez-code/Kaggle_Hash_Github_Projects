import unittest

from app.agents.bi.bi_agent import BIAgent, BIContext
from app.tools.bi_tools import BITools


class BIAgentTests(unittest.TestCase):
    def test_plan_report_uses_bi_context(self):
        agent = BIAgent(context=BIContext(source_type="warehouse", dialect="snowflake", environment="powerbi"))
        plan = agent.plan_report("Show quarterly sales and revenue")

        self.assertEqual(plan["intent"], "report_generation")
        self.assertIn("sales", plan["metrics"])
        self.assertIn("revenue", plan["metrics"])
        self.assertIn("sql_query_tool", plan["suggested_tools"])

    def test_generate_query_for_sales(self):
        agent = BIAgent()
        query = agent.generate_query("Show me sales by month")

        self.assertIn("sales", query.lower())
        self.assertIn("group by", query.lower())

    def test_bi_tools_support_multiple_environments(self):
        tools = BITools()

        self.assertIn("powerbi", tools.list_supported_environments())
        self.assertIn("tableau", tools.list_supported_environments())
        self.assertEqual(tools.recommend_language("powerbi"), "DAX")


if __name__ == "__main__":
    unittest.main()
