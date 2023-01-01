import os
import json
from typing import List

from dsa.model import Model


class Assessment:
    def __init__(self, name: str = "", description: str = "", models: List[Model] = None):
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

    def save(self):
        for model in self.models:
            print("Model:", model)
            for scenario in model.scenarios:
                print("Scenario:", scenario)
                for action in scenario.actions:
                    print("Action:", action)
        if not os.path.exists("assessments"):
            os.makedirs("assessments")
        json_string = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        print(json_string)
        with open(f"assessments/{self.name}.json", "w") as outfile:
            outfile.write(json_string)

    @classmethod
    def load_from_json(cls, json_path):
        with open(json_path, "r") as handle:
            assessment_json = json.load(handle)
            name = assessment_json["name"]
            description = assessment_json["description"]
            models = []
            for model_json in assessment_json["models"]:
                model = Model.load_from_json(model_json)
                models.append(model)
            instance = Assessment(name, description, models)
            return instance


if __name__ == '__main__':
    m1 = Model("Model 1")
    m2 = Model("Model 2")
    a = Assessment("DSA HOPS 2022", "Dynamic Stability Assessment for 2022", [m1, m2])
    print(a.info)