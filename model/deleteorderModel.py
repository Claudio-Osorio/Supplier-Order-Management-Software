from helpers.database import delete_order
import os, logging
from helpers.configurations import read_attachment_partial_path

class DeleteOrderModel:
    @staticmethod
    def delete_orders(list_orders):
        for order in list_orders:
            DeleteOrderModel.delete_attachment(order=order)
            delete_order(order_id=order[0])

    @staticmethod
    def delete_attachment(order):
        _id = order[0]
        attachment_name = order[13]
        if attachment_name:
            attachment_path = os.getcwd() + \
                              read_attachment_partial_path() + \
                              attachment_name
            if os.path.exists(attachment_path):
                try:
                    os.remove(attachment_path)
                    logging.info(f"Order Id:{_id} - Successfully deleted"
                                 f" attachment \"{attachment_name}\"")
                except FileNotFoundError:
                    logging.warning(f"Order Id:{_id} - Could not delete "
                                    f"expected attachment file \"{attachment_name}\"."
                                    f" File exists but cannot be accessed.")
            else:
                logging.warning(f"Order Id:{_id} - Could not delete "
                                f"expected attachment file \"{attachment_name}\"."
                                f" File not present.")
        else:
            logging.warning(f"Order Id:{_id} does not have any attachment. "
                            f"Deletion operation ignored.")