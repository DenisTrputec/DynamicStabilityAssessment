from enum import IntEnum
from typing import List


class OptionType(IntEnum):
    BusU = 1
    BranchP = 2


class GroupByType(IntEnum):
    VoltageLevel = 1
    ZoneNumber = 2


class Option:
    def __init__(self, option_type: OptionType, in_use: bool,
                 group_by_page_type: GroupByType, group_by_page_values: list,
                 group_by_subplot_type: GroupByType, group_by_subplot_values: list,
                 group_by_subplots_in_use: List[bool] = None):
        self.type = option_type
        self.in_use = in_use
        self.group_by_page_type = group_by_page_type
        self.group_by_page_values = group_by_page_values
        self.group_by_subplots_type = group_by_subplot_type
        self.group_by_subplots_values = group_by_subplot_values
        self.group_by_subplots_in_use = group_by_subplots_in_use
