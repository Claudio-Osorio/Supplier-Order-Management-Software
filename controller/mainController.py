class MainController:
    def __init__(self,root, model, view, app_controller):
        self.root = root
        self.model = model
        self.view = view(root, self, app_controller)
        self.app_controller = app_controller

    def show_ui(self):
        self.view.show_ui()

    def fill_order_tree(self, order_tree, params):
        self.model.filter_orders_by_params(order_tree, params)

    def open_order(self, order_tree):
        self.model.open_order(order_tree)

    def send_orders(self, order_tree):
        self.model.prepare_emails(order_tree)

    def get_selected_orders(self):
        return self.view.get_selected_orders_id()

    def refresh_view(self):
        self.view.refresh_list_of_orders()

    def refresh_search_options(self):
        self.view.fill_search_entries()

    def get_companies(self):
        return self.model.get_name_of_all_companies()

    def get_projects_for_company(self, company_id):
        return self.model.\
            get_all_projects(company_id)

    def get_employees(self):
        return self.model.get_name_of_all_employees()

    def get_statuses(self):
        return self.model.get_all_statuses()

    def get_supervisors(self):
        return self.model.get_all_supervisors()

    def save_data(self,data):
        self.model.save_data(data)

    def get_types(self):
        return self.model.get_all_types()

    def read_tree_config(self):
        return self.model.read_tree_config()

    def read_search_checkbox_config(self, checkbox):
        return self.model.read_search_config(checkbox)

    def destroy_view(self):
        self.view.destroy_view()