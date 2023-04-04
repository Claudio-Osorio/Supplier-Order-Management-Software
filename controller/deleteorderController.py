from database import get_order_by_id
class DeleteOrderController:
    def __init__(self, root, model, view, app_controller):
        self.root = root
        self.model = model
        self.view = view(root, self)
        self.app_controller = app_controller

    def confirm_deletion(self, list_orders):
        return self.view.show_ui(list_orders)

    def delete_selected_orders(self, orders_id):
        list_orders = list()
        for _id in orders_id:
            list_orders.append(get_order_by_id(_id)[0])
        print(list_orders)
        if self.confirm_deletion(list_orders):
            self.model.delete_orders(list_orders)
            self.refresh_orders()

    def refresh_orders(self):
        self.app_controller.refresh_view()