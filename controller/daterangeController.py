class DateRangeController:
    def __init__(self, root, model, view, app_controller):
        self.root = root
        self.model = model
        self.view = view(root, self)
        self.app_controller = app_controller

    def show_ui(self):
        self.view.show_ui()

    def store_setting(self, data):
        self.model.store_setting(data)
        self.refresh_ui()

    def refresh_ui(self):
        self.app_controller.refresh_search_options()
        self.app_controller.refresh_view()