import pathlib
import yaml


class Settings(object):

    def __init__(self, root_path: str = './'):
        self.filename = pathlib.Path(root_path) / 'settings.yaml'
        self.load()

    def load(self,):
        with open(self.filename, 'r') as file:
            self.data = yaml.safe_load(file)

    def save(self):
        with open(self.filename, 'w') as file:
            yaml.dump(self.data, file)
