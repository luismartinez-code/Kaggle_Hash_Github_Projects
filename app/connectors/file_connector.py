from __future__ import annotations

from pathlib import Path

from .base import Connector, ConnectorConfig, ConnectorResult


class FileConnector(Connector):
    """A file-based connector for local CSV or JSON content."""

    def connect(self) -> None:
        self.connected = True

    def fetch(self, query: str | None = None) -> ConnectorResult:
        if not getattr(self, "connected", False):
            self.connect()

        path = self.config.source_path or ""
        target = Path(path)
        if not target.exists():
            return ConnectorResult(rows=[], metadata={"path": str(target), "status": "missing"})

        return ConnectorResult(
            rows=[{"path": str(target), "source": self.config.name}],
            metadata={"connector_type": self.config.connector_type, "path": str(target)},
        )

    def close(self) -> None:
        self.connected = False
