import unittest

from app.api import route_request_payload, run_parallel_workflow_payload


class APITests(unittest.TestCase):
    def test_route_request_payload_uses_router(self):
        payload = route_request_payload({"request": "Show sales trends"})

        self.assertEqual(payload["intent"], "business_intelligence")
        self.assertIn("bi_agent", payload["agents"])

    def test_parallel_workflow_payload_supports_summary(self):
        payload = run_parallel_workflow_payload(
            {"request": "Show sales revenue", "summarize": True, "max_workers": 2}
        )

        self.assertIn("branches", payload)
        self.assertIn("summary", payload)
        self.assertIn("key_results", payload)


if __name__ == "__main__":
    unittest.main()
