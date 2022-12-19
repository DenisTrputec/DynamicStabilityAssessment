from typing import List

from dsa.model import Model


class Assessment:
    def __init__(self, name: str, description: str = "", models: List[Model] = None):
        self.name = name
        self.description = description
        self.models = models if models else []

    def __str__(self):
        return f"Assessment: {self.name}"

    @property
    def info(self):
        text = f"\nName: {self.name}"
        if self.description:
            text += f"\nDescription: {self.description}"
        if self.models:
            text += "\nModels:"
            for model in self.models:
                text += f"\n\t{model.name}"
        return text


if __name__ == '__main__':
    m1 = Model("Model 1")
    m2 = Model("Model 2")
    a = Assessment("DSA HOPS 2022", "Dynamic Stability Assessment for 2022", [m1, m2])
    print(a.info)