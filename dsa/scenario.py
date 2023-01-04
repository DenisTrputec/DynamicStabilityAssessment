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
        for action_json in json_string["actions"]:
            action = Action.load_from_json(action_json)
            actions.append(action)
        instance = cls(name, description, actions)
        return instance

    def update_clear_faults_index(self):
        for clear_fault in [x for x in self.actions if x.method_key == "clear_fault"]:
            for i, fault in enumerate([x for x in self.actions if x.method_key in ["bus_fault", "line_fault"]]):
                if clear_fault.argument.name == fault.argument.name:
                    clear_fault.index = i + 1

    def update_clear_fault(self, updated_fault: Action):
        for fault_index, fault in enumerate([x for x in self.actions if x.method_key in ["bus_fault", "line_fault"]]):
            print(1, fault)
            if updated_fault.argument.name == fault.argument.name:
                print(2)
                for clear_fault in [x for x in self.actions if x.method_key == "clear_fault"]:
                    print(3, clear_fault)
                    if clear_fault.index - 1 == fault_index:
                        print(4, clear_fault.index)
                        clear_fault.argument = updated_fault.argument
                        clear_fault.update_name()
