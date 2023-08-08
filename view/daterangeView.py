from tkinter import *
import datetime
from tkinter.constants import *
from tkcalendar import DateEntry
from helpers.input_validation import *

class DateRangeView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.win = None

        # Objects
        self.start_date = None
        self.end_date = None

        # Data
        self.data = dict()
        self.option_var = StringVar(value=0)
        self.start_date_var = StringVar()
        self.end_date_var = StringVar()

        #Buttons
        self.btn_save = None
        self.btn_cancel = None

    def show_ui(self):
        self.win = Toplevel(self.root)
        self.win.geometry("400x300+550+280")
        self.win.resizable(False, False)
        self.win.attributes("-toolwindow", 1)
        self.win.grab_set()
        self.win.title("Date Range Options")

        # Labels
        Label(self.win, text="Please choose one:", font='Arial 12 bold').place(x=27, y=10)

        # Entry Setup
        todays_date = datetime.date.today()
        tomorrows_date = todays_date + datetime.timedelta(days=1)
        self.start_date = DateEntry(self.win, selectmode='night',
                                    date_pattern='mm/dd/yyyy',
                                    textvariable=self.start_date_var,
                                    date= todays_date,
                                    state="normal")

        self.end_date = DateEntry(self.win, selectmode='night',
                                    date_pattern='mm/dd/yyyy',
                                    textvariable=self.end_date_var,
                                    date=tomorrows_date,
                                    state="normal")

        self.start_date.config(state="disabled")
        self.end_date.config(state="disabled")
        self.start_date.place(x=150, y=160)
        self.end_date.place(x=250, y=160)

        # Options
        Radiobutton(self.win, text="Up to Date (Jan 1st to Present Day)",
                    variable=self.option_var, value="uptodate", command=self.on_custom_date_range).place(x=27, y=40)
        Radiobutton(self.win, text="Current Natural Year (Jan 1st to Dec 31st)",
                    variable=self.option_var,value="naturalyear", command=self.on_custom_date_range).place(x=27, y=80)
        Radiobutton(self.win, text="Current Fiscal Year (Previous Oct 1st to Upcoming Sept 30th)",
                    variable=self.option_var, value="fiscalyear", command=self.on_custom_date_range).place(x=27, y=120)
        Radiobutton(self.win, text="Custom:", variable=self.option_var,
                        value="custom", command=self.on_custom_date_range).place(x=27, y=160)

        self.btn_save = Button(self.win, text="Save", font=("Arial", 12),
                          height=1, width=9,command= self.store_data)

        self.btn_cancel = Button(self.win, text="Cancel", font=("Arial", 12),
                            height=1, width=9, command= self.exit_window)

        self.btn_save.place(x=70, y=250)
        self.btn_cancel.place(x=180, y=250)

    def on_custom_date_range(self):
        self.data['option'] = self.option_var.get()
        if self.option_var.get() == "custom":
            self.start_date.config(state="normal")
            self.end_date.config(state="normal")
        else:
            self.start_date.config(state="readonly")
            self.end_date.config(state="readonly")

    def store_data(self):
        if self.option_var.get() == "custom":
            if self.validate_data():
                self.controller.store_setting(self.data)
                self.exit_window()
        elif self.option_var.get() == '0':
            # Ignore input
            pass
        else:
            self.controller.store_setting(self.data)
            self.exit_window()

    def validate_data(self):
        valid_record = True
        error_msg = str()
        if not 'option' in self.data:
            raise Exception

        if self.data['option'] == 'custom':
            start_date = self.start_date.get()
            end_date = self.end_date.get()

            if blank_input(start_date) or blank_input(end_date):
                error_msg += "*Date field cannot be blank\n"
                valid_record = False
            elif validate_date(start_date) and validate_date(end_date):
                start_date = datetime.datetime.strptime(
                    start_date, '%m/%d/%Y').strftime('%Y-%m-%d')
                end_date = datetime.datetime.strptime(
                    end_date, '%m/%d/%Y').strftime('%Y-%m-%d')
                if start_date < end_date:
                    self.data["start_date"] = start_date
                    self.data["end_date"] = end_date
                else:
                    error_msg += "*The start date cannot be equal or older than the end date\n"
                    valid_record = False
            else:
                error_msg += "*The Date entered is invalid\n"
                valid_record = False

            if not valid_record:
                self.error_label = Label(self.win, text=error_msg,
                                         justify="left", fg="red", font='Arial 8 bold')
                self.error_label.place(x=27, y=190)
                return False
            else:
                return True
        return True

    def exit_window(self):
        self.win.destroy()