import tkinter as tk
from tkinter.constants import *
from tkinter import ttk
from helpers.input_validation import blank_input, validate_by_regex

class NewCompanyView:
    def __init__(self, root, controller):
        self.root = root
        self.win = None
        self.controller = controller
        self.frame_divisions = None
        self.error_label = None

        # Entry
        self.name_entry = None

        # Tree
        self.division_tree = None
        self.division_tree = None
        self.division_tree_scroll_x = None
        self.division_tree_scroll_y = None
        self.division_tree_style = None

    def show_ui(self):
        self.win = tk.Toplevel(self.root)
        self.win.geometry("800x400+560+380")
        self.win.resizable(False, False)
        self.win.attributes("-toolwindow", 1)
        self.win.grab_set()
        self.win.title("Add New Company")

        # FRAME
        self.frame_divisions = tk.Frame(self.win,
                                   width=760, height=220, bg="red")
        self.frame_divisions.place(x=20, y=90)
        # Prevents children widget to modify the frame size
        self.frame_divisions.pack_propagate(False)

        tk.Label(self.win, text="New Company:", font='Arial 12 bold'). \
            place(x=20, y=20)

        tk.Label(self.win, text="Divisions", font='Arial 12 bold'). \
            place(x=20, y=60)


        self.name_entry = tk.Entry(self.win, bd=2, width=25,
                                   font='Arial 12 normal')

        self.name_entry.place(x=145, y=20)

        # TREE
        # Scrollbars
        self.division_tree_scroll_x = tk.Scrollbar(self.frame_divisions,
                                        orient=HORIZONTAL)
        self.division_tree_scroll_x.pack(side=BOTTOM,
                                      fill=X)
        self.division_tree_scroll_y = tk.Scrollbar(self.frame_divisions,
                                        orient=VERTICAL)
        self.division_tree_scroll_y.pack(side=RIGHT, fill=Y)

        # Instance
        self.division_tree = ttk.Treeview(self.frame_divisions,
                                selectmode="browse",
                                xscrollcommand=self.division_tree_scroll_x.set,
                                yscrollcommand=self.division_tree_scroll_y.set)
        self.division_tree['columns'] = ("Id","Name", "Location",
                                         "Accounts Agent", "Email")
        self.division_tree.column("#0", width=0,
                                    stretch=NO)
        self.division_tree_scroll_x.config(command=self.division_tree.xview)
        self.division_tree_scroll_y.config(command=self.division_tree.yview)

        # Tree Column
        self.division_tree.column("Id", anchor=W,
                                    width=3)
        self.division_tree.column("Name", anchor=W,
                                    width=120)
        self.division_tree.column("Location", anchor=W,
                                    width=150)
        self.division_tree.column("Accounts Agent", anchor=W,
                                    width=80)
        self.division_tree.column("Email", anchor=W,
                                    width=150)
        self.division_tree['displaycolumns'] = ("Id", "Name", "Location",
                                         "Accounts Agent", "Email")

        # Tree Headings
        self.division_tree.heading("Id", text="Id",
                                             anchor=W)
        self.division_tree.heading("Name", text="Name",
                                             anchor=W)
        self.division_tree.heading("Location", text="Location",
                                             anchor=W)
        self.division_tree.heading("Accounts Agent",
                                    text="Accounts Agent",
                                    anchor=W)
        self.division_tree.heading("Email",
                                    text="Email",
                                    anchor=W)


        # Tree Style
        self.division_tree_style = ttk.Style()

        # Theme
        self.division_tree_style.theme_use("clam")

        # Configure treeview colors
        self.division_tree_style.configure("Treeview",
                                     background="#c7c7c7",
                                     foreground="white",
                                     fieldbackground="white",
                                     rowheight=25)
        self.division_tree_style.map('Treeview',
                                     background=[('selected', '#518aed')])
        # Tags
        self.division_tree.tag_configure("textonly",foreground="black")

        self.division_tree.pack(fill='both', expand=True)

        # Buttons
        btn_add_division = tk.Button(self.win, text="New",
                             font=("Arial", 8), height=1, width=11)
        btn_add_division.configure(command=self.insert_division)
        btn_remove_division = tk.Button(self.win, text="Delete",
                                     font=("Arial", 8), height=1, width=11)
        btn_remove_division.configure(command=self.remove_selected_division)

        btn_save = tk.Button(self.win, text="Save",
                             font=("Arial", 12), height=1, width=9)
        btn_save.configure(command=self.store_data)

        btn_cancel = tk.Button(self.win, text="Cancel",
                               font=("Arial", 12), height=1, width=9)
        btn_cancel.configure(command=self.exit_window)

        btn_add_division.place(x=600, y=312)
        btn_remove_division.place(x=675, y=312)
        btn_save.place(x=311, y=350)
        btn_cancel.place(x=402, y=350)

    def store_data(self):
        if self.error_label is not None:
            self.error_label.destroy()
        company_name = dict()

        if self.validate_data(company_name):
            self.controller.store_data(company_name)
            self.exit_window()
            self.controller.refresh_companies()

    def validate_data(self, company_name):
        error_msg = str()
        valid_record = True

        # NAME
        if blank_input(self.name_entry.get()):
            error_msg += "*The Name field cannot be blank\n"
            valid_record = False
        elif validate_by_regex(self.name_entry.get(), r"^[a-zA-Z0-9\s]*"):
            company_name["_name"] = str(self.name_entry.get())
        else:
            error_msg += "*The Name field cannot have special characters\n"
            valid_record = False

        if self.controller.empty_division():
            error_msg += "*Company must have at least one division"
            valid_record = False

        if not valid_record:
            self.error_label = tk.Label(self.win, text=error_msg,
                                        justify="left", fg="red",
                                        font='Arial 8 bold')
            self.error_label.place(x=20, y=315)
            return False
        return True

    def insert_division(self):
        self.controller.get_new_division()

    def refresh_division_tree(self, divisions):
        self.remove_all_divisions()
        for index, division in enumerate(divisions):
            tup = (index + 1,
                   division["division._name"],
                   division["division.location"],
                   division["division.accounts_payable_name"],
                   division["division.accounts_payable_email"])
            self.division_tree.insert(parent='', index='end', iid=index, text="",
                                 values=tup)

    def remove_selected_division(self):
        if self.empty_tree():
            return
        focused_item = self.division_tree.focus()
        division_id = self.division_tree.item(focused_item)["values"][0]
        self.controller.remove_division(division_id - 1)

    def remove_all_divisions(self):
        for item in  self.division_tree.get_children():
            self.division_tree.delete(item)

    def exit_window(self):
        self.win.destroy()


    def empty_tree(self):
        items = self.division_tree.get_children()
        if len(items) == 0:
            return True
        else:
            return False
