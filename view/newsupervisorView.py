import tkinter as tk
from input_validation import *

class NewSupervisorView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.win = None
        self.name_entry = None
        self.phone_entry = None
        self.email_entry = None

        self.error_label = None

    def show_ui(self):
        self.win = tk.Toplevel(self.root)
        self.win.geometry("400x250+650+380")
        self.win.resizable(False, False)
        self.win.attributes("-toolwindow", 1)
        self.win.grab_set()
        self.win.title("Add New Supervisor")

        tk.Label(self.win, text="Name:", font='Arial 12 bold').\
            place(x=20, y=20)

        tk.Label(self.win, text="Phone#:", font='Arial 12 bold').\
            place(x=20, y=70)

        tk.Label(self.win, text="Email:", font='Arial 12 bold').\
            place(x=20, y=120)

        self.name_entry = tk.Entry(self.win, bd=2, width=25,
                                      font='Arial 12 normal')
        self.phone_entry = tk.Entry(self.win, bd=2, width=12,
                                      font='Arial 12 normal')
        self.email_entry = tk.Entry(self.win, bd=2, width=27,
                                      font='Arial 12 normal')

        self.name_entry.place(x=100, y=20)
        self.phone_entry.place(x=100, y=70)
        self.email_entry.place(x=100, y=120)

        # Buttons
        btn_save = tk.Button(self.win, text="Save",
                             font=("Arial", 12), height=1, width=9)
        btn_save.configure(command= self.store_data)

        btn_cancel = tk.Button(self.win, text="Cancel",
                               font=("Arial", 12), height=1, width=9)
        btn_cancel.configure(command= self.exit_window)

        btn_save.place(x=111, y=200)
        btn_cancel.place(x=202, y=200)

    def store_data(self):
        if self.error_label is not None:
            self.error_label.destroy()
        data = dict()

        if self.validate_data(data):
            print(str(data))
            self.controller.save_data(data)
            self.exit_window()
            self.controller.refresh_supervisors()

    def validate_data(self, data):
        error_msg = str()
        valid_record = True

        # NAME
        if blank_input(self.name_entry.get()):
            error_msg += "*The Name field cannot be blank\n"
            valid_record = False
        elif validate_by_regex(self.name_entry.get(),r"^[a-zA-Z\s\.]*"):
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
            self.error_label = tk.Label(self.win, text=error_msg,
                                 justify="left", fg="red", font='Arial 8 bold')
            self.error_label.place(x=20, y=150)
            return False
        return True

    def exit_window(self):
        self.win.destroy()