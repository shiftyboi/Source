import tkinter as tk


class fr_view(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self,parent)
        self.name = "view"
        
        self.item = None
        self.cur = None # Set later in refresh function
        self.data = None
        
        
        self.txt_id = tk.StringVar()
        self.txt_user = tk.StringVar()
        
        self.lb_id = tk.Label(self, text=f"ID: null",font=("Arial", 15), textvariable=self.txt_id)
        self.lb_id.grid(row=0,column=0,sticky="nw", columnspan=2)
        
        self.lb_user = tk.Label(self, text=f"USER: null", font=("Arial", 15), textvariable=self.txt_user)
        self.lb_user.grid(row=1,column=0,sticky="nw",columnspan=2)
        
        self.btn_lend = tk.Button(self, text="Lend Item", font=("Arial", 15), command=lambda: self.lend)
        self.btn_lend.grid(row=1, column=1, sticky="nw")
        
    def lend(self):
        userid = self.cur.execute(f'''
                         
                         SELECT id FROM Users WHERE username={self.controller.user}
                         
                         ''')
        
        self.cur.execute(f'''
                         
                         UPDATE Assets
                         SET Assets.user={userid.fetchone()[0]}
                         WHERE Assets.id={self.item}
                         
                         ''')
                    
    
    
    
    
    def refresh(self):
        self.item = self.controller.item
        self.cur = self.controller.cur # Borrowing variables from app class for ease of use

        self.data = self.cur.execute(f'''
                                     
                                     SELECT Assets.id, Users.username, Assets.name, Rooms.name
                                     FROM Assets
                                     JOIN Users on Assets.user=Users.id
                                     JOIN Rooms on Assets.location=Rooms.id
                                     WHERE Assets.id={self.item}
                                     
                                     ''') # Grab data needed from the database
        
        self.data = self.data.fetchone()
        
        self.txt_id.set(f"ID: {self.data[0]}")
        self.txt_user.set(f"USER: {self.data[1]}")
        
        self.controller.geometry("600x600")
        
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)