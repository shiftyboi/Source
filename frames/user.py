import tkinter as tk
from tkinter import ttk

class fr_user(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.name = "user"

        self.cur = None
        self.alerts = None # List of alerts to be iterated through
        
        self.txt_alert = tk.StringVar()
        
        self.lb_alert = tk.Label(self,font=("Arial", 15),textvariable=self.txt_alert) # Label that will display the alert.
        self.lb_alert.grid(row=0,column=0,sticky="nsew")

        self.btn_next = tk.Button(self, font=("Arial", 15), command=lambda: self.next(), text="Next")
        self.btn_next.grid(row=1,column=0)
    
    
    
    
    
    def refresh(self):
        self.controller.geometry("600x500")
        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)

        self.cur = self.controller.cur # Grab cursor for ease of use

        self.alerts = self.cur.execute(f'''

                        SELECT * FROM Alerts 
                        WHERE recipient = (SELECT id FROM Users WHERE username="{self.controller.user}")


''')


