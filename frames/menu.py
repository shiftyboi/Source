import tkinter as tk

class fr_menu(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.name = "menu"
        
        self.var_welcome = tk.StringVar() # Needed to dynamically update the username, so it is set correctly
        
        self.lb_welcome = tk.Label(self, text=f"Welcome {controller.user}", textvariable=self.var_welcome,font=("Arial", 15))
        self.lb_welcome.grid(row=0,column=0, sticky="ew")
        
        self.btn_index = tk.Button(self, text="Index", command=lambda: self.controller.show_frame("index"), font=("Arial", 15))
        self.btn_index.grid(row=0,column=1,pady=2, padx=5, sticky="e", ipadx=5)
        
        self.btn_user = tk.Button(self, text="Alerts",font=("Arial", 15))
        self.btn_user.grid(row=1, column=1, pady=2, padx=5, sticky="e", ipadx=5)
    
    
    
    def refresh(self):
        self.var_welcome.set(f"Welcome {self.controller.user}") # Update username displayed
        self.controller.geometry("400x200")
        
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
