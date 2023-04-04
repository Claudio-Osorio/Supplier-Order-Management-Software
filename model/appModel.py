from database import *
from configurations import store_main_window_geometry

class AppModel:
    @staticmethod
    def validate_database():
        validate_database()

    @staticmethod
    def store_current_geometry(geometry):
        store_main_window_geometry(geometry)