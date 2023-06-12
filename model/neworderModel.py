from helpers.database import *

class NewOrderModel:
    @staticmethod
    def save_data(data):
        store_new_order(data)

    @staticmethod
    def get_order(order_id):
        return get_order_by_id(order_id)

    @staticmethod
    def get_dict_order_by_id(order_id):
        return get_dict_order_by_id(order_id)

    @staticmethod
    def get_name_of_all_companies():
        return get_name_of_all_companies()

    @staticmethod
    def get_company_from_project_id(project_id):
        return get_company_from_project_id(project_id)

    @staticmethod
    def get_all_projects(company_id):
        return get_all_projects(company_id)

    @staticmethod
    def get_all_statuses():
        return get_all_order_status()

    @staticmethod
    def get_all_supervisors():
        return get_name_of_all_supervisors()

    @staticmethod
    def get_all_employees():
        return get_name_of_all_employees()

    @staticmethod
    def get_all_types():
        return get_all_types()

    @staticmethod
    def get_preferred_employee(project_id):
        return get_preferred_employee(project_id)

    @staticmethod
    def get_attachment_storage_path():
        return os.getcwd() + read_attachment_partial_path()

    @staticmethod
    def filter_options(combobox, options):
        if options:
            typed_text = combobox.get().lower()
            filtered_options = [option[1] for option in options if typed_text in option[1].lower()]
            combobox['values'] = filtered_options