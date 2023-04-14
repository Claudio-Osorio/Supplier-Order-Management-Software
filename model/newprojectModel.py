from helpers.database import get_name_of_all_companies
from helpers.database import get_all_divisions
from helpers.database import store_new_project
from helpers.database import get_name_of_all_employees

class NewProjectModel:
    @staticmethod
    def get_name_of_all_companies():
        return get_name_of_all_companies()

    @staticmethod
    def get_name_of_all_divisions(company_id):
        return get_all_divisions(company_id)

    @staticmethod
    def save_data(data):
        store_new_project(data)

    @staticmethod
    def get_name_of_all_employees():
        return get_name_of_all_employees()
