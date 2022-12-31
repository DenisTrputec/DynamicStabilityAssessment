from typing import List, Union

from dsa.action import Action


class Scenario:
    def __init__(self, name: str = "", description: str = "", actions: List[Union[float, Action]] = None):
        self.name = name
        self.description = description
        self.actions = actions if actions else []

    def __str__(self):
        return f"Scenario: {self.name}"

    @property
    def info(self):
        text = f"\nScenario:" \
               f"\nName: {self.name}" \
               f"\nDescription: {self.description}" \
               f"\nActions:"
        for action in self.actions:
            pass
        return text

    @classmethod
    def load_from_json(cls, json_string):
        name = json_string["name"]
        description = json_string["description"]
        actions = []
        # for action_json in json_string["actions"]:
        #     action = Action.load_from_json(action_json)
        #     actions.append(action)
        instance = Scenario(name, description, actions)
        return instance
