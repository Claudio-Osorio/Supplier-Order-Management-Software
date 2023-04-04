import win32com.client
from datetime import datetime
from configurations import *
import pythoncom
import logging
from pprint import pprint

class ComposedEmail:
    def __init__(self, to_name, to_email):
        self.to_name = to_name
        self.to_email = to_email
        self.cc = read_default_email_cc()
        self.subject = read_default_subject()
        self.body = None
        self.signature = read_default_signature()

        self.paid_orders = list()
        self.short_paid_orders = list()
        self.approved_orders = list()
        self.pre_approved_orders = list()
        self.sent_orders = list()
        self.not_paid_orders = list()
        self.reviewing_orders = list()
        self.not_sent_orders = list()
        self.void_orders = list()

        self.all_order_status_lists = None

    def add_paid_order(self, order):
        self.paid_orders.append(order)

    def add_short_paid_order(self, order):
        self.short_paid_orders.append(order)

    def add_approved_order(self, order):
        self.approved_orders.append(order)

    def add_pre_approved_order(self, order):
        self.pre_approved_orders.append(order)

    def add_sent_order(self, order):
        self.sent_orders.append(order)

    def add_not_paid_order(self, order):
        self.not_paid_orders.append(order)

    def add_reviewing_order(self, order):
        self.reviewing_orders.append(order)

    def add_not_sent_order(self, order):
        self.not_sent_orders.append(order)

    def add_void_order(self, order):
        self.void_orders.append(order)

    def generate_body(self):
        self.all_order_status_lists = [self.paid_orders,
                                       self.short_paid_orders,
                                       self.approved_orders,
                                       self.pre_approved_orders,
                                       self.sent_orders,
                                       self.not_paid_orders,
                                       self.reviewing_orders,
                                       self.not_sent_orders,
                                       self.void_orders]

        self.body = str()
        self.body += read_table_style()
        self.body += (read_introduction()).format(self.to_name)
        # Processing subset of (orders by status)
        for subset_orders in self.all_order_status_lists:
            if subset_orders:
                self.generate_body_for_status(subset_orders)
        self.body += read_default_signature()
        return self.body

    def generate_body_for_status(self, order_by_status):
        company_id = (order_by_status[0])['company.id']
        status_id = (order_by_status[0])['order_status.id']

        self.body += read_status_header_path(company_id, status_id)
        self.body += read_table_header()

        for order in order_by_status:
            # Enter order stuff
            age = calculate_age(order["_order._date"])
            row =f"""  <tr>
                            <td>{order["order_type._type"]}:
                            {order["_order.id"]}</td>
                            <td>{order["_order._date"]}</td>
                            <td>{order["_order.order_number"]}</td>
                            <td>{order["community._name"]}</td>"""
            if order["_order.full_address"]:
                row += f""" <td>
                                <table style="width:100%">
                                    <th>{order["_order.full_address"]}</th>
                                    <tr>{order["_order.unit_address"]}</tr>
                                </table>
                            </td>"""
            elif order["_order.unit_address"]:
                row += f""" <td>{order["_order.unit_address"]}</td>"""
            else:
                row += f""" <td>{order["_order.full_address"]}</td>"""
            row += f"""     <td>${order["_order.amount"]}</td>
                            <td>{age}</td>
                        </tr>"""
            self.body += row
        self.body += read_table_footer()

    def create_email_draft(self, supervisor_id, outlook_id):
        pythoncom.CoInitialize()
        instance = win32com.client.Dispatch(pythoncom.CoGetInterfaceAndReleaseStream(
            outlook_id,
            pythoncom.IID_IDispatch))

        email = instance.CreateItem(0)
        email.To = self.to_email        # 'contact@company.com'
        email.CC = self.cc              # "a@cmp.com;b@cmp.com;c@cmp.com"
        email.Subject = self.subject    # 'Sample Email'
        email.HTMLBody = self.generate_body()
        # If True then it gets focused and script stalls.
        # With Display False it also shows up.
        email.Display(False)

        for a_list in self.all_order_status_lists:
            for order in a_list:
                if order["supervisor.id"] == supervisor_id:
                    order_id = order["_order.id"]
                    filename = order["_order.attachment_name"]
                    if filename and \
                        filename != 'None':

                        email.Attachments.Add(os.getcwd() + \
                                          read_attachment_partial_path() + \
                                          filename)
                        logging.info(f"Operational: Successfully attached {filename}"
                                     f" for order id {order_id} ")
                    else:
                        logging.warning(f"Operational: Order id {order_id} has no attachment."
                                        " Attachment operation ignored.")
        # email.Send()

def calculate_age(order_date):
    original_time = datetime.strptime(order_date, '%m/%d/%Y')
    today = datetime.today()
    age = today - original_time
    return str(age.days)