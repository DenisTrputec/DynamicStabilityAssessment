import json
from os.path import dirname, join
from typing import List

from dsa.model import Model
from utils.logger import logger
from utils.system_manager import SystemManager


class Assessment:
    def __init__(self, name: str = "My DSA", description: str = "This is my very own Dynamic Stability Assessment",
                 models: List[Model] = None):
        self.name = name
        self.description = description
        self.models = models or []

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

    def save(self, filepath=None):
        logger.info(f"Saving assessment '{self.name}'")
        filepath = filepath or join("assessments", f"{self.name}.json")
        SystemManager.create_folder(dirname(filepath))
        json_dump = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        with open(filepath, "w") as outfile:
            outfile.write(json_dump)
        logger.info(f"Assessment '{self.name}' saved successfully")

    @classmethod
    def load_from_json(cls, json_path):
        logger.info(f"Loading assessment '{json_path}'")
        with open(json_path, "r") as handle:
            assessment_json = json.load(handle)
            name = assessment_json["name"]
            description = assessment_json["description"]
            models = [Model.load_from_json(model_json) for model_json in assessment_json["models"]]
            instance = cls(name, description, models)
            logger.info(f"Assessment '{name}' loaded successfully")
            return instance

