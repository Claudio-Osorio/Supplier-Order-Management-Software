import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
from configurations import *
from configurations import store_main_window_geometry as store_mw_geometry
from configurations import read_main_window_geometry as read_mw_geometry

class AppView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        # Main Window Setup
        self.root.resizable(True, True)
        geometry = read_mw_geometry()
        self.root.geometry(f'{geometry}')
        self.root.minsize(1645,600)
        self.root.title('Supplier Order Management Software' + read_version())
        self.root.config(bg='#000000')

        # DATA Menu
        self.menubar = tk.Menu(self.root)
        self.data_menu = tk.Menu(self.menubar, tearoff=0)
        self.data_menu.add_command(label="Import Excel File",
                              command=self.controller.import_excel_file)
        self.data_menu.add_command(label="Export to Excel File",
                              command=self.controller.export_to_excel_file)
        self.data_menu.add_separator()
        self.data_menu.add_command(label="Reload Missing Attachments",
                              command=self.controller.reload_all_attachments)
        self.data_menu.add_command(label="Reload All Attachments",
                              command=self.controller.reload_all_attachments)
        self.data_menu.add_command(label="Load Attachment Folder",
                              command=self.controller.load_attachment_folder)
        self.data_menu.add_separator()
        self.data_menu.add_command(label="Exit",
                              command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.data_menu)

        # EDIT Menu
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="New Order",
                             command=self.controller.new_order)
        self.editmenu.add_command(label="Update Order",
                             command=self.controller.update_order)
        self.editmenu.add_command(label="Delete Order",
                             command=self.controller.delete_order)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="New Supervisor",
                             command=self.controller.new_supervisor)
        self.editmenu.add_command(label="Update Supervisor",
                             command=self.controller.update_supervisor)
        self.editmenu.add_command(label="Delete Supervisor",
                             command=self.controller.delete_supervisor)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="New Employee",
                                  command=self.controller.new_employee)
        self.editmenu.add_command(label="Update Employee",
                                  command=self.controller.update_employee)
        self.editmenu.add_command(label="Delete Employee",
                                  command=self.controller.delete_employee)
        self.editmenu.add_command(label="Edit Employee Projects",
                                  command=self.controller.edit_employee_projects)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="New Company",
                             command=self.controller.new_company)
        self.editmenu.add_command(label="Update Company",
                             command=self.controller.update_company)
        self.editmenu.add_command(label="Delete Company",
                             command=self.controller.delete_company)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="New Project",
                             command=self.controller.new_project)
        self.editmenu.add_command(label="Update Project",
                             command=self.controller.update_project)
        self.editmenu.add_command(label="Delete Project",
                                  command=self.controller.delete_project)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        # CONFIG Menu
        self.configmenu = tk.Menu(self.menubar, tearoff=0)
        self.configmenu.add_command(label="Store Current Layout as Default",
                               command=self.store_current_layout)
        self.configmenu.add_command(label="Edit Email Draft",
                                    command=self.controller.edit_email_draft)
        self.menubar.add_cascade(label="Config", menu=self.configmenu)

        # HELP Menu
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index")
        self.helpmenu.add_command(label="About...")
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.root.config(menu=self.menubar)


    def store_current_layout(self):
        geometry = self.root.winfo_geometry()
        self.controller.store_current_geometry(geometry)