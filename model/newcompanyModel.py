import logging

from helpers.database import store_new_company,store_new_division
from helpers.integrity_check import *
import os
import shutil

class NewCompanyModel:
    def __init__(self):
        self.divisions = list()

    @staticmethod
    def store_data(company_data, company_divisions):
        try:
            if check_status_folder_exists():
                for status_id in range(1,9):
                    if not check_status_header_exists(0, status_id):
                        raise FileNotFoundError

                new_company_id = store_new_company(company_data)

                if new_company_id is not None:
                    for division in company_divisions:
                        store_new_division(new_company_id, division)
                else:
                    raise ValueError

                curr_abs_header_path = os.getcwd() + read_status_header_path()
                src = curr_abs_header_path + '0' + '\\'
                dst = curr_abs_header_path + str(new_company_id) + '\\'
                shutil.copytree(src, dst)
            else:
                raise FileNotFoundError

            logging.info(f"New Company id:{new_company_id} - {company_data}: successfully stored."
                         f" Header files successfully created.")

        except FileNotFoundError:
            logging.critical("File integrity failed. Files needed to create a new company"
                             " were not found. New company not stored")
        except ValueError:
            logging.critical("Failed storing new company on database")
        except:
            logging.critical("Unexpected error while storing new company")

    def add_division(self, data):
        self.divisions.append(data)

    def remove_division(self, division_id):
        del self.divisions[division_id]

    def get_divisions(self):
        return self.divisions