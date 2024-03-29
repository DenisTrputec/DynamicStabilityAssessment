from typing import List, Union, Callable

from power_system.bus import Bus
from power_system.branch import Branch
from power_system.machine import Machine
from dsa import psse


class Action:
    def __init__(self, name: str, method_key: str, argument: Union[int, float, Bus, Branch, Machine], index: int = 0):
        self.name = f"{name}: {argument}"
        self.method_key = method_key
        self.argument = argument
        self.index = index

    def __str__(self):
        return self.name

    def activate(self):
        if self.method_key == "clear_fault":
            psse.method[self.method_key](self.index)
        else:
            psse.method[self.method_key](self.argument)

    def update_name(self):
        self.name = f"{self.name.split(':')[0]}: {self.argument}"

    @classmethod
    def load_from_json(cls, json_string):
        name = json_string["name"].split(':')[0]
        key = json_string["method_key"]
        argument = cls.__get_argument(json_string["argument"])
        index = json_string["index"]
        instance = cls(name, key, argument, index)
        return instance

    @staticmethod
    def __get_argument(argument_json):
        if type(argument_json) is dict:
            if "cc" in argument_json:
                return Bus.load_from_json(argument_json)
            elif "bus2" in argument_json:
                return Branch.load_from_json(argument_json)
            else:
                return Machine.load_from_json(argument_json)
        else:
            return argument_json
