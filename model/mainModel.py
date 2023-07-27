from helpers.composed_email import *
from helpers.database import *
import pythoncom, win32com.client, threading
from helpers.input_validation import blank_input
from helpers.configurations import store_tree_status_filter, read_tree_status_filter


class MainModel:
    # Returns the supervisor Id. Returns -1 if no supervisor is selected
    @staticmethod
    def get_current_supervisor_id(supervisor_tree):
        # Id is -1 when there is no supervisor
        if len(supervisor_tree.get_children()) == 1:
            return -1
        # Get record index
        selected = supervisor_tree.focus()
        # Handle when no selection
        if not selected:
            return -1

        # Get Record Value
        value = supervisor_tree.item(selected, 'values')
        return int(value[0])

    @staticmethod
    def filter_orders_by_params(order_tree, params):
        active_checkboxes_ids = list()
        checkboxes = params["status"]
        for key, value in checkboxes.items():
            if value:
                active_checkboxes_ids.append(int(key))

        sql = f"""
            SELECT  supervisor.id,
                    supervisor._name,
                    supervisor.phone_number,
                    supervisor.email,
                    employee.id,
                    employee._name,
                    employee.phone_number,
                    employee.email,
                    company.id,
                    company._name,
                    division.id,
                    division._name,
                    division.location,
                    division.accounts_payable_name,
                    division.accounts_payable_email,
                    project.id,
                    project._name,
                    order_type.id,
                    order_type._type,
                    order_status.id,
                    order_status._status,
                    _order.id,
                    _order.unit_address,
                    _order.full_address,
                    _order.order_number,
                    _order.amount,
                    _order._date,
                    _order.external_tracking,
                    _order.note,
                    _order.attachment_name
            FROM _order
            INNER JOIN supervisor
            ON _order.supervisor_id = supervisor.id 
            INNER JOIN employee 
            ON _order.employee_id = employee.id
            INNER JOIN order_status
            ON _order._status_id = order_status.id
            INNER JOIN order_type
            ON _order._type_id = order_type.id
            INNER JOIN project
            ON _order.project_id = project.id
            INNER JOIN division
            ON project.division_id = division.id
            INNER JOIN company
            ON project.company_id = company.id 
            """
        values = list()
        sql += f"""WHERE """
        # Search Parameters
        one_param = True
        sql += f"""_order._date BETWEEN ? AND ?"""
        values += [params["start_date"]]
        values += [params["end_date"]]
        sql += " \nAND "

        if "supervisor" in params:
            if params["supervisor"] != 0:
                    sql += f"""_order.supervisor_id = ?"""
                    values += [params["supervisor"]]
            else:
                one_param = False
        else:
            one_param = False

        if one_param:
            sql += " \nAND "
        else:
            one_param = True

        if "employee" in params:
            if params["employee"] != 0:
                    sql += f"""_order.employee_id = ?"""
                    values += [params["employee"]]
            else:
                one_param = False
        else:
            one_param = False

        if one_param:
            sql += " \nAND "
        else:
            one_param = True

        if params["project"] != 0:
            sql += f"""_order.project_id = ?"""
            values += [params["project"]]
        else:
            one_param = False

        if one_param:
            sql += " \nAND "
        else:
            one_param = True

        if "lot_blk" in params:
            sql += f"""_order.unit_address = ?"""
            values += [params["lot_blk"]]
        else:
            one_param = False

        if one_param:
            sql += " \nAND "
        else:
            one_param = True

        if "address" in params:
            sql += f"""_order.full_address = ?"""
            values += [params["address"]]
        else:
            one_param = False

        if one_param:
            sql += " \nAND "
        else:
            one_param = True

        if "amount" in params:
            sql += f"""_order.amount = ?"""
            values += [params["amount"]]
        else:
            one_param = False

        if one_param:
            sql += " \nAND "
        else:
            one_param = True

        if params["type"] != 0:
                sql += f"""_order._type_id = ?"""
                values += [params["type"]]
        else:
            one_param = False

        if one_param:
            sql += " \nAND "
        else:
            one_param = True

        if "order" in params:
            sql += f"""_order.order_number = ?"""
            values += [params["order"]]
        else:
            one_param = False

        if one_param:
            sql += " \nAND "
        else:
            one_param = True

        if "tracking" in params:
            sql += f"""_order.external_tracking = ?"""
            values += [params["tracking"]]
        else:
            one_param = False

        if one_param:
            sql += " \nAND \n"

        sql += "("
        # # # Status
        status_count = 0
        num_status = len(active_checkboxes_ids)
        if num_status > 0:
            for status_id in active_checkboxes_ids:
                sql += f"""_order._status_id = ?"""
                values += [status_id]
                status_count += 1
                if status_count < num_status:
                    sql += " \nOR "
        sql += ") \n"

        # Ordering
        sql += f"ORDER BY {params['header']}"

        if params['sort_type'] != 'ASC':
            sql += " DESC"

        sql += ";"

        orders = execute_query(sql, *values)
        MainModel.fill_order_tree(order_tree, orders)
        MainModel.store_tree_config(params)

    @staticmethod
    def clear_data(tree):
        for record in tree.get_children():
            tree.delete(record)

    @staticmethod
    def read_tree_config():
        return (read_tree_sorting(),
                read_tree_sorting_type(),
                read_tree_limit())

    @staticmethod
    def read_search_config(checkbox):
        return read_tree_status_filter(checkbox)

    @staticmethod
    def store_tree_config(params):
        store_tree_status_filter(params["status"])
        store_tree_sorting(params['header'])
        store_tree_sorting_type(params['sort_type'])
        store_tree_limit(params['limit'])

    @staticmethod
    def fill_order_tree(order_tree, record):
        MainModel.clear_data(order_tree)
        if len(record) > 0:
            MainModel.insert_formatted_columns(order_tree, record)


    @staticmethod
    def insert_formatted_columns(order_tree, record):
        # Specific columns index.
        col_guide = dict()
        col_guide['Amount'] = 25
        col_guide['Date'] = 26
        # Inserting formatted records with tags
        for row_index, row in enumerate(record):
            row_values = list()
            for col_index, col in enumerate(row):
                if col_index == col_guide['Amount']:
                    row_values.append(str("{:0.2f}".format(col/100)))
                    continue
                if col_index == col_guide['Date']:
                    col  = datetime.strptime(col, '%Y-%m-%d').\
                        strftime('%m/%d/%Y')
                    row_values.append(col)
                    continue
                if col == None:
                    row_values.append('')
                else:
                    row_values.append(col)
            order_tree.insert(parent='', index='end',
                  iid=row_index, text="",
                  tags=("textonly",),
                  values=tuple(row_values))

        order_tree.tag_configure("textonly",
                                 foreground="black",
                                 font = 'Arial 10')

    @staticmethod
    def open_order(order_tree):
        order = order_tree.item(order_tree.focus())
        _id = order["values"][21]
        filename = order["values"][29]
        if not blank_input(filename) and filename != "None":
            path =  os.getcwd() + \
                    read_attachment_partial_path() + \
                    filename
            try:
                os.startfile(path)
                logging.info(f"Operational: Order id {_id}. Successfully opened attachment"
                             f" \"{filename}\"")
            except FileNotFoundError:
                logging.critical(f"Operational: Failed opening of expected attachment file"
                                 f" \"{filename}\". File not found.")
        else:
            logging.warning(f"Operational: Order id {_id}. Order has no attachment. Opening file ignored.")

    @staticmethod
    def save_data(data):
        store_new_order(data)

    @staticmethod
    def get_name_of_all_companies():
        return get_name_of_all_companies()

    @staticmethod
    def get_all_projects(company_id):
        return get_all_projects(company_id)

    @staticmethod
    def get_name_of_all_employees():
        return get_name_of_all_employees()

    @staticmethod
    def get_all_statuses():
        return get_all_order_status()

    @staticmethod
    def get_all_supervisors():
        return get_name_of_all_supervisors()

    @staticmethod
    def get_all_employees():
        return get_name_of_all_employees()

    @staticmethod
    def get_all_types():
        return get_all_types()

    @staticmethod
    def prepare_emails(order_tree):
        selected_items = order_tree.selection()
        if not selected_items:
            return

        rows = list()
        for item in selected_items:
            row = order_tree.item(item)
            rows.append(row)

        keys = []
        for col in order_tree["columns"]:
            column_name = order_tree.column(col, option="id")
            keys.append(column_name)
        orders = list()
        for row in rows:
            values = row.get("values")
            orders.append(dict(zip(keys, values)))
        # Segregating orders by supervisor
        list_supervisors = list()
        orders_by_supervisor = list()
        for order in orders:
            if (order["supervisor.id"],
                order["supervisor._name"],
                order["supervisor.email"]) not in list_supervisors:
                list_supervisors.append((order["supervisor.id"],
                                         order["supervisor._name"],
                                         order["supervisor.email"]))

        threads = list()
        pythoncom.CoInitialize()
        # Single Application for all emails
        outlook = win32com.client.Dispatch('outlook.application')
        logging.info(f"Operational: Outlook application dispatch created")
        # Finding all orders for each supervisor, separating them by status and
        # using threads to generate each email for each supervisor.
        # For multithreading with Outlook it is needed to create a thread interface
        # which uses the main application and generates multiple Dispatch instances
        # Each instance can then be used to create and modify emails independently.
        # This approach speeds up the creation and modification of emails
        # by opening n queues for n emails
        for supervisor in list_supervisors:
            outlook_id = pythoncom.CoMarshalInterThreadInterfaceInStream(
                                            pythoncom.IID_IDispatch,
                                            outlook)
            logging.info(f"Operational: Outlook Interface {outlook_id} created")
            t = threading.Thread(target=MainModel.compose_email,
                                            args=(supervisor[0],
                                                  supervisor[1],
                                                  supervisor[2],
                                                  orders),
                                            kwargs={'outlook_id': outlook_id})
            logging.info(f"Threading: New thread created")
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        logging.info("Threading: All threads finished. Email draft creation is finished")

    @staticmethod
    def compose_email(supervisor_id, supervisor_name,
                      supervisor_email, orders, outlook_id):
        new_email = ComposedEmail(supervisor_name, supervisor_email)
        for order in orders:
            if order["supervisor.id"] == supervisor_id:
                order_status_id = order["order_status.id"]
                if order_status_id == 1:
                    new_email.add_paid_order(order)
                elif order_status_id == 2:
                    new_email.add_short_paid_order(order)
                elif order_status_id == 3:
                    new_email.add_approved_order(order)
                elif order_status_id == 4:
                    new_email.add_pre_approved_order(order)
                elif order_status_id == 5:
                    new_email.add_sent_order(order)
                elif order_status_id == 6:
                    new_email.add_not_paid_order(order)
                elif order_status_id == 7:
                    new_email.add_reviewing_order(order)
                elif order_status_id == 8:
                    new_email.add_not_sent_order(order)
                elif order_status_id == 9:
                    new_email.add_void_order(order)
                else:
                    raise ValueError

        new_email.create_email_draft(supervisor_id, outlook_id)

    @staticmethod
    def filter_options(combobox, options):
        if options:
            typed_text = combobox.get().lower()
            filtered_options = [option[1] for option in options if typed_text in option[1].lower()]
            combobox['values'] = filtered_options