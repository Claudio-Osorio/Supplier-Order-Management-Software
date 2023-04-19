import time
class ImportController:
    def __init__(self,root, model, view, app_controller):
        self.root = root
        self.model = model
        self.view = view(root, self, app_controller)
        self.app_controller = app_controller

    def show_ui(self):
        self.view.show_ui()

    def refresh_view(self):
        self.view.refresh_list_of_orders()

    def import_excel_file(self, excel_file_path):
        summary = self.model.import_excel_file(excel_file_path)
        if summary is not None:
            self.view.import_summary(summary)
        else:
            self.view.import_failed()