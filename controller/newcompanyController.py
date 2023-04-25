from controller.newdivisionController import NewDivisionController
from model.newdivisionModel import NewDivisionModel
from view.newdivisionView import NewDivisionView
from controller.newdivisionController import NewDivisionController

class NewCompanyController:
    def __init__(self, root, model, view, app_controller):
        self.root = root
        self.model = model()
        self.view = view(root, self)

        self.app_controller = app_controller
        self.division_controller = None

    def show_ui(self):
        self.view.show_ui()

    def refresh_companies(self):
        self.app_controller.refresh_search_options()

    def store_data(self, company_name):
        divisions = self.get_pre_stored_divisions()
        self.model.store_data(company_name, divisions)

    def get_new_division(self):
        self.division_controller = NewDivisionController(self.root,
                                                    NewDivisionModel,
                                                    NewDivisionView,
                                                    self)
        self.division_controller.show_ui()

    def add_division(self, data):
        self.model.add_division(data)
        self.refresh_divisions()

    def remove_division(self, division_id):
        self.model.remove_division(division_id)
        self.refresh_divisions()

    def refresh_divisions(self):
        divisions = self.get_pre_stored_divisions()
        self.view.refresh_division_tree(divisions)

    def get_pre_stored_divisions(self):
        return self.model.get_divisions()

    def empty_division(self):
        divisions = self.get_pre_stored_divisions()
        if len(divisions) == 0:
            return True
        return False