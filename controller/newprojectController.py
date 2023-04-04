class NewProjectController:
    def __init__(self, root, model, view, app_controller):
        self.root = root
        self.model = model
        self.view = view(root, self)
        self.app_controller = app_controller

    def show_ui(self):
        self.view.show_ui()

    def refresh_projects(self):
        self.app_controller.refresh_search_options()

    def get_companies(self):
        return self.model.get_name_of_all_companies()

    def get_divisions(self, company_id):
        return self.model.get_name_of_all_divisions(company_id)

    def get_employees(self):
        return self.model.get_name_of_all_employees()


    def save_data(self, data):
        self.model.save_data(data)