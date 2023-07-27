from tkinter import *
from tkinter.constants import *
from tkinter.ttk import Combobox, Scrollbar, Treeview, Style
from tkcalendar import DateEntry
from helpers.input_validation import *
import datetime

class MainView:
    def __init__(self, root, controller, app_controller):
        self.root = root
        self.controller = controller
        self.app_controller = app_controller

        # FRAMES
        self.frame_search_menu1 = None
        self.frame_search_menu2 = None
        self.frame_search_menu3 = None
        self.frame_option_menu = None
        self.frame_order_area = None

        # Entry
        self.start_date_entry = None
        self.end_date_entry = None
        self.type_entry = None
        self.company_entry = None
        self.project_entry = None
        self.address_entry = None
        self.lotblk_entry = None
        self.order_entry = None
        self.amount_entry = None
        self.supervisor_entry = None
        self.tracking_entry = None
        self.status_data = None
        self.employee_entry = None

        # Data Tree
        self.order_tree = None
        self.order_tree_style = None
        self.order_tree_scroll_x = None
        self.order_tree_scroll_y = None

        # Checkbox - Filtering
        self.cb_paid = None
        self.cb_short_paid = None
        self.cb_approved = None
        self.cb_pre_approved = None
        self.cb_sent = None
        self.cb_not_paid = None
        self.cb_reviewing = None
        self.cb_not_sent = None
        self.cb_void = None

        # Checkbox - On/Off status
        self.cb_paid_status = None
        self.cb_short_paid_status = None
        self.cb_approved_status = None
        self.cb_pre_approved_status = None
        self.cb_sent_status = None
        self.cb_not_paid_status = None
        self.cb_reviewing_status = None
        self.cb_not_sent_status = None
        self.cb_void_status = None

        # Buttons
        self.btn_send_selected = None
        self.btn_add_order = None
        self.btn_modify_order = None
        self.btn_delete_order = None
        self.btn_search = None
        self.btn_clear = None

        # Var
        self.start_date_var = StringVar()
        self.end_date_var = StringVar()
        self.type_var = StringVar()
        self.company_var = StringVar()
        self.project_var = StringVar()
        self.status_var = StringVar()
        self.supervisor_var = StringVar()
        self.employee_var = StringVar()

        # Combobox Data
        self.supervisor_data = None
        self.employee_data = None
        self.company_data = None
        self.project_data = None
        self.type_data = None

        self.sort_by_header = None
        self.sort_type = None
        self.order_limit = None

    def show_ui(self):
        self.show_search_menu()
        self.show_option_menu()
        self.show_order_tree()
        self.search_now()

    @staticmethod
    def get_geometry(frame):
        geometry = frame.winfo_geometry()
        x_pos = int(geometry.split("+")[1])
        y_pos = int(geometry.split("+")[2])
        return x_pos, y_pos

    def refresh_list_of_orders(self):
        self.search_now()

    def fill_search_entries(self):
        self.supervisor_data = self.controller.get_supervisors()
        self.supervisor_data.insert(0,(0,"All"))
        self.employee_data = self.controller.get_employees()
        self.employee_data.insert(0, (0, "All"))
        self.company_data = self.controller.get_companies()
        self.company_data.insert(0,(0,"All"))
        self.status_data = self.controller.get_statuses()
        self.status_data.insert(0,(0,"All"))
        self.type_data = self.controller.get_types()
        self.type_data.insert(0,(0,"All"))

        default_start_date = datetime.date.today().replace(month=1, day=1)
        self.start_date_entry.set_date(default_start_date)
        self.end_date_entry.set_date(datetime.date.today())
        self.supervisor_entry['values'] = [value[1] for value in self.supervisor_data]
        self.employee_entry['values'] = [value[1] for value in self.employee_data]
        self.company_entry['values'] = [value[1] for value in self.company_data]
        self.project_entry['values'] = [('All')]
        self.type_entry['values'] = [value[1] for value in self.type_data]

        self.supervisor_entry.current(0)
        self.employee_entry.current(0)
        self.company_entry.current(0)
        self.project_entry.current(0)
        self.type_entry.current(0)

        self.supervisor_entry.event_generate("<<ComboboxSelected>>")
        self.employee_entry.event_generate("<<ComboboxSelected>>")
        self.company_entry.event_generate("<<ComboboxSelected>>")
        self.project_entry.event_generate("<<ComboboxSelected>>")
        self.type_entry.event_generate("<<ComboboxSelected>>")

    def show_search_menu(self):
        self.frame_search_menu1 = Frame(self.root, height=38)
        self.frame_search_menu2 = Frame(self.root, height=38)
        self.frame_search_menu3 = Frame(self.root, height=38)
        self.frame_search_menu1.pack(fill="x")
        self.frame_search_menu2.pack(fill="x")
        self.frame_search_menu3.pack(fill="x")

        # Doesn't let the children widget modify the frame size
        self.frame_search_menu1.pack_propagate(False)
        self.frame_search_menu2.pack_propagate(False)
        self.frame_search_menu3.pack_propagate(False)

        # Search
        # Labels Col 1 (LHS)
        label_font = 'Arial 10 bold'
        start_date_label = Label(self.frame_search_menu1, text="Start Date:",
                                 font=label_font)
        end_date_label = Label(self.frame_search_menu1, text="End Date:",
                               font=label_font)
        supervisor_label = Label(self.frame_search_menu1, text="Supervisor:",
                                 font=label_font)
        employee_label = Label(self.frame_search_menu1, text="Employee:",
                                font=label_font)
        company_label = Label(self.frame_search_menu1, text="Company:",
                              font=label_font)
        project_label = Label(self.frame_search_menu1, text="Project:",
                                font=label_font)
        lot_blk_label = Label(self.frame_search_menu2, text="Lot/Blk:",
                              font=label_font)
        address_label = Label(self.frame_search_menu2, text="Address:",
                              font=label_font)
        amount_label = Label(self.frame_search_menu2, text="Amount:   $",
                             font=label_font)
        type_label = Label(self.frame_search_menu2, text="Type:",
                           font=label_font)
        order_label = Label(self.frame_search_menu2, text="Order#:",
                            font=label_font)
        tracking_label = Label(self.frame_search_menu2, text="Tracking#:",
                               font=label_font)

        # Entry Setup
        self.start_date_entry = DateEntry(self.frame_search_menu1, selectmode='night',
                                          date_pattern='mm/dd/yyyy',
                                          textvariable=self.start_date_var)
        self.end_date_entry = DateEntry(self.frame_search_menu1, selectmode='night',
                                        date_pattern='mm/dd/yyyy',
                                        textvariable=self.end_date_var)
        self.supervisor_entry = Combobox(self.frame_search_menu1, width=27,
                                         height=40, textvariable=self.supervisor_var)
        self.employee_entry = Combobox(self.frame_search_menu1, width=27, height=40,
                                       textvariable=self.employee_var)
        self.company_entry = Combobox(self.frame_search_menu1,
                                      width=27, height=40, textvariable=self.company_var)
        self.project_entry = Combobox(self.frame_search_menu1,
                                      width=27, height=40, textvariable=self.project_var,
                                      state="disabled")
        self.lotblk_entry = Entry(self.frame_search_menu2, bd=2, width=15,
                                     font='Arial 10 normal')
        self.address_entry = Entry(self.frame_search_menu2, bd=2, width=33,
                                      font='Arial 10 normal')
        self.amount_entry = Entry(self.frame_search_menu2, bd=2, width=12,
                                     font='Arial 10 normal')
        self.type_entry = Combobox(self.frame_search_menu2, width=12, height=40,
                                   textvariable=self.type_var)
        self.order_entry = Entry(self.frame_search_menu2, bd=2, width=15,
                                    font='Arial 10 normal')
        self.tracking_entry = Entry(self.frame_search_menu2, bd=2, width=15,
                                       font='Arial 10 normal')

        self.fill_search_entries()
        self.clear_search()

        # Resetting list of options when one is selected
        self.type_entry.bind('<<ComboboxSelected>>',
                             lambda x: self.set_entry_options(self.type_entry, self.type_data))
        self.company_entry.bind('<<ComboboxSelected>>',
                             lambda x: (self.set_entry_options(self.company_entry, self.company_data),
                                        self.on_search_company_selected()))
        self.project_entry.bind('<<ComboboxSelected>>',
                             lambda x:  (self.set_entry_options(self.project_entry, self.project_data),
                                         self.on_search_project_selected()))
        self.supervisor_entry.bind('<<ComboboxSelected>>',
                             lambda x: self.set_entry_options(self.supervisor_entry, self.supervisor_data))
        self.employee_entry.bind('<<ComboboxSelected>>',
                             lambda x: self.set_entry_options(self.employee_entry, self.employee_data))

        self.type_var.trace('w',self.on_type_input)
        self.company_var.trace('w', self.on_company_input)
        self.project_var.trace('w', self.on_project_input)
        self.supervisor_var.trace('w',self.on_supervisor_input)
        self.employee_var.trace('w',self.on_employee_input)

        #First Frame
        start_date_label.pack(side="left")
        self.start_date_entry.pack(side="left", padx=(0,30))
        end_date_label.pack(side="left")
        self.end_date_entry.pack(side="left", padx=(0,30))
        supervisor_label.pack(side="left", padx=(137,0))
        self.supervisor_entry.pack(side="left", padx=(0,30))
        employee_label.pack(side="left")
        self.employee_entry.pack(side="left", padx=(0, 30))
        company_label.pack(side="left")
        self.company_entry.pack(side="left", padx=(0,30))
        project_label.pack(side="left")
        self.project_entry.pack(side="left", padx=(0, 30))

        # Second Frame
        lot_blk_label.pack(side="left")
        self.lotblk_entry.pack(side="left", padx=(0,30))
        address_label.pack(side="left")
        self.address_entry.pack(side="left", padx=(0,30))
        amount_label.pack(side="left")
        self.amount_entry.pack(side="left", padx=(0,30))
        type_label.pack(side="left", padx=(0,30))
        self.type_entry.pack(side="left", padx=(0,30))
        order_label.pack(side="left")
        self.order_entry.pack(side="left", padx=(0,30))
        tracking_label.pack(side="left")
        self.tracking_entry.pack(side="left", padx=(0,30))

        # Buttons
        self.btn_search = Button(self.frame_search_menu2, text="Search",
                            font=("Arial", 10), height=1, width=9)

        self.btn_clear = Button(self.frame_search_menu2, text="Clear",
                                font=("Arial", 10), height=1, width=9)

        self.btn_search.configure(command=self.search_now)
        self.btn_clear.configure(command=self.clear_search)
        self.btn_clear.pack(side="right", padx=(0,50))
        self.btn_search.pack(side="right")

        self.btn_search.bind_all('<Alt-Return>', lambda event: self.search_now())
        self.btn_search.bind_all('<Alt-BackSpace>', lambda event: self.clear_search())

        # Checkboxes Declaration, Positioning, Value, and Event

        # PAID. Database id=1
        get_cbox_value = self.controller.read_search_checkbox_config
        self.cb_paid = Checkbutton(self.frame_search_menu3, text='Paid',
                                      onvalue=True, offvalue=False, font=("Arial", 12))
        self.cb_paid_status = BooleanVar(value=get_cbox_value(1))
        self.cb_paid.configure(variable=self.cb_paid_status)
        # SHORT_PAID. Database id=2
        checkbox_font = ("Arial", 12)
        self.cb_short_paid = Checkbutton(self.frame_search_menu3, text='Short-Paid',
                                            onvalue=True, offvalue=False,
                                            font=checkbox_font)
        self.cb_short_paid_status = BooleanVar(value=get_cbox_value(2))
        self.cb_short_paid.configure(variable= self.cb_short_paid_status)
        # APPROVED. Database id=3
        self.cb_approved = Checkbutton(self.frame_search_menu3, text='Approved',
                                          onvalue=True, offvalue=False,
                                          font=checkbox_font)
        self.cb_approved_status = BooleanVar(value=get_cbox_value(3))
        self.cb_approved.configure(variable=self.cb_approved_status)
        # PRE_APPROVED. Database id=4
        self.cb_pre_approved = Checkbutton(self.frame_search_menu3, text='Pre-Approved',
                                          onvalue=True, offvalue=False,
                                          font=checkbox_font)
        self.cb_pre_approved_status = BooleanVar(value=get_cbox_value(4))
        self.cb_pre_approved.configure(variable=self.cb_pre_approved_status)
        # SENT. Database id=5
        self.cb_sent = Checkbutton(self.frame_search_menu3, text='Sent',
                                          onvalue=True, offvalue=False,
                                          font=checkbox_font)
        self.cb_sent_status = BooleanVar(value=get_cbox_value(5))
        self.cb_sent.configure(variable=self.cb_sent_status)
        # NOT_PAID. Database id=6
        self.cb_not_paid = Checkbutton(self.frame_search_menu3, text='Not-Paid',
                                          onvalue=True, offvalue=False,
                                          font=checkbox_font)
        self.cb_not_paid_status = BooleanVar(value=get_cbox_value(6))
        self.cb_not_paid.configure(variable=self.cb_not_paid_status)
        # REVIEWING. Database id=7
        self.cb_reviewing = Checkbutton(self.frame_search_menu3, text='Reviewing',
                                           onvalue=True, offvalue=False,
                                           font=checkbox_font)
        self.cb_reviewing_status = BooleanVar(value=get_cbox_value(7))
        self.cb_reviewing.configure(variable=self.cb_reviewing_status)
        # NOT_SENT. Database id=8
        self.cb_not_sent = Checkbutton(self.frame_search_menu3, text='Not-Sent',
                                          onvalue=True, offvalue=False,
                                          font=checkbox_font)
        self.cb_not_sent_status = BooleanVar(value=get_cbox_value(8))
        self.cb_not_sent.configure(variable=self.cb_not_sent_status)
        # VOID. Database id=9
        self.cb_void = Checkbutton(self.frame_search_menu3, text='Void',
                                          onvalue=True, offvalue=False,
                                          font=checkbox_font)
        self.cb_void_status = BooleanVar(value=get_cbox_value(9))
        self.cb_void.configure(variable=self.cb_void_status)

        self.cb_paid.grid(row=0, column=1, padx=(0,30))
        self.cb_short_paid.grid(row=0, column=2, padx=(0,30))
        self.cb_approved.grid(row=0, column=3, padx=(0,30))
        self.cb_pre_approved.grid(row=0, column=4, padx=(0,30))
        self.cb_sent.grid(row=0, column=5, padx=(0,30))
        self.cb_not_paid.grid(row=0, column=6, padx=(0,30))
        self.cb_reviewing.grid(row=0, column=7, padx=(0,30))
        self.cb_not_sent.grid(row=0, column=8, padx=(0,30))
        self.cb_void.grid(row=0, column=9, padx=(0,30))

    def show_option_menu(self):
        self.frame_option_menu = Frame(self.root, height=28)
        self.frame_option_menu.pack(fill="x")
        self.frame_option_menu.pack_propagate(False)  # Doesn't let the children widget modify the frame size

        # Buttons
        button_font = ('arial', 12, 'normal')
        self.btn_add_order = Button(self.frame_option_menu,
                                        text='Add',
                                        font= button_font,
                                        command=self.app_controller.new_order)

        self.btn_modify_order = Button(self.frame_option_menu,
                                        text='Modify',
                                        font= button_font,
                                        command=self.app_controller.modify_order)
        self.btn_delete_order = Button(self.frame_option_menu,
                                        text='Delete',
                                        font= button_font,
                                        command=self.app_controller.delete_order)
        self.btn_send_selected = Button(self.frame_option_menu,
                                        text="Send Selected",
                                        font= button_font,
                                        command=self.callback_send_selected_order)

        self.btn_delete_order.pack(side='right')
        self.btn_modify_order.pack(side='right')
        self.btn_add_order.pack(side='right')
        self.btn_send_selected.pack(side='right')

        self.btn_modify_order.bind_all('<Alt-Button-1>',
                       lambda event:self.app_controller.modify_order())

    def show_order_tree(self):
        # Frame Work Area Right Side
        self.frame_order_area = Frame(self.root)
        self.frame_order_area.pack(fill="both", expand=True)
        # Prevents children widget to modify the frame size
        self.frame_order_area.pack_propagate(False)
        # Scrollbars
        self.order_tree_scroll_x = Scrollbar(self.frame_order_area,
                                             orient=HORIZONTAL)
        self.order_tree_scroll_x.pack(side=BOTTOM,
                                      fill=X)
        self.order_tree_scroll_y = Scrollbar(self.frame_order_area,
                                             orient=VERTICAL)
        self.order_tree_scroll_y.pack(side=RIGHT,
                                      fill=Y)
        # Tree Instance
        self.order_tree = Treeview(self.frame_order_area,
                                       xscrollcommand=self.order_tree_scroll_x.set,
                                       yscrollcommand=self.order_tree_scroll_y.set)
        self.order_tree_scroll_x.config(command=self.order_tree.xview)
        self.order_tree_scroll_y.config(command=self.order_tree.yview)

        # Columns
        self.order_tree['columns'] = ("supervisor.id",
                    "supervisor._name",
                    "supervisor.phone_number",
                    "supervisor.email",
                    "employee.id",
                    "employee._name",
                    "employee.phone_number",
                    "employee.email",
                    "company.id",
                    "company._name",
                    "division.id",
                    "division._name",
                    "division.location",
                    "division.accounts_payable_name",
                    "division.accounts_payable_email",
                    "project.id",
                    "project._name",
                    "order_type.id",
                    "order_type._type",
                    "order_status.id",
                    "order_status._status",
                    "_order.id",
                    "_order.unit_address",
                    "_order.full_address",
                    "_order.order_number",
                    "_order.amount",
                    "_order._date",
                    "_order.external_tracking",
                    "_order.note",
                    "_order.attachment_name")
        # Columns
        self.order_tree.column("#0", width=0, stretch=NO)  # Ghost Column... used for parent/child
        self.order_tree.column("_order._date", anchor=CENTER, width=10)
        self.order_tree.column("supervisor._name", anchor=W, width=40)
        self.order_tree.column("employee._name", anchor=W, width=30)
        self.order_tree.column("order_status._status", anchor=CENTER, width=25)
        self.order_tree.column("order_type._type", anchor=W, width=15)
        self.order_tree.column("company._name", anchor=W, width=50)
        self.order_tree.column("project._name", anchor=W, width=60)
        self.order_tree.column("_order.unit_address", anchor=W, width=10)
        self.order_tree.column("_order.full_address", anchor=W, width=70)
        self.order_tree.column("_order.order_number", anchor=CENTER, width=8)
        self.order_tree.column("_order.amount", anchor=E, width=10)
        self.order_tree.column("_order.external_tracking", anchor=W, width=25)
        self.order_tree.column("_order.note", anchor=W, width=60)
        # Headings
        self.order_tree.heading("#0", text="", anchor=CENTER)
        self.order_tree.heading("_order._date", text="Date", anchor=CENTER,
                                command=lambda: self.sort_tree("_order._date"))
        self.order_tree.heading("supervisor._name", text="Supervisor", anchor=CENTER,
                                command=lambda: self.sort_tree("supervisor._name"))
        self.order_tree.heading("employee._name", text="Employee", anchor=CENTER,
                                command=lambda: self.sort_tree("employee._name"))
        self.order_tree.heading("order_status._status", text="Status", anchor=CENTER,
                                command=lambda: self.sort_tree("order_status._status"))
        self.order_tree.heading("order_type._type", text="Type", anchor=CENTER,
                                command=lambda: self.sort_tree("order_type._type"))
        self.order_tree.heading("company._name", text="Company", anchor=CENTER,
                                command=lambda: self.sort_tree("company._name"))
        self.order_tree.heading("project._name", text="Project", anchor=CENTER,
                                command=lambda: self.sort_tree("project._name"))
        self.order_tree.heading("_order.unit_address", text="Lot/Blk", anchor=CENTER,
                                command=lambda: self.sort_tree("_order.unit_address"))
        self.order_tree.heading("_order.full_address", text="Address", anchor=CENTER,
                                command=lambda: self.sort_tree("_order.full_address"))
        self.order_tree.heading("_order.order_number", text="Order#", anchor=CENTER,
                                command=lambda: self.sort_tree("_order.order_number"))
        self.order_tree.heading("_order.amount", text="Amount", anchor=CENTER,
                                command=lambda: self.sort_tree("_order.amount"))
        self.order_tree.heading("_order.external_tracking", text="Tracking No.", anchor=CENTER,
                                command=lambda: self.sort_tree("_order.external_tracking"))
        self.order_tree.heading("_order.note", text="Note", anchor=CENTER,
                                command=lambda: self.sort_tree("_order.note"))
        # Visible Columns
        self.order_tree['displaycolumns'] = ("_order._date",
                                             "supervisor._name",
                                             "employee._name",
                                             "order_status._status",
                                             "order_type._type",
                                             "company._name",
                                             "project._name",
                                             "_order.unit_address",
                                             "_order.full_address",
                                             "_order.order_number",
                                             "_order.amount",
                                             "_order.external_tracking",
                                             "_order.note")
        self.order_tree.pack(fill='both', expand=True)

        self.order_tree_style = Style()
        self.order_tree_style.theme_use("clam")
        self.order_tree_style.configure("Treeview",
                             background="#c7c7c7",  # Bg when there are orders
                             foreground="white",  #
                             fieldbackground="white",
                             rowheight=25)

        # Change selected color. This is a requirement to make config  work.
        self.order_tree_style.map('Treeview',
                       background=[('selected', '#518aed')])  # Color of selected

        # Bind click event to custom tag
        self.order_tree.tag_bind("textonly", "<Double-Button-1>",
                                 self.open_order_attachment)

        tree_config = self.controller.read_tree_config()
        self.sort_by_header = tree_config[0]
        self.sort_type = tree_config[1]
        self.order_limit = tree_config[2]

    # Callbacks and Events
    def open_order_attachment(self, *args):
        self.controller.open_order(self.order_tree)

    # Returns list of all orders selected
    def get_selected_orders_id(self,):
        index_selected_items = self.order_tree.selection()
        list_of_orders = list()
        for each_item in index_selected_items:
            # Id is index 21 on tree.
            list_of_orders.append(self.order_tree.item(each_item)["values"][21])
        return list_of_orders

    def sort_tree(self, new_header):
        if self.sort_by_header == new_header:
            if self.sort_type == 'ASC':
                self.sort_type = 'DESC'
            else:
                self.sort_type = 'ASC'
        else:
            self.sort_by_header = new_header
        self.controller.refresh_view()

    def fill_order_tree(self, params):
        self.controller.fill_order_tree(self.order_tree, params)

    def search_now(self):
        search_params={}
        # Start Date
        start_date = self.start_date_entry.get()
        if not validate_date(start_date):
            start_date = datetime.date.today().replace(month=1, day=1)
        else:
            start_date = datetime.datetime.strptime(
                    start_date, '%m/%d/%Y').strftime('%Y-%m-%d')
        search_params["start_date"] = str(start_date)

        # End Date
        end_date = self.end_date_entry.get()
        if not validate_date(end_date):
            end_date = datetime.date.today()
        else:
            end_date = datetime.datetime.strptime(
                    end_date, '%m/%d/%Y').strftime('%Y-%m-%d')
        search_params["end_date"] = str(end_date)

        # Supervisor
        try:
            # Error when if no selection (-1)
            if self.supervisor_entry.current() < 0:
                raise ValueError
            supervisor_id = int(self.supervisor_data[self. \
                                supervisor_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            pass
        else:
            search_params["supervisor"] = supervisor_id

        # Employee
        try:
            # Error when if no selection (-1)
            if self.employee_entry.current() < 0:
                raise ValueError
            employee_id = int(self.employee_data[self. \
                               employee_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            pass
        else:
            search_params["employee"] = employee_id

        # Project
        try:
            # Error when if no selection(-1)
            if self.project_entry.current() < 0:
                raise ValueError
            project_id = int(self.project_data[self. \
                               project_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            search_params["project"] = 0
        else:
            search_params["project"] = project_id

        # Lot/Blk
        lotblk = self.lotblk_entry.get()
        if not blank_input(lotblk):
            search_params["lot_blk"] = str(lotblk)

        # Address
        address = self.address_entry.get()
        if not blank_input(address):
            search_params["address"] = str(address)

       # Amount
        amount = self.amount_entry.get()
        try:
            if not blank_input(amount):
                amount = re.sub(r',', '', self.amount_entry.get())
                amount = int(float(amount) * 100.00)
                search_params["amount"] = amount
        except ValueError:
            pass

        # Type
        try:
            # Error when if no selection(-1)
            if self.type_entry.current() < 0:
                raise ValueError
            type_id = int(self.type_data[self.\
                type_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            pass
        else:
            search_params["type"] = type_id

        # Order
        order_no = self.order_entry.get()
        if not blank_input(order_no) and validate_all_numbers(order_no):
            search_params["order"] = order_no

        # Tracking
        tracking = self.tracking_entry.get()
        if not blank_input(tracking):
            search_params["tracking"] = tracking

        checkbox = {'1': self.cb_paid_status.get(),
                    '2': self.cb_short_paid_status.get(),
                    '3': self.cb_approved_status.get(),
                    '4': self.cb_pre_approved_status.get(),
                    '5': self.cb_sent_status.get(),
                    '6': self.cb_not_paid_status.get(),
                    '7': self.cb_reviewing_status.get(),
                    '8': self.cb_not_sent_status.get(),
                    '9': self.cb_void_status.get()}

        search_params["status"] = checkbox
        search_params["header"] = self.sort_by_header
        search_params["sort_type"] = self.sort_type
        search_params["limit"] = self.order_limit
        self.controller.fill_order_tree(self.order_tree, search_params)

    def clear_search(self):
        default_start_date = datetime.date.today().replace(month=1, day=1)
        self.start_date_entry.set_date(default_start_date)
        self.end_date_entry.set_date(datetime.date.today())

        self.type_entry.current(0)
        self.lotblk_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.amount_entry.delete(0, END)
        self.order_entry.delete(0, END)
        self.tracking_entry.delete(0, END)

        self.fill_search_entries()
        self.project_entry.config(state="disabled")

    def callback_send_selected_order(self):
        self.controller.send_orders(self.order_tree)

    def destroy_view(self):
        frames = [self.frame_search_menu1,
                  self.frame_search_menu2,
                  self.frame_search_menu3,
                  self.frame_option_menu,
                  self.frame_order_area]
        for frame in frames:
            for widgets in frame.winfo_children():
                widgets.destroy()
            frame.destroy()

    @staticmethod
    def destroy_frame(frame):
        for widgets in frame.winfo_children():
            widgets.destroy()
        frame.destroy()

    def set_entry_options(self, entry, data):
        entry['values'] = [value[1] for value in data]

    def on_type_input(self, *args):
        self.controller.filter_options(self.type_entry, self.type_data)

    def on_company_input(self, *args):
        self.controller.filter_options(self.company_entry, self.company_data)

    def on_project_input(self, *args):
        self.controller.filter_options(self.project_entry, self.project_data)

    def on_supervisor_input(self, *args):
        self.controller.filter_options(self.supervisor_entry, self.supervisor_data)

    def on_employee_input(self, *args):
        self.controller.filter_options(self.employee_entry, self.employee_data)

    def on_search_company_selected(self, *args):
        selected_company_id = self.company_data[self.company_entry.current()][0]
        self.project_data = self.controller. \
            get_projects_for_company(selected_company_id)
        self.set_entry_options(self.project_entry,self.project_data)

        # If there is no project set project as "All"
        if len(self.project_entry['values']) == 0:
            self.project_entry['values'] = [('All')]
            self.project_entry.current(0)
            self.project_entry.config(state="disabled")
        # Trigger update on dropdown
        self.project_entry.current(0)
        self.project_entry.event_generate("<<ComboboxSelected>>")
        self.set_entry_options(self.project_entry, self.project_data)
        self.on_search_project_selected()

    def on_search_project_selected(self, *args):
        if len(self.project_entry['values']) > 0 and \
                self.project_entry['values'][0] != "All":
            self.project_entry.config(state='normal')