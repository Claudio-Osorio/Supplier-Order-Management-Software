import tkinter as tk
from app import *
import logging

DEBUG = True

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()