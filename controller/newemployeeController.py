from tkinter import *
import tkinter as tk
from tkinter import ttk

def __init__(self, root, controller):
    self.root = root
    self.controller = controller

    self.frame_communities = None
    self.name_entry = None
    self.phone_entry = None
    self.email_entry = None
    self.project_tree_scroll_x = None
    self.project_tree_scroll_y = None

def show_ui(self):
    self.win = tk.Toplevel(self.root)
    self.win.geometry("800x550+550+280")
    self.win.resizable(False, False)
    self.win.attributes("-toolwindow", 1)
    self.win.grab_set()
    self.win.title("Add New Employee")

    # Tree Frame
    self.frame_communities = tk.Frame(self.win,
                      width=330, height=230, bg="red")
    self.frame_communities.place(x=400, y=60)
    self.frame_communities.pack_propagate(False)

    # Tree Scrollbars
    self.project_tree_scroll_y = Scrollbar(self.win)
    self.project_tree_scroll_y.pack(side=RIGHT, fill=Y)
    self.project_tree_scroll_x = Scrollbar(self.win, orient=HORIZONTAL)
    self.project_tree_scroll_x.pack(side=BOTTOM, fill=X)
    self.project_tree = ttk.Treeview(self.frame_communities,
                                     yscrollcommand=self.project_tree_scroll_y.set,
                                     xscrollcommand=self.project_tree_scroll_x.set)

    # All the possible columns
    self.project_tree['columns'] = ("Project")

    # Defining Columns
    self.project_tree.column("#0", width=0, stretch=NO) # Ghost Column...
    self.project_tree.column("Project", anchor=W, width=120)

    # Defining Headings
    self.project_tree.heading("#0", text="",
                              anchor=CENTER)
    self.project_tree.heading("Select", text="Select",
                              anchor=CENTER)
    self.project_tree.heading("Project", text="Project",
                              anchor=CENTER)

    # Style
    project_tree_style = ttk.Style()
    project_tree_style.theme_use("clam")
    project_tree_style.configure("Treeview",
                                   background="#c7c7c7",  # Bg when there are orders
                                   foreground="white",  #
                                   fieldbackground="white",
                                   rowheight=25)

    # Columns to show
    self.project_tree['displaycolumns'] = ("Select", "Project")
    self.project_tree.pack(fill='both', expand=True)