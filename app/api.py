from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from app.agents.router_agent import RouterAgent
from app.workflow.graph_runner import GraphRunner


class AgentRequestHandler(BaseHTTPRequestHandler):
    """Minimal HTTP entrypoint for the agent platform."""

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/route":
            payload = self._read_json_body()
            self._send_json(HTTPStatus.OK, route_request_payload(payload))
            return

        if self.path == "/workflow/parallel":
            payload = self._read_json_body()
            self._send_json(HTTPStatus.OK, run_parallel_workflow_payload(payload))
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def _read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
        try:
            return json.loads(body) if body else {}
        except json.JSONDecodeError:
            return {"error": "invalid_json"}

    def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def route_request_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    request_text = str((payload or {}).get("request", "")).strip() or "general request"
    router = RouterAgent()
    return router.route_request(request_text)


def run_parallel_workflow_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    request_text = str((payload or {}).get("request", "")).strip() or "general request"
    max_workers = (payload or {}).get("max_workers")
    summarize = bool((payload or {}).get("summarize", False))
    runner = GraphRunner()
    return runner.run_parallel(request_text, max_workers=max_workers, summarize=summarize)


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), AgentRequestHandler)
    print(f"Serving agent API on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
