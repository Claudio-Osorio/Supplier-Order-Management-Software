from database import *

class NewOrderModel:
    def __init__(self):
        pass

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