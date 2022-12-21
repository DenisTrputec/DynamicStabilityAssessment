import json
from typing import List

from dsa.model import Model


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        else:
            return json.JSONEncoder.default(self, obj)


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

    def __to_json(self):
        return dict(name=self.name, description=self.description, models=self.models)

    def save(self):
        # print(self.__to_json())
        # json_string = json.dumps(self.__to_json(), cls=ComplexEncoder, indent=4)
        # print(json_string)
        json_string = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        with open(f"assessments/{self.name}.json", "w") as outfile:
            outfile.write(json_string)


if __name__ == '__main__':
    m1 = Model("Model 1")
    m2 = Model("Model 2")
    a = Assessment("DSA HOPS 2022", "Dynamic Stability Assessment for 2022", [m1, m2])
    print(a.info)