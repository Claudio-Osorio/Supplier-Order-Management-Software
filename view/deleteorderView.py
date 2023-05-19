from tkinter.messagebox import askyesno

class DeleteOrderView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.win = None

    @staticmethod
    def show_ui(list_orders):
        message ="Are you sure you want to delete "
        num_orders = len(list_orders)
        if num_orders > 1:
            message+=  f"""the following {num_orders} orders?\n"""
        else:
            message+=  f""" the following order?\n"""
        message += "This CANNOT be undone.\n\n"

        for index, order in enumerate(list_orders, 1):
            order_no = order[4]
            message += f"""{index}.- Order #{order_no}\n"""
            if index > 4:
                message += f"""...and more"""
                break
        return askyesno("Delete Order", message)