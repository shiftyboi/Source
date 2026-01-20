import tkinter as tk
from tkinter import ttk

class fr_user(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.name = "user"

    def refresh(self):
        self.controller.geometry("600x500")