class NewOrderController:
    def __init__(self, root, model, view, app_controller):
        self.root = root
        self.model = model
        self.view = view(root, self)
        self.app_controller = app_controller

    def show_new_order_ui(self):
        self.view.show_add_new_order()

    def refresh_orders(self):
        self.app_controller.refresh_view()

    def get_companies(self):
        return self.model.get_name_of_all_companies()

    def get_projects_for_company(self, company_id):
        return self.model.\
            get_all_projects(company_id)

    def get_statuses(self):
        return self.model.get_all_statuses()

    def get_supervisors(self):
        return self.model.get_all_supervisors()

    def get_employees(self):
        return self.model.get_all_employees()

    def get_preferred_employee(self, project_id):
        return self.model.get_preferred_employee(project_id)

    def save_data(self,data):
        self.model.save_data(data)

    def get_types(self):
        return self.model.get_all_types()