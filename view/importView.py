from tkinter.messagebox import *
from helpers.input_validation import blank_input
from tkinter.filedialog import askopenfilename
from model.importModel import ImportModel
from tkinter.ttk import Progressbar, Button
from tkinter import *
from tkinter import ttk

import os

class ImportView:
    def __init__(self, root, controller, app_controller):
        self.root = root
        self.controller = controller
        self.app_controller = app_controller
        self.win = None
        self.progress = None
        self.progress_bar_style = None
        self.btn_cancel = None

    def show_ui(self):
        message ="SOMS is only able to import Excel (.xlsx) files that" \
                 " have been formatted as expected. It is required that " \
                 " all orders have attachments and that they are located" \
                 " in the same folder where the Excel file is located." \
                 " The attachments must be named exactly by the order number listed." \
                 " For example, \"4233.pdf\".\n If you wish to proceed" \
                 " importing an Excel file please click YES and select" \
                 " the file.\n\nWARNING: If the order, project, or other data" \
                 " expected cannot be matched or read then the order will not be" \
                 " added to the database to prevent possible issues." \
                 " Please read the log to obtain a comprehensive list of the orders" \
                 " that failed to be imported."

        if askyesno("Import Orders From Excel File (.xlsx)", message):
            excel_file_path = askopenfilename(parent=self.root,
                                              title="IMPORTING ORDERS FROM EXCEL FILE (.XLSX)",
                                              defaultextension=".xlsx",
                                              filetypes=(("Excel Spreadsheet", "*.xlsx"),))
            if not blank_input(excel_file_path) and \
                    os.path.exists(excel_file_path):
                self.controller.import_excel_file( excel_file_path)

    def import_summary(self, summary):
        if summary:
            message = f"Sucessfully Imported: {summary[0]}" \
                      f"\nFailed to import: {summary[1]} \n\n" \
                      f"NOTE: To view and resolve failed imports please refer " \
                      f"to the latest log file"
            showinfo(title='IMPORT FINISHED', message=message)

    def import_failed(self):
        message = f"The Excel spreadsheet file could not be opened or parsed." \
                  f" Please make sure that the file is correctly formatted and all the" \
                  f" expected columns are present before you try again."
        showerror(title='IMPORT FAILED', message=message)