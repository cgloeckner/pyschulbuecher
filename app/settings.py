import pathlib
import yaml


entry_grade = 5
graduation_grade = 12
course_grade = 11


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
