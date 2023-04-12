from tkinter import Toplevel, Label, Button
class AboutView:

    def show_ui(self):
        self.win = Toplevel(self.root)
        self.win.geometry("500x150")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - 250
        y = (screen_height / 2) - 75
        self.win.geometry("+%d+%d" % (x, y))
        self.win.resizable(False, False)
        self.win.attributes("-toolwindow", 1)
        self.win.grab_set()
        self.win.title("About")

        Label(self.win, text="Supplier Order Manangement Software", font='Arial 17 bold'). \
            place(x=30, y=10)
        Label(self.win, text="Created by:", font='Arial 15 bold'). \
            place(x=110, y=45)
        Label(self.win, text="Claudio B. Osorio", font='Arial 15 normal'). \
            place(x=230, y=45)
        Label(self.win, text="email: osorioclaudiobenjamin@gmail.com",
              font='Arial 10 normal').place(x=130, y=70)
        Button(self.win, text="OK", font=("Arial", 12),
               height=1, width=6, command=lambda:self.win.destroy()).place(x=220, y=105)
