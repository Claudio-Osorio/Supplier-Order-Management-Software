from tkinter import *
from tkinter.ttk import Combobox
from input_validation import validate_address
from input_validation import validate_by_regex
from input_validation import blank_input

class NewProjectView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.win = None

        self.name_entry = None
        self.address_entry = None
        self.company_entry = None
        self.division_entry = None
        self.cbox_employee_entry = None  #Combobox

        self.company_var = StringVar()
        self.division_var = StringVar()
        self.company_data = None
        self.division_data = None
        self.employee_data = None         #Combobox options
        self.employee_var = StringVar()   #Combobox selected

        self.error_label = None


    def show_ui(self):
        self.win = Toplevel(self.root)
        self.win.geometry("450x340+560+380")
        self.win.resizable(False, False)
        self.win.attributes("-toolwindow", 1)
        self.win.grab_set()
        self.win.title("Add New Project")

        Label(self.win, text="Name:", font='Arial 12 bold'). \
            place(x=20, y=20)

        Label(self.win, text="Address:", font='Arial 12 bold'). \
            place(x=20, y=60)

        Label(self.win, text="Company:", font='Arial 12 bold'). \
            place(x=20, y=100)

        Label(self.win, text="Division:", font='Arial 12 bold'). \
            place(x=20, y=140)

        Label(self.win, text="Default Employee:",
              font='Arial 12 bold',
              anchor='w').\
            place(x=20, y=180)

        self.name_entry = Entry(self.win, bd=2, width=33,
                                   font='Arial 12 normal')

        self.address_entry = Entry(self.win, bd=2, width=33,
                                   font='Arial 12 normal')

        self.company_entry = Combobox(self.win,
                      width=27, height=40, textvariable=self.company_var,
                      state="readonly")

        self.division_entry = Combobox(self.win,
                      width=27, height=40, textvariable=self.division_var,
                      state="readonly")

        self.cbox_employee_entry = Combobox(self.win, width=20, height=40,
                                            textvariable=self.employee_var,
                                            state="readonly")

        self.name_entry.place(x=110, y=20)
        self.address_entry.place(x=110, y=60)
        self.company_entry.place(x=110, y=103)
        self.division_entry.place(x=110, y=143)
        self.cbox_employee_entry.place(x=170, y=183)

        self.company_data = self.controller.get_companies()
        self.company_entry['values'] = [value[1] for value in self.company_data]
        self.division_entry['values'] = [('Select a company first')]
        self.division_entry.config(state="disabled")
        self.division_entry.current(0)
        self.employee_data = self.controller.get_employees()
        self.cbox_employee_entry['values'] = [value[1] for value in self.employee_data]

        self.company_var.trace('w', self.on_company_selected)
        self.division_var.trace('w', self.on_division_selected)

        btn_save = Button(self.win, text="Save",
                             font=("Arial", 12), height=1, width=9,
                             command= self.store_data)

        btn_cancel = Button(self.win, text="Cancel",
                              font=("Arial", 12), height=1, width=9,
                              command= self.exit_window)

        btn_save.place(x=136, y=300)
        btn_cancel.place(x=227, y=300)

    def on_company_selected(self, *arg):
        # Get Divisions
        selected_company_id = self.company_data[self.company_entry.current()][0]
        self.division_data = self.controller. \
            get_divisions(selected_company_id)
        self.division_entry['values'] = [value[1] for value in self.division_data]
        # If there is no division set division entry as "None"
        if len(self.division_entry['values']) == 0:
            self.division_entry['values'] = [('None')]
            self.division_entry.current(0)
            self.division_entry.config(state="disabled")
        else:
            self.division_entry.config(state="readonly")
        # Trigger update on dropdown
        self.division_entry.current(0)
        self.on_division_selected()

    def on_division_selected(self, *args):
        pass

    def store_data(self):
        if self.error_label is not None:
            self.error_label.destroy()
        data = dict()
        if self.validate_data(data):
            print(data)
            self.controller.save_data(data)
            self.exit_window()
            self.controller.refresh_projects()

    def validate_data(self, data):
        valid_record = True
        error_msg = str()

        # NAME
        project_name = self.name_entry.get()
        if blank_input(project_name):
            error_msg += "*The Name field cannot be blank\n"
        elif validate_by_regex(project_name, r"^[a-zA-Z0-9\s\\\.]*"):
            data["project._name"] = project_name
        else:
            error_msg += "*The Name entered is invalid\n"
            valid_record = False

        # ADDRESS
        project_address = self.address_entry.get()
        if validate_address(project_address):
            data["project.address"] = project_address
        else:
            error_msg += "*The Address entered is invalid\n"
            valid_record = False

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
        else:
            data["project.company_id"] = company_id

        # DIVISION
        try:
            # Error when if no selection (-1)
            if len(self.division_entry['values']) < 0 or \
                self.division_entry['values'][0] == "None":
                raise ValueError
            division_id = int(self.division_data[self.\
                division_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            error_msg += "*A Division must be selected\n"
            valid_record = False
        else:
            data["project.division_id"] = division_id
        # EMPLOYEE
        try:
            # Error when if no selection(-1)
            if self.cbox_employee_entry.current() < 0:
                raise ValueError
            employee_id = int(self.employee_data[self. \
                               cbox_employee_entry.current()][0])
        except (TypeError, ValueError, KeyError, IndexError):
            error_msg += "*A Employee must be selected"
            valid_record = False
        else:
            data["employee.id"] = employee_id

        if not valid_record:
            self.error_label = Label(self.win, text=error_msg,
                                        justify="left", fg="red", font='Arial 8 bold')
            self.error_label.place(x=23, y=207)
            return False
        return True

    def exit_window(self):
        self.win.destroy()