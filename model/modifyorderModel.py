from helpers.database import *

class ModifyOrderModel:
    @staticmethod
    def store_updated_order(order_id, data):
        update_new_order(order_id, data)