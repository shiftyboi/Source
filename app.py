import tkinter as tk
from frames.login import fr_login
from frames.menu import fr_menu
from frames.index import fr_index
from frames.view import fr_view


class App(tk.Tk):
    def __init__(
        self,
        screenName=None,
        baseName=None,
        className="Tk",
        useTk=True,
        sync=False,
        use=None,
    ):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.cur = None
        self.user = None  # These will be set later by the login process, so other frames can use them
        self.item = None

        self.frames = {}

        self.classes = [fr_login, fr_menu, fr_index, fr_view]  # List of frame classes

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        for F in self.classes:
            frame = F(self.container, self)
            self.frames[frame.name] = frame
        self.show_frame("login")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.refresh()  # Makes sure any data the frame needs is updated; also updates frame's aspect ratio, etc
        frame.tkraise()
        frame.grid(row=0, column=0, sticky="nsew")


main = App()

main.mainloop()
