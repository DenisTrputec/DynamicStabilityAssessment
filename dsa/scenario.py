from typing import List, Union

from dsa.disturbance import Disturbance


class Scenario:
    def __init__(self, name: str, description: str, actions: List[Union[float, Disturbance]] = None):
        self.name = name
        self.description = description
        self.actions = actions if actions else []

    def __str__(self):
        return f"Scenario: {self.name}"

    def info(self):
        text = f"\nScenario:" \
               f"\nName: {self.name}" \
               f"\nDescription: {self.description}" \
               f"\nActions:"
        for action in self.actions:
            pass
        return text