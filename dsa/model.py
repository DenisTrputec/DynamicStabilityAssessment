from typing import List

from dsa.scenario import Scenario
from utils.logger import logger


class Model:
    def __init__(self, name: str = "", description: str = "", raw_path: str = "", dyr_path: str = "",
                 scenarios: List[Scenario] = None):
        self.name = name
        self.description = description
        self.raw_path = raw_path
        self.dyr_path = dyr_path
        self.scenarios = scenarios if scenarios else []

    def __str__(self):
        return f"Model: {self.name}"

    @property
    def info(self):
        text = f"\nName: {self.name}"
        if self.description:
            text += f"\nDescription: {self.description}"
        if self.raw_path:
            text += f"\nRAW filepath: \"{self.raw_path}\""
        if self.dyr_path:
            text += f"\nDYR filepath: \"{self.dyr_path}\""
        if self.scenarios:
            text += f"\nScenarios:"
            for scenario in self.scenarios:
                text += f"\n\t{scenario.name}"
        return text

    @classmethod
    def load_from_json(cls, json_string):
        logger.info(f"Loading model...")
        name = json_string["name"]
        description = json_string["description"]
        raw_path = json_string["raw_path"]
        dyr_path = json_string["dyr_path"]
        scenarios = [Scenario.load_from_json(scenario_json) for scenario_json in json_string["scenarios"]]
        instance = cls(name, description, raw_path, dyr_path, scenarios)
        logger.info(f"Model '{name}' loaded successfully")
        return instance
