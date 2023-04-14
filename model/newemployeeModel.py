from helpers.database import *

class NewEmployeeModel:
    @staticmethod
    def get_companies_and_projects():
        companies = get_name_of_all_companies()
        data = list()
        for company in companies:
            projects = get_all_projects(company[0])
            for project in projects:
                unique_project = (project[0],
                                  f"{company[1]} - {project[1]}")
                data.append(unique_project)
        return data

    @staticmethod
    def save_data(data):
        print("storing")
        employee_id = store_new_employee(data)
        if data["projects"] is not None:
            delete_preferred_employee(data["projects"])
            store_new_preferred_employee(employee_id,data["projects"])