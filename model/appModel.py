from helpers.database import *
from helpers.configurations import store_main_window_geometry

class AppModel:
    @staticmethod
    def validate_database():
        validate_database()

    @staticmethod
    def store_current_geometry(geometry):
        store_main_window_geometry(geometry)

    @staticmethod
    def import_excel_file():
        pass

    @staticmethod
    def export_to_excel_file():
        pass

    @staticmethod
    def edit_email_draft():
        pass