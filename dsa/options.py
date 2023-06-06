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
        self.group_by_subplot_type = group_by_subplot_type
        self.group_by_subplot_values = group_by_subplot_values
        self.group_by_subplot_in_use = group_by_subplots_in_use

    def __str__(self):
        return f"Type: {self.type}" \
               f"In sse: {self.in_use}" \
               f"Group by page type: {self.group_by_page_type}" \
               f"Group by page values: {self.group_by_page_values}" \
               f"Group by subplot type: {self.group_by_subplot_type}" \
               f"Group by subplot values: {self.group_by_subplot_values}" \
               f"Group by subplot - In use: {self.group_by_subplot_in_use}\n"
