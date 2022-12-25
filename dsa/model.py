from typing import List

from dsa.scenario import Scenario


class Model:
    def __init__(self, name: str = "", description: str = "", raw_path: str = "", dyr_path: str = "",
                 scenarios: List[Scenario] = None):
        self.name = name
        self.description = description
        self.raw_path = raw_path
        self.dyr_path = dyr_path
        self.scenarios = scenarios if scenarios else []

    def __str__(self):
        return f"Model: {self.name}"

    @property
    def info(self):
        text = f"\nName: {self.name}"
        if self.description:
            text += f"\nDescription: {self.description}"
        if self.raw_path:
            text += f"\nRAW filepath: \"{self.raw_path}\""
        if self.dyr_path:
            text += f"\nDYR filepath: \"{self.dyr_path}\""
        if self.scenarios:
            text += f"\nScenarios:"
            for scenario in self.scenarios:
                text += f"\n\t{scenario.name}"
        return text


if __name__ == '__main__':
    s1 = Scenario("Scene1", "Ispad na necemu")
    s2 = Scenario("Scene2", "Prekid signala")
    m = Model("Denis", "asd.raw", "fgh.dyr", "Model Desc", [s1, s2])
    print(m.info)
