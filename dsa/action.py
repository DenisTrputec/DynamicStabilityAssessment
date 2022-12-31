from typing import List, Union, Callable

from power_system.bus import Bus
from power_system.branch import Branch
from power_system.machine import Machine


class Action:
    def __init__(self, function: Callable, argument: Union[int | float | Bus | Branch | Machine]):
        self.function = function
        self.argument = argument

    def activate(self):
        self.function(self.argument)
