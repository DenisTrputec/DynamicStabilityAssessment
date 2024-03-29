from typing import List, Union

from dsa.action import Action
from utils.logger import logger


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
               f"\nDescription: {self.description}"
        if self.actions:
            text += f"\nActions:"
            for action in self.actions:
                text += f"\n\t{action.name}"
        return text

    @classmethod
    def load_from_json(cls, json_string):
        logger.info(f"Loading scenario...")
        name = json_string["name"]
        description = json_string["description"]
        actions = []
        for action_json in json_string["actions"]:
            action = Action.load_from_json(action_json)
            actions.append(action)
        instance = cls(name, description, actions)
        logger.info(f"Scenario '{name}' loaded successfully")
        return instance

    def update_clear_faults_indexes(self):
        logger.info("Updating Clear Faults Indexes")
        cleared = []
        for clear_fault in [x for x in self.actions if x.method_key == "clear_fault"]:
            i = 1
            for fault in [x for x in self.actions if x.method_key in ["bus_fault", "line_fault"]]:
                if clear_fault.argument.name == fault.argument.name:
                    cleared.append(fault)
                    clear_fault.index = i
                elif fault not in cleared:
                    i += 1

    def update_corresponding_clear_fault(self, updated_fault: Action):
        logger.info("Updating Corresponding Clear Fault")
        for fault_index, fault in enumerate([x for x in self.actions if x.method_key in ["bus_fault", "line_fault"]]):
            if updated_fault.argument.name == fault.argument.name:
                for clear_fault in [x for x in self.actions if x.method_key == "clear_fault"]:
                    if clear_fault.index - 1 == fault_index:
                        clear_fault.argument = updated_fault.argument
                        clear_fault.update_name()
