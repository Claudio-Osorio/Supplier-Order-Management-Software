from tkinter import *
from tkinter import ttk
from input_validation import validate_email,validate_phone,\
    validate_by_regex, blank_input

class NewEmployeeView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.win = None

        self.frame_all_projects = None
        self.frame_employee_projects = None
        self.name_entry = None
        self.phone_entry = None
        self.email_entry = None

        self.all_projects_scrollbar = None
        self.employee_projects_scrollbar = None

        self.employee_projects_listbox = None
        self.projects_listbox = None

        self.employee_projects_tracking = list()
        self.all_projects_data = None

        self.employee_projects_items = None
        self.all_projects_items = None
        self.error_label = None

    def show_ui(self):
        self.win = Toplevel(self.root)
        self.win.geometry("800x500+450+280")
        self.win.resizable(False, False)
        self.win.attributes("-toolwindow", 1)
        self.win.grab_set()
        self.win.title("Add New Employee")

        self.frame_all_projects = Frame(self.win, width=330, height=300)
        self.frame_employee_projects = Frame(self.win, width=330, height=300)

        self.frame_all_projects.place(x=20, y=135)
        self.frame_employee_projects.place(x=450, y=135)

        self.frame_all_projects.pack_propagate(False)
        self.frame_employee_projects.pack_propagate(False)

        label_font = 'Arial 12 bold'
        Label(self.win, text="Name:", font=label_font).\
            place(x=20, y=20)
        Label(self.win, text="Phone#:", font=label_font).\
            place(x=400, y=20)
        Label(self.win, text="Email:", font=label_font).\
            place(x=20, y=70)
        Label(self.win, text="Assigned Projects", font=label_font).\
            place(x=555, y=110)
        Label(self.win, text="All Projects", font=label_font).\
            place(x=130, y=110)

        entry_font = 'Arial 12 normal'
        self.name_entry = Entry(self.win, bd=2, width=27,
                                      font=entry_font)
        self.phone_entry = Entry(self.win, bd=2, width=12,
                                      font=entry_font)
        self.email_entry = Entry(self.win, bd=2, width=27,
                                      font=entry_font)

        self.name_entry.place(x=85, y=20)
        self.email_entry.place(x=85, y=70)
        self.phone_entry.place(x=480, y=20)

        self.all_projects_data = self.controller.get_companies_and_projects()
        self.all_projects_items = Variable(value=tuple(row[1] for row in self.all_projects_data))

        self.all_projects_listbox = Listbox(self.frame_all_projects,
                                    selectmode=EXTENDED,
                                    font=entry_font,
                                    listvariable=self.all_projects_items)

        self.employee_projects_listbox = Listbox(self.frame_employee_projects,
                                    selectmode=SINGLE,
                                    font=entry_font,
                                    listvariable=self.employee_projects_items)

        self.all_projects_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.employee_projects_listbox.pack(side=LEFT, fill=BOTH, expand=True)

        self.all_projects_scrollbar = Scrollbar(self.frame_all_projects,
                        orient=VERTICAL, command=self.all_projects_listbox.yview)
        self.all_projects_listbox.config(yscrollcommand=self.all_projects_scrollbar.set)
        self.all_projects_scrollbar.pack(side=RIGHT, fill=Y)

        self.employee_projects_scrollbar = Scrollbar(self.frame_employee_projects,
                        orient=VERTICAL, command=self.employee_projects_listbox.yview)
        self.employee_projects_scrollbar.pack(side=RIGHT, fill=Y)
        self.employee_projects_listbox.config(yscrollcommand=\
                                             self.employee_projects_scrollbar.set)

        # Buttons
        button_font = ("Arial", 12)
        btn_add = Button(self.win, text="Assign",
                             font=button_font, height=1, width=6)
        btn_remove = Button(self.win, text="Unassign",
                             font=button_font, height=1, width=8)
        btn_save = Button(self.win, text="Save",
                             font=button_font, height=1, width=9)
        btn_cancel = Button(self.win, text="Cancel",
                               font=button_font, height=1, width=9)

        btn_add.configure(command= self.add_project)
        btn_remove.configure(command= self.remove_project)
        btn_save.configure(command= self.store_data)
        btn_cancel.configure(command= self.exit_window)

        btn_add.place(x=367, y=240)
        btn_remove.place(x=357, y=280)
        btn_save.place(x=300, y=455)
        btn_cancel.place(x=400, y=455)

    def add_project(self):
        selection = self.all_projects_listbox.curselection()
        if selection:
            for index in selection:
                project_db_id = self.all_projects_data[index][0]
                if project_db_id not in self.employee_projects_tracking:
                    project = self.all_projects_listbox.get(index)
                    self.employee_projects_listbox.insert(END, project)
                    self.employee_projects_tracking.append(project_db_id)

    def remove_project(self):
        selection = self.employee_projects_listbox.curselection()
        if selection:
            self.employee_projects_listbox.delete(selection[0])
            del self.employee_projects_tracking[selection[0]]

    def store_data(self):
        if self.error_label is not None:
            self.error_label.destroy()
        data = dict()
        if self.validate_data(data):
            self.controller.save_data(data)
            self.exit_window()
            self.controller.refresh_employees()

    def validate_data(self, data):
        error_msg = str()
        valid_record = True

        # NAME
        if blank_input(self.name_entry.get()):
            error_msg += "*The Name field cannot be blank\n"
            valid_record = False
        elif validate_by_regex(self.name_entry.get(), r"^[a-zA-Z\s\.]*"):
            data["name"] = str(self.name_entry.get())
        else:
            error_msg += "*The Name field cannot have special characters\n"
            valid_record = False
        # PHONE NUMBER
        if not blank_input(self.phone_entry.get()) and \
                not validate_phone(self.phone_entry.get()):
            error_msg += "*The Phone number is not properly formatted\n"
            valid_record = False
        else:
            data["phone"] = str(self.phone_entry.get())
        # EMAIL
        if blank_input(self.email_entry.get()):
            error_msg += "*The Email field cannot be blank"
            valid_record = False
        elif not validate_email(self.email_entry.get()):
            error_msg += "*The Email field cannot contain special characters"
            valid_record = False
        else:
            data["email"] = str(self.email_entry.get())

        if not valid_record:
            self.error_label = Label(self.win, text=error_msg,
                                     justify="left", fg="red", font='Arial 8 bold')
            self.error_label.place(x=27, y=450)
            return False
        if len(self.employee_projects_tracking) == 0:
            data["projects"] = None
        else:
            data["projects"] = self.employee_projects_tracking
        print(data)
        return True

    def exit_window(self):
        self.win.destroy()