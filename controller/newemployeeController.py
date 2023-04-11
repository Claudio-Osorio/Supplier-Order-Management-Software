from tkinter import *
import tkinter as tk
from tkinter import ttk

class NewEmployeeController:
    def __init__(self, root, model, view, app_controller):
        self.root = root
        self.model = model
        self.view = view(root, self)
        self.app_controller = app_controller

    def show_ui(self):
        self.view.show_ui()

    def save_data(self,data):
        self.model.save_data(data)

    def refresh_employees(self):
        self.app_controller.refresh_search_options()

    def get_companies_and_projects(self):
        return self.model.get_companies_and_projects()