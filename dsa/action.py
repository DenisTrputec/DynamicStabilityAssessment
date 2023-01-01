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
