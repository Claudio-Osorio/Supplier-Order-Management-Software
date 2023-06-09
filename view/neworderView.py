import logging
from tkinter import *
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from helpers.input_validation import *
import os
import datetime

class NewOrderView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.win = None

        # Objects
        self.date_entry = None
        self.type_entry = None
        self.company_entry = None
        self.project_entry = None
        self.address_entry = None
        self.lotblk_entry = None
        self.order_entry = None
        self.amount_entry = None
        self.supervisor_entry = None
        self.status_entry = None
        self.employee_entry = None
        self.note_text = None
        self.et_entry = None
        self.attachment_entry = None
        self.btn_select_attachment = None

        # Var
        self.date_var = StringVar()
        self.type_var = StringVar()
        self.company_var = StringVar()
        self.project_var = StringVar()
        self.status_var = StringVar()
        self.supervisor_var = StringVar()
        self.employee_var = StringVar()

        # Data
        self.type_data = None
        self.company_data = None
        self.project_data = None
        self.employee_data = None
        self.supervisor_data = None
        self.status_data = None

        self.error_label = None

        self.btn_save = None
        self.btn_cancel = None

    def show_ui(self):
        self.win = Toplevel(self.root)
        self.win.geometry("800x550+550+280")
        self.win.resizable(False, False)
        self.win.attributes("-toolwindow", 1)
        self.win.grab_set()
        self.win.title("Add New Order")

        # Labels Col 1 (LHS)
        Label(self.win, text="Date:", font='Arial 12 bold').\
            place(x=25, y=20)
        Label(self.win, text="Company:", font='Arial 12 bold').\
            place(x=25, y=70)
        Label(self.win, text="Lot/Blk:", font='Arial 12 bold').\
            place(x=25, y=120)
        Label(self.win, text="Amount:   $", font='Arial 12 bold').\
            place(x=25, y=170)
        Label(self.win, text="Employee:", font='Arial 12 bold').\
            place(x=25, y=220)
        Label(self.win, text="Status:", font='Arial 12 bold').\
            place(x=25, y=270)
        Label(self.win, text="Attachment:", font='Arial 12 bold').\
            place(x=25, y=320)

        # Labels Col 2 (RHS)
        Label(self.win, text="Type:", font='Arial 12 bold').\
            place(x=350, y=20)
        Label(self.win, text="Project:", font='Arial 12 bold').\
            place(x=350, y=70)
        Label(self.win, text="Address:", font='Arial 12 bold').\
            place(x=350, y=120)
        Label(self.win, text="Order#:", font='Arial 12 bold').\
            place(x=350, y=170)
        Label(self.win, text="Supervisor:", font='Arial 12 bold').\
            place(x=350, y=220)
        Label(self.win, text="Tracking#:", font='Arial 12 bold').\
            place(x=350, y=270)
        Label(self.win, text="Note:", font='Arial 12 bold').\
            place(x=350, y=320)

        # Entry Setup
        self.date_entry = DateEntry(self.win, selectmode='night',
                                    date_pattern='mm/dd/yyyy',
                                    textvariable=self.date_var)
        self.type_entry = Combobox(self.win, width=10, height=40,
                      textvariable=self.type_var)
        self.company_entry = Combobox(self.win,
                      width=27, height=40, textvariable=self.company_var)
        self.project_entry = Combobox(self.win,
                                      width=27, height=40, textvariable=self.project_var,
                                      state="disabled")
        self.address_entry = Entry(self.win, bd=2, width=33,
                                      font='Arial 12 normal')
        self.lotblk_entry = Entry(self.win, bd=2, width=15,
                                     font='Arial 12 normal')
        self.order_entry = Entry(self.win, bd=2, width=15,
                                    font='Arial 12 normal')
        self.amount_entry = Entry(self.win, bd=2, width=12,
                                     font='Arial 12 normal')
        self.supervisor_entry = Combobox(self.win, width=27,
                        height=40, textvariable=self.supervisor_var)
        self.et_entry = Entry(self.win, bd=2, width=15,
                                     font='Arial 12 normal')
        self.employee_entry = Combobox(self.win,
                                       width=27, height=40, textvariable=self.employee_var)
        self.status_entry = Combobox(self.win, width=27, height=40,
                         textvariable=self.status_var)
        self.attachment_entry = Entry(self.win, bd=2, width=15,
                         font='Arial 10 normal', state='normal')
        self.btn_select_attachment = Button(self.win, text="Import",
                    font=("Arial", 9), height=1, width=6,
                    command=self.select_attachment)
        self.note_text = Text(self.win, bd=2, width=40, height=4,
                         font='Arial 12 normal', warp=None)

        # Entry Data Preset
        self.company_data = self.controller.get_companies()
        self.set_entry_options(self.company_entry, self.company_data)

        self.project_entry['values'] = [('Select a company first')]
        self.project_entry.current(0)

        self.status_data = self.controller.get_statuses()
        self.set_entry_options(self.status_entry, self.status_data)

        self.type_data = self.controller.get_types()
        self.set_entry_options(self.type_entry, self.type_data)

        self.supervisor_data = self.controller.get_supervisors()
        self.set_entry_options(self.supervisor_entry, self.supervisor_data)

        self.employee_data = self.controller.get_employees()
        self.set_entry_options(self.employee_entry, self.employee_data)

        self.attachment_entry.insert(0, 'None')
        self.attachment_entry.config(state='readonly')

        # Triggers
        self.type_var.trace('w',self.on_type_input)
        self.company_var.trace('w', self.on_company_input)
        self.project_var.trace('w', self.on_project_input)
        self.status_var.trace('w',self.on_status_input)
        self.supervisor_var.trace('w',self.on_supervisor_input)
        self.employee_var.trace('w',self.on_employee_input)

        # Resetting list of options when one is selected
        self.type_entry.bind('<<ComboboxSelected>>',
                             lambda x: self.set_entry_options(self.type_entry, self.type_data))
        self.company_entry.bind('<<ComboboxSelected>>',
                             lambda x: (self.set_entry_options(self.company_entry, self.company_data),
                                        self.on_company_selected()))
        self.project_entry.bind('<<ComboboxSelected>>',
                             lambda x:  (self.set_entry_options(self.project_entry, self.project_data),
                                         self.on_project_selected()))
        self.status_entry.bind('<<ComboboxSelected>>',
                             lambda x: self.set_entry_options(self.status_entry, self.status_data))
        self.supervisor_entry.bind('<<ComboboxSelected>>',
                             lambda x: self.set_entry_options(self.supervisor_entry, self.supervisor_data))
        self.employee_entry.bind('<<ComboboxSelected>>',
                             lambda x: self.set_entry_options(self.employee_entry, self.employee_data))

        # Column 1 (LHS)
        self.date_entry.place(x=120, y=20)
        self.company_entry.place(x=120, y=70)
        self.lotblk_entry.place(x=120, y=120)
        self.amount_entry.place(x=120, y=170)
        self.employee_entry.place(x=120, y=223)
        self.status_entry.place(x=120, y=270)
        self.attachment_entry.place(x=124, y=322)
        self.btn_select_attachment.place(x=243, y=320)

        # Column 2 (RHS)
        self.type_entry.place(x=460, y=20)
        self.project_entry.place(x=460, y=70)
        self.address_entry.place(x=460, y=120)
        self.order_entry.place(x=460, y=170)
        self.supervisor_entry.place(x=460, y=220)
        self.et_entry.place(x=460, y=270)
        self.note_text.place(x=353, y=345)

        self.btn_save = Button(self.win, text="Save", font=("Arial", 12),
                          height=1, width=9,command= self.store_data)

        self.btn_cancel = Button(self.win, text="Cancel", font=("Arial", 12),
                            height=1, width=9, command= self.exit_window)

        self.btn_save.place(x=311, y=480)
        self.btn_cancel.place(x=402, y=480)

    def set_entry_options(self, entry, data):
        entry['values'] = [value[1] for value in data]

    def on_type_input(self, *args):
        self.controller.filter_options(self.type_entry, self.type_data)

    def on_company_input(self, *args):
        self.controller.filter_options(self.company_entry, self.company_data)

    def on_project_input(self, *args):
        self.controller.filter_options(self.project_entry, self.project_data)

    def on_status_input(self, *args):
        self.controller.filter_options(self.status_entry, self.status_data)

    def on_supervisor_input(self, *args):
        self.controller.filter_options(self.supervisor_entry, self.supervisor_data)

    def on_employee_input(self, *args):
        self.controller.filter_options(self.employee_entry, self.employee_data)

    # Updates project scope to only show data for selected company
    # Updates employee based on predefined project
    def on_company_selected(self):
        if self.company_entry.current() != -1:
            # Get Projects if a company is selected
            selected_company_id=self.company_data[self.company_entry.current()][0]
            self.project_data = self.controller.\
                get_projects_for_company(selected_company_id)

            # Removes potential disabled and instructions from entry
            self.project_entry.config(state="normal")
            self.set_entry_options(self.project_entry, self.project_data)
        else:
            # If there is no company selected or no project then set project as "None"
            self.project_entry['values'] = []

        if len(self.project_entry['values']) == 0:
            self.project_entry['values'] = [('None')]
            self.project_entry.current(0)
            self.project_entry.config(state="disabled")
        else:
            self.project_entry.config(state="normal")
            self.project_entry.current(0)
            self.project_entry.event_generate("<<ComboboxSelected>>")
            self.set_entry_options(self.project_entry, self.project_data)

    def on_project_selected(self, *arg):
        selected_project_id = self.project_data[self.project_entry.current()][0]
        try:
            preferred_employee_id = self.controller.get_preferred_employee(selected_project_id)
            index = -1
            for employee_id, employee in self.employee_data:
                index += 1
                if employee_id == preferred_employee_id:
                    break
            self.set_entry_options(self.employee_entry, self.employee_data)
            self.employee_entry.current(index)
            self.employee_entry.event_generate("<<ComboboxSelected>>")
        except Exception as e:
            logging.critical(f"""Project id {selected_project_id} has no preferred
             employee set. Presetting employee failed.""")

    def store_data(self):
        if self.error_label is not None:
            self.error_label.destroy()

        data = dict()
        if self.validate_data(data):
            self.controller.save_data(data)
            self.exit_window()
            self.controller.refresh_orders()

    def validate_data(self, data):
        valid_record = True
        error_msg = str()

        # DATE
        date = self.date_entry.get()
        if blank_input(date):
            error_msg += "*Date field cannot be blank\n"
        elif validate_date(date):
            date = datetime.datetime.strptime(
                date, '%m/%d/%Y').strftime('%Y-%m-%d')
            data["_date"] = date
        else:
            error_msg += "*The Date entered is invalid\n"
            valid_record = False

        # STATUS
        try:
            # Error when if no selection(-1)
            if self.status_entry.current() < 0:
                raise ValueError
            status = int(self.status_data[self.status_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            error_msg += "*A Status must be selected\n"
            valid_record = False
        else:
            data["_status_id"] = status

        # COMPANY
        try:
            # Error when if no selection(-1)
            if self.company_entry.current() < 0:
                raise ValueError
            company_id = int(self.company_data[self.\
                company_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            error_msg += "*A Company must be selected\n"
            valid_record = False

        # PROJECT
        try:
            # Error when if no selection(-1)
            if self.project_entry.current() < 0:
                raise ValueError
            project_id = int(self.project_data[self. \
                               project_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            error_msg += "*A Project must be selected\n"
            valid_record = False
        else:
            data["project_id"] = project_id

        # LOT/BLK
        lotblk = self.lotblk_entry.get()
        address = self.address_entry.get()
        if blank_input(lotblk) and\
                blank_input(address):
            error_msg += "*A Lot/Blk OR Address must be provided\n"
            valid_record = False
        else:
            if not blank_input(lotblk):
                if validate_by_regex(lotblk, r"^[a-zA-Z0-9\s\/\-\,]*"):
                        data["unit_address"] = str(lotblk)
                else:
                    error_msg += "*The Lot/Blk field cannot contain special characters\n"
                    valid_record = False
            else:
                data["unit_address"] = None

            if not blank_input(address):
                if validate_address(address):
                    data["full_address"] = str(address)
                else:
                    error_msg += "*The Address field cannot contain special characters\n"
                    valid_record = False
            else:
                data["full_address"] = None

        # AMOUNT
        amount = self.amount_entry.get()
        if blank_input(amount):
            error_msg += "*Amount field cannot be left blank\n"
            valid_record = False
        else:
            try:
                if validate_amount(amount):
                    amount = re.sub(r',','',self.amount_entry.get())
                    amount = int(float(amount) * 100.00)
                    data["amount"] = amount
                else:
                    raise ValueError
            except ValueError:
                error_msg += "*Amount format invalid\n"
                valid_record = False

        # ORDER NUMBER
        order = self.order_entry.get()
        if blank_input(order):
            error_msg += "*Order field cannot be left blank\n"
            valid_record = False
        else:
            try:
                if validate_all_numbers(order):
                    data["order_number"] = int(order)
                else:
                    raise ValueError
            except ValueError:
                error_msg += "*Order field must be numbers only\n"
                valid_record = False

        # ORDER TYPE
        try:
            # Error when if no selection(-1)
            if self.type_entry.current() < 0:
                raise ValueError
            type_id = str(self.type_data[self.\
                type_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            error_msg += "*An Order Type must be selected\n"
            valid_record = False
        else:
            data["_type_id"] = type_id

        # SUPERVISOR
        try:
            # Error when if no selection (-1)
            if self.supervisor_entry.current() < 0:
                raise ValueError
            supervisor_id = int(self.supervisor_data[self.\
                supervisor_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            error_msg += "*A Supervisor must be selected\n"
            valid_record = False
        else:
            data["supervisor_id"] = supervisor_id

        # EMPLOYEE
        try:
            # Error when if no selection (-1)
            if self.employee_entry.current() < 0:
                raise ValueError
            employee_id = int(self.employee_data[self. \
                               employee_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            error_msg += "*A Employee must be selected\n"
            valid_record = False
        else:
            data["employee_id"] = employee_id

        # ATTACHMENT
        attch = self.attachment_entry.get()
        if attch != 'None' and not blank_input(attch) and \
            os.path.exists(attch):
            data["attachment_name"] = attch
        else:
            self.attachment_entry.insert(0, "None")
            error_msg += "*An attachment must be imported"
            valid_record = False

        data['external_tracking'] = self.et_entry.get()
        data['note'] = self.note_text.get("1.0", END)

        if not valid_record:
            self.error_label = Label(self.win, text=error_msg,
                            justify="left", fg="red", font='Arial 8 bold')
            self.error_label.place(x=27, y=380)
            return False
        return True

    def select_attachment(self):
        attachment_path = askopenfilename(parent=self.win,
                                   title="SELECTING PDF ATTACHMENT FILE",
                                   defaultextension=".pdf",
                                   filetypes=(("PDF","*.pdf"),))
        if not blank_input(attachment_path):
            self.attachment_entry.config(state="normal")
            self.attachment_entry.delete(0, END)
            self.attachment_entry.insert(0, attachment_path)
            self.attachment_entry.xview_moveto(1.0)
            self.attachment_entry.config(state="readonly")

    def exit_window(self):
        self.win.destroy()