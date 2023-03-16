import os


class SystemManager:
    def __init__(self):
        pass

    @staticmethod
    def create_folder(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
