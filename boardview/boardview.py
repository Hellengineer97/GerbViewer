from pygerber.gerberx3.api.v2 import Project, GerberFile


class Boardview:
    def __init__(self, pygerber_project: Project | None = None):
        self.pygerber_project = pygerber_project if pygerber_project is not None else Project()
    def add_layer():
        self.pygerber_project