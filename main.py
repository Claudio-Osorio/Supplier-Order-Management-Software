import tkinter as tk
from app import *
from helpers.debugging import *

init_logging()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()