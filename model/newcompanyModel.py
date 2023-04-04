from database import store_new_company,store_new_division
class NewCompanyModel:
    def __init__(self):
        self.divisions = list()

    @staticmethod
    def store_data(company_name, company_divisions):
        new_company_id = store_new_company(company_name)

        for division in company_divisions:
            store_new_division(new_company_id, division)

    def add_division(self, data):
        self.divisions.append(data)

    def remove_division(self, division_id):
        del self.divisions[division_id]

    def get_divisions(self):
        return self.divisions