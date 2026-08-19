from __future__ import annotations

from .base import Connector, ConnectorConfig, ConnectorResult


class SQLConnector(Connector):
    """A simple SQL connector stub for local prototype use."""

    def connect(self) -> None:
        self.connected = True

    def fetch(self, query: str | None = None) -> ConnectorResult:
        if not getattr(self, "connected", False):
            self.connect()

        query_text = query or "SELECT 1 AS placeholder"
        return ConnectorResult(
            rows=[{"query": query_text, "source": self.config.name}],
            metadata={"connector_type": self.config.connector_type, "query": query_text},
        )

    def close(self) -> None:
        self.connected = False
