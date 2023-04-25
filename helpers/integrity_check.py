import logging
from helpers.configurations import *
import os

def file_exists(file_relative_path, error_msg):
    if os.path.exists(str(os.getcwd()) + str(file_relative_path)):
        return True
    else:
        logging.critical(error_msg)
        return False

def check_status_folder_exists():
    error_msg = "Company status header folder not found"
    return file_exists(read_status_header_path(), error_msg)

def check_status_header_exists(company_id, header_id):
    error_msg = "Company header folder not found"
    status_file_path = read_status_header_path() + \
                       str(company_id) + '\\' + str(header_id) + '.html'
    return file_exists(status_file_path, error_msg)