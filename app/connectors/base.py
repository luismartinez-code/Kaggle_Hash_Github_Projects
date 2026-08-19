from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class ConnectorConfig:
    """Configuration for a data connector."""

    name: str
    connector_type: str
    connection_string: Optional[str] = None
    source_path: Optional[str] = None
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConnectorResult:
    """Container for connector execution results."""

    rows: List[dict[str, Any]]
    metadata: dict[str, Any] = field(default_factory=dict)


class Connector:
    """Abstract connector interface for data access."""

    def __init__(self, config: ConnectorConfig) -> None:
        self.config = config

    def connect(self) -> None:
        raise NotImplementedError

    def fetch(self, query: Optional[str] = None) -> ConnectorResult:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
