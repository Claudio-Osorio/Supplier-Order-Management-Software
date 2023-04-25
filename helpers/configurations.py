from configparser import ConfigParser
from helpers.email_threading import *
import os

config_object = ConfigParser()
config_object.read("config.ini")

# DEVELOPMENT - ACCESSORS
def read_debug_mode():
    return config_object["developer_mode"]["debug_mode"]

# UI - ACCESSORS
def read_version():
    return config_object["about"]["version"]

def read_main_window_geometry():
    return config_object["geometry"]["main_window"]

def read_tree_status_filter(status):
    return config_object["search_param"][f"""{status}"""]

def read_tree_sorting():
    return config_object["search_param"]["sorting_by_col"]

def read_tree_sorting_type():
    return config_object["search_param"]["sorting_type"]

def read_tree_limit():
    return int(config_object["search_param"]["tree_limit"])

# DATABASE - ACCESSORS
def read_database_path():
    return config_object["database"]["database_path"]

def read_DDL_path():
    return config_object["database"]["ddl_path"]

def read_restored_DML_path():
    return config_object["database"]["restore_dml_path"]

def read_dummy_DML_path():
    return config_object["database"]["dummy_dml_path"]

# EMAIL - ACCESSORS
def read_table_style():
    return read_file('email', 'email_table_style_path')

def read_introduction():
    return read_file('email', 'email_introduction_path')

def read_table_header():
    return read_file('email', 'email_table_header_path')

def read_table_footer():
    return read_file('email', 'email_table_footer_path')

def read_default_email_cc():
    return read_file('email', 'email_cc_path')

def read_default_subject():
    return read_file('email', 'email_subject_path')

def read_status_header_path():
    return config_object["email"]["email_status_header_path"]

def read_status_header_file(company_id, status_id):
    status_header_path = config_object["email"]["email_status_header_path"] + \
                         str(company_id) + '\\' + str(status_id) + '.html'
    with open(os.getcwd() + status_header_path, 'r') as file:
        header = file.read()
    return header

def read_attachment_partial_path():
    return config_object["email"]["email_attachment_path"]

def read_default_signature():
    return read_file('email', 'email_signature_path')

# UI - MUTATORS
def store_tree_status_filter(check_box_status):
    key_list = check_box_status.keys()
    for key in key_list:
        if check_box_status[key]:
            config_object["search_param"][key] = str(True)
        else:
            config_object["search_param"][key] = str(False)
    write_config()

def store_main_window_geometry(geometry):
    config_object["geometry"]["main_window"] = str(geometry)
    write_config()

def store_tree_sorting(sorting):
    config_object["search_param"]["sorting_by_col"] = str(sorting)
    write_config()

def store_tree_sorting_type(_type):
    config_object["search_param"]["sorting_type"] = str(_type)
    write_config()

def store_tree_limit(limit):
    config_object["search_param"]["tree_limit"] = str(limit)
    write_config()

def store_status_header_path(path):
    config_object["email"]["email_status_header_path"] = str(path)
    write_config()

# DATABASE - MUTATORS
def store_database_path(path):
    config_object["PATHS"]["database_path"] = path
    write_config()

def store_DDL_path(path):
    config_object["database"]["ddl_path"] = path
    write_config()

def store_dummy_DML_path(path):
    config_object["database"]["dummy_dml_path"] = path
    write_config()

# HELPERS
def reset_entire_section(section_name):
    if config_object.has_section(section_name):
        config_object.remove_section(section_name)
        config_object.add_section(section_name)

def read_file(section, item):
    with email_lock:
        with open(os.getcwd() + config_object[section][item], 'r') as file:
            return file.read()

def write_config():
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
