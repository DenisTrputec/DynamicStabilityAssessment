from typing import List, Union, Callable

from power_system.bus import Bus
from power_system.branch import Branch
from power_system.machine import Machine
from dsa.psse import PSSE


class Action:
    def __init__(self, name: str, method_key: str, argument: Union[int, float, Bus, Branch, Machine]):
        self.name = f"{name}: {argument}"
        self.method_key = method_key
        self.argument = argument

    def __str__(self):
        return self.name

    def activate(self):
        PSSE.method[self.method_key](self.argument)

    @classmethod
    def load_from_json(cls, json_string):
        name = json_string["name"].split(':')[0]
        key = json_string["method_key"]
        argument = Action.__get_argument(json_string["argument"])
        instance = Action(name, key, argument)
        return instance

    @staticmethod
    def __get_argument(argument_json):
        if "cc" in argument_json:
            return Bus.load_from_json(argument_json)
        elif "bus2" in argument_json:
            return Branch.load_from_json(argument_json)
        else:
            return Machine.load_from_json(argument_json)
