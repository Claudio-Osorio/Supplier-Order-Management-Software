# Controller
from controller.mainController import MainController
from controller.neworderController import NewOrderController
from controller.deleteorderController import DeleteOrderController
from controller.newsupervisorController import NewSupervisorController
from controller.newemployeeController import NewEmployeeController
from controller.newcompanyController import NewCompanyController
from controller.newprojectController import NewProjectController
# View
from view.aboutView import AboutView
from view.mainView import MainView
from view.neworderView import NewOrderView
from view.deleteorderView import DeleteOrderView
from view.newsupervisorView import NewSupervisorView
from view.newemployeeView import NewEmployeeView
from view.newcompanyView import NewCompanyView
from view.newprojectView import NewProjectView
# Model
from model.mainModel import MainModel
from model.neworderModel import NewOrderModel
from model.deleteorderModel import DeleteOrderModel
from model.newsupervisorModel import NewSupervisorModel
from model.newemployeeModel import NewEmployeeModel
from model.newcompanyModel import NewCompanyModel
from model.newprojectModel import NewProjectModel

class AppController:
    def __init__(self, root, model, view):
        self.root = root
        self.model = model
        self.view = view(root, self)

        self.main_controller = None
        self.new_order_controller = None
        self.delete_order_controller = None
        self.new_employee_controller = None
        self.new_supervisor_controller = None
        self.new_company_controller = None
        self.new_project_controller = None

    def validate_database(self):
        self.model.validate_database()

    def about(self):
        AboutView.show_ui(self)

    def show_main_ui(self):
        self.main_controller = MainController(self.root,
                                            MainModel,
                                            MainView,
                                            self)
        self.main_controller.show_ui()

    def refresh_view(self):
        self.main_controller.refresh_view()

    def refresh_search_options(self):
        self.main_controller.refresh_search_options()

    # Returns list of all selected orders
    def get_selected_orders(self):
        return self.main_controller.get_selected_orders_id()

    def new_order(self):
        self.new_order_controller = NewOrderController(self.root,
                                            NewOrderModel,
                                            NewOrderView,
                                            self)
        self.new_order_controller.show_ui()

    def update_order(self):
        orders_id = self.main_controller.get_selected_orders()
        for order_id in orders_id:
            self.new_order_controller = NewOrderController(self.root,
                                                           NewOrderModel,
                                                           NewOrderView,
                                                           self)
            self.new_order_controller.update(order_id)

    def delete_order(self):
        orders_id = self.main_controller.get_selected_orders()
        if len(orders_id) >= 1:
            self.delete_order_controller = DeleteOrderController(self.root,
                                                 DeleteOrderModel,
                                                 DeleteOrderView,
                                                 self)
            self.delete_order_controller.delete_selected_orders(orders_id)

    def import_excel_file(self):
        self.model.import_excel_file()

    def export_to_excel_file(self):
        self.model.export_to_excel_file()

    def new_supervisor(self):
        self.new_supervisor_controller = NewSupervisorController(self.root,
                                             NewSupervisorModel,
                                             NewSupervisorView,
                                             self)
        self.new_supervisor_controller.show_ui()

    def update_supervisor(self):
        self.model.update_supervisor()

    def delete_supervisor(self):
        pass

    def new_employee(self):
        self.new_employee_controller = NewEmployeeController(self.root,
                                               NewEmployeeModel,
                                               NewEmployeeView,
                                               self)
        self.new_employee_controller.show_ui()

    def update_employee(self):
        pass

    def delete_employee(self):
        pass

    def new_company(self):
        self.new_company_controller = NewCompanyController(self.root,
                                             NewCompanyModel,
                                             NewCompanyView,
                                             self)
        self.new_company_controller.show_ui()

    def update_company(self):
        pass

    def delete_company(self):
        pass

    def new_project(self):
        self.new_project_controller = NewProjectController(self.root,
                                                             NewProjectModel,
                                                             NewProjectView,
                                                             self)
        self.new_project_controller.show_ui()

    def update_project(self):
        pass

    def delete_project(self):
        pass

    def store_current_geometry(self,geometry):
        self.model.store_current_geometry(geometry)

    def edit_email_draft(self):
        self.model.edit_email_draft()

    def get_companies(self):
        return self.model.get_name_of_all_companies()

    def get_projects_for_company(self, company_id):
        return self.model.\
            get_all_projects(company_id)

    def get_statuses(self):
        return self.model.get_all_statuses()

    def get_supervisors(self):
        return self.model.get_all_supervisors()

    def save_data(self,data):
        self.model.save_data(data)

    def get_types(self):
        return self.model.get_all_types()