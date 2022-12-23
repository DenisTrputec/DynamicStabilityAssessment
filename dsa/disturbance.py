from typing import List, Union

from power_system.bus import Bus
from power_system.branch import Branch


class Disturbance:
    def __init__(self, element: Union[Bus, Branch], trip_elements: List[Union[Bus, Branch]], time: float):
        self.element = element
        self.trip_elements = trip_elements
        self.time = time
