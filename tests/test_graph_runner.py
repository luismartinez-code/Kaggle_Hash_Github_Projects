import time
import unittest

from app.workflow.graph_runner import GraphRunner


class GraphRunnerTests(unittest.TestCase):
    def test_standard_bi_scenario(self):
        runner = GraphRunner()
        result = runner.run("Show sales for the current quarter")

        self.assertEqual(result["intent"], "business_intelligence")
        self.assertIn("sales", result["metrics"])
        self.assertEqual(result["execution"], "query_generated")
        self.assertEqual(result["result"], "Report prepared for review")

    def test_escalation_scenario(self):
        runner = GraphRunner()
        result = runner.run("Urgent approval required for executive revenue report")

        self.assertEqual(result["route_to"], "escalate")
        self.assertEqual(result["result"], "Escalated for human review")

    def test_parallel_branches_for_multi_metric_request(self):
        runner = GraphRunner()
        branches = runner.run_parallel("Show sales revenue and customer trends")

        self.assertEqual(len(branches), 3)
        self.assertTrue(all(branch["parallel_branch_completed"] for branch in branches))
        self.assertTrue(any(branch["branch_name"] == "sales_report" for branch in branches))
        self.assertTrue(any(branch["branch_name"] == "revenue_report" for branch in branches))
        self.assertTrue(any(branch["branch_name"] == "customer_report" for branch in branches))

    def test_parallel_execution_is_concurrent(self):
        runner = GraphRunner()
        start = time.perf_counter()
        branches = runner.run_parallel("Show sales revenue", max_workers=2)
        elapsed = time.perf_counter() - start

        self.assertEqual(len(branches), 2)
        self.assertLess(elapsed, 0.35)

    def test_parallel_run_can_summarize_results(self):
        runner = GraphRunner()
        result = runner.run_parallel("Show sales revenue", summarize=True, max_workers=2)

        self.assertIn("branches", result)
        self.assertIn("summary", result)
        self.assertIn("key_results", result)
        self.assertIn("sales", result["summary"].lower())
        self.assertIn("revenue", result["summary"].lower())
        self.assertTrue(result["key_results"])
        self.assertTrue(all("branch" in item for item in result["key_results"]))


if __name__ == "__main__":
    unittest.main()
