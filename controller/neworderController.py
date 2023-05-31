class NewOrderController:
    def __init__(self, root, model, view, app_controller):
        self.root = root
        self.model = model
        self.view = view(root, self)
        self.app_controller = app_controller

    def show_ui(self):
        self.view.show_ui()

    def update(self, order_id):
        self.view.show_ui()
        self.view.update(order_id)

    def refresh_orders(self):
        self.app_controller.refresh_view()

    def get_order(self, order_id):
        return self.model.get_order(order_id)

    def get_dict_order_by_id(self, order_id):
        return self.model.get_dict_order_by_id(order_id)

    def get_companies(self):
        return self.model.get_name_of_all_companies()

    def get_company_from_project_id(self, project_id):
        return self.model.get_company_from_project_id(project_id)

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

    def get_attachment_storage_path(self):
        return self.model.get_attachment_storage_path()

    def save_data(self,data):
        self.model.save_data(data)

    def store_updated_order(self,order_id, data):
        self.model.store_updated_order(order_id, data)

    def get_types(self):
        return self.model.get_all_types()

    def filter_options(self, combobox, options):
        self.model.filter_options(combobox, options)