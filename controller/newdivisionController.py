
class NewDivisionController:
    def __init__(self, root, model, view, new_company_controller):
        self.root = root
        self.model = model
        self.view = view(root, self)
        self.new_company_controller = new_company_controller

    def show_ui(self):
        self.view.show_ui()

    def callback_add_division(self, data):
        self.new_company_controller.add_division(data)

