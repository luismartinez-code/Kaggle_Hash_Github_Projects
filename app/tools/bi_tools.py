from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class BIEnvironment:
    """Represents a BI environment such as Power BI, Tableau, or Looker."""

    name: str
    language: str
    strengths: List[str]


class BITools:
    """Utility helpers for BI execution across different environments."""

    def __init__(self) -> None:
        self.supported_environments = [
            BIEnvironment("powerbi", "DAX", ["semantic models", "measure authoring", "dashboarding"]),
            BIEnvironment("tableau", "Tableau Calculations", ["visual analytics", "dashboards", "storypoints"]),
            BIEnvironment("looker", "LookML", ["explores", "semantic layer", "embedded analytics"]),
            BIEnvironment("qlik", "Script", ["data associations", "set analysis", "dashboards"]),
        ]

    def list_supported_environments(self) -> List[str]:
        return [environment.name for environment in self.supported_environments]

    def get_environment_profile(self, name: str) -> BIEnvironment | None:
        for environment in self.supported_environments:
            if environment.name.lower() == name.lower():
                return environment
        return None

    def recommend_language(self, environment: str) -> str:
        profile = self.get_environment_profile(environment)
        if profile is None:
            return "sql"
        return profile.language
