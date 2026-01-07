import tkinter as tk
from tkinter import ttk

class fr_index(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.name = "index"
        
        self.btn_back = tk.Button(self, text="← Back", command=lambda: self.controller.show_frame("menu"), font=("Arial", 15))
        self.btn_back.grid(row=0,column=0,pady=2, sticky="nw")
        
        self.lb_hint = tk.Label(self, text="Double-click an item to view it in detail", font=("Arial", 15))
        self.lb_hint.grid(row=0,column=1,sticky="nsew")

        self.btn_new = tk.Button(self, text="New item", font=("Arial", 15), command=lambda: self.new())
        self.btn_new.grid(row=0,column=1, sticky="nw")
        
        self.tree_assets = ttk.Treeview(self, columns=('name','user','room'))
        
        self.tree_assets.heading('#0', text="ID")
        self.tree_assets.heading('name', text="Name")
        self.tree_assets.heading('user', text="User")
        self.tree_assets.heading('room', text="Location")
        
        self.tree_assets.grid(row=1,column=0, sticky="nsew", columnspan=2)
        
        self.style = ttk.Style()
        self.style.configure("Treeview", font=(None,12))
        self.style.configure("Treeview.Heading", font=(None,15))
        
        

    
    def refresh(self):
        self.controller.geometry("800x800")
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=7)
        
        self.cur = self.controller.cur
        
        self.data = self.cur.execute('''
                           
                           SELECT Assets.id, Assets.name, Users.username, Rooms.name
                           FROM Assets
                           JOIN Users on Assets.user=Users.id
                           JOIN Rooms on Assets.location=Rooms.id
                           
                           ''') # Grab needed data from db
        
        
        self.data = self.data.fetchall()
        
        
        self.tree_assets.delete(*self.tree_assets.get_children())
        
        for i in range(len(self.data)):
            
            self.tree_assets.insert('', tk.END, text=self.data[i][0], values=(self.data[i][1], self.data[i][2], self.data[i][3]))
            
        self.tree_assets.bind('<Double-Button-1>', self.select_item)
        
    def select_item(self, event):
        curItem = self.tree_assets.focus()
        if curItem:
            item = self.tree_assets.item(curItem)
            self.controller.item = item["text"]
            # Gets item ID currently clicked and switches to view frame
            self.controller.show_frame("view")

    def new(self):
        self.cur = self.controller.cur
        userid = self.cur.execute(f"""
                         
                         SELECT id FROM Users WHERE username="{self.controller.user}"
                         
                         """).fetchone()[0] # Get userid based off logged-in user
        
        
        
        self.cur.execute(f'''

                        INSERT INTO Assets (name, user, location, "serial number") VALUES ("New Asset",{userid},1,"None")

                        ''') # Create item in database
        self.controller.conn.commit()

        self.data = self.cur.execute('''

                        SELECT id
                        FROM Assets
                        ORDER BY id DESC
                        LIMIT 1


''')
        self.newid = self.data.fetchone()[0]
        self.controller.item = self.newid
        self.controller.show_frame("view")
        