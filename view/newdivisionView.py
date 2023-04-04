import tkinter as tk
from input_validation import *

class NewDivisionView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.win = None
        self.name_entry = None
        self.location_entry = None
        self.accounts_name_entry = None
        self.accounts_email_entry = None
        self.error_label = None

    def show_ui(self):
        self.win = tk.Toplevel(self.root)
        self.win.geometry("400x330+760+380")
        self.win.resizable(False, False)
        self.win.attributes("-toolwindow", 1)
        self.win.grab_set()
        self.win.title("New Division")

        tk.Label(self.win, text="Division", font='Arial 12 bold'). \
            place(x=20, y=20)
        tk.Label(self.win, text="Name:", font='Arial 12 normal'). \
            place(x=20, y=50)
        tk.Label(self.win, text="Location:", font='Arial 12 normal'). \
            place(x=20, y=80)
        tk.Label(self.win, text="Accounts Payable", font='Arial 12 bold'). \
            place(x=20, y=110)
        tk.Label(self.win, text="Name:", font='Arial 12 normal'). \
            place(x=20, y=140)
        tk.Label(self.win, text="Email:", font='Arial 12 normal'). \
            place(x=20, y=170)

        self.name_entry = tk.Entry(self.win, bd=2, width=25,
                                   font='Arial 12 normal')
        self.location_entry = tk.Entry(self.win, bd=2, width=25,
                           font='Arial 12 normal')
        self.accounts_name_entry = tk.Entry(self.win, bd=2, width=25,
                           font='Arial 12 normal')
        self.accounts_email_entry = tk.Entry(self.win, bd=2, width=25,
                           font='Arial 12 normal')

        self.name_entry.place(x=100, y=50)
        self.location_entry.place(x=100, y=80)
        self.accounts_name_entry.place(x=100, y=140)
        self.accounts_email_entry.place(x=100, y=170)

        btn_save = tk.Button(self.win, text="Save",
                             font=("Arial", 14), height=1, width=11)
        btn_save.configure(command=self.store_data)

        btn_cancel = tk.Button(self.win, text="Cancel",
                               font=("Arial", 14), height=1, width=11)
        btn_cancel.configure(command=self.exit_window)

        btn_save.place(x=23, y=280)
        btn_cancel.place(x=200, y=280)

    def store_data(self):
        if self.error_label is not None:
            self.error_label.destroy()
        data = dict()
        if self.validate_data(data):
            self.controller.callback_add_division(data)
            self.exit_window()

    def validate_data(self, data):
        error_msg = str()
        valid_record = True

        # Division Name
        name = self.name_entry.get()
        if blank_input(name):
            error_msg += "*The Division Name field cannot be blank\n"
            valid_record = False
        elif validate_by_regex(name, r"^[a-zA-Z0-9\s\-\\\/]*"):
            data["division._name"] = str(name)
        else:
            error_msg += "*The Division Name field cannot have special characters\n"
            valid_record = False

        # Location
        location = self.location_entry.get()
        if validate_address(location):
            data["division.location"] = str(location)
        else:
            error_msg += "*The Location field cannot have special characters\n"
            valid_record = False

        # Accounts Name
        acc_name = self.accounts_name_entry.get()
        if blank_input(acc_name):
            error_msg += "*The Accounts Name field cannot be blank\n"
            valid_record = False
        elif validate_by_regex(self.accounts_name_entry.get(), r"^[a-zA-Z\s\.]*"):
            data["division.accounts_payable_name"] = str(acc_name)
        else:
            error_msg += "*The Accounts Name field cannot have special characters\n"
            valid_record = False

        # Accounts Email
        acc_email = self.accounts_email_entry.get()
        if blank_input(acc_email):
            error_msg += "*The Accounts Email field cannot be blank\n"
            valid_record = False
        elif validate_email(acc_email):
            data["division.accounts_payable_email"] = str(acc_email)
        else:
            error_msg += "*The Accounts Email format is invalid"
            valid_record = False

        if not valid_record:
            self.error_label = tk.Label(self.win, text=error_msg,
                                        justify="left", fg="red",
                                        font='Arial 8 bold')
            self.error_label.place(x=20, y=200)
            return False
        return True

    def exit_window(self):
        self.win.destroy()