from view.appView import AppView
from model.appModel import AppModel
from controller.appController import AppController

class App:
    def __init__(self, root):
        self.root = root
        self.controller = AppController(root, AppModel, AppView)
        self.controller.validate_database()
        self.controller.show_main_ui()