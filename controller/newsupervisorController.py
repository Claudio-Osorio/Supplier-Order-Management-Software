class NewSupervisorController:
    def __init__(self, root, model, view, app_controller):
        self.root = root
        self.model = model
        self.view = view(root, self)
        self.app_controller = app_controller

    def show_ui(self):
        self.view.show_ui()

    def refresh_supervisors(self):
        self.app_controller.refresh_search_options()

    def save_data(self, data):
        self.model.save_data(data)