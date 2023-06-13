class ModifyOrderController:
    def __init__(self, root, model, view, app_controller, new_order_controller):
        self.root = root
        self.model = model
        self.view = view(root, self)
        self.app_controller = app_controller
        self.new_order_controller = new_order_controller

    def modify(self, order_id):
        self.view.show_ui()
        self.view.modify(order_id)

    def refresh_orders(self):
        self.app_controller.refresh_view()

    def store_updated_order(self,order_id, data):
        self.model.store_updated_order(order_id, data)

    def get_companies(self):
        return self.new_order_controller.get_companies()

    def get_order(self, order_id):
        return self.new_order_controller.get_order(order_id)

    def get_dict_order_by_id(self, order_id):
        return self.new_order_controller.get_dict_order_by_id(order_id)

    def get_companies(self):
        return self.new_order_controller.get_companies()

    def get_company_from_project_id(self, project_id):
        return self.new_order_controller.get_company_from_project_id(project_id)

    def get_projects_for_company(self, company_id):
        return self.new_order_controller.\
            get_projects_for_company(company_id)

    def get_statuses(self):
        return self.new_order_controller.get_statuses()

    def get_supervisors(self):
        return self.new_order_controller.get_supervisors()

    def get_employees(self):
        return self.new_order_controller.get_employees()

    def get_preferred_employee(self, project_id):
        return self.new_order_controller.get_preferred_employee(project_id)

    def get_attachment_storage_path(self):
        return self.new_order_controller.get_attachment_storage_path()

    def save_data(self,data):
        self.new_order_controller.save_data(data)

    def get_types(self):
        return self.new_order_controller.get_types()

    def filter_options(self, combobox, options):
        self.new_order_controller.filter_options(combobox, options)