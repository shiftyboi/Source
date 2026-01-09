import tkinter as tk
import sqlite3


class fr_view(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.name = "view"

        self.item = None
        self.cur: sqlite3.Cursor  # Set later in refresh function
        self.data = None

        self.txt_id = tk.StringVar()
        self.txt_user = tk.StringVar()
        self.txt_name = tk.StringVar()
        self.txt_ent_name = tk.StringVar()

        self.lb_id = tk.Label(
            self, text="ID: null", font=("Arial", 15), textvariable=self.txt_id
        )
        self.lb_id.grid(row=0, column=0, sticky="nw", columnspan=2)

        self.lb_user = tk.Label(
            self, text="USER: null", font=("Arial", 15), textvariable=self.txt_user
        )
        self.lb_user.grid(row=1, column=0, sticky="nw", columnspan=2)

        self.lb_name = tk.Label(
            self, text="NAME: null", font=("Arial", 15), textvariable=self.txt_name
        )
        self.lb_name.grid(row=2, column=0, sticky="w",columnspan=2)

        self.btn_lend = tk.Button(
            self, text="Lend Item", font=("Arial", 15), command=lambda: self.lend()
        )
        self.btn_lend.grid(row=1, column=1, sticky="nw")

        self.btn_delete = tk.Button(
            self, text="Delete Item", font=("Arial", 15), command=lambda: self.delete()
        )
        self.btn_delete.grid(row=0, column=1, sticky="nw")

        self.btn_save = tk.Button(self, text="Save name", font=("Arial", 15), command=lambda: self.save())
        self.btn_save.grid(row=2, column=1, sticky="")
        
        self.ent_name = tk.Entry(self, textvariable=self.txt_ent_name, font=("Arial", 15))
        self.ent_name.grid(row=2, column=0, sticky="e")

        self.btn_back = tk.Button(self, text="← Back", command=lambda: self.controller.show_frame("index"))
        self.btn_back.grid(row=0, column=2, sticky="")

    def lend(self):
        print("Lend triggered")
        userid = self.cur.execute(f"""
                         
                         SELECT id FROM Users WHERE username="{self.controller.user}"
                         
                         """)

        self.cur.execute(f"""
                         
                         UPDATE Assets
                         SET user={userid.fetchone()[0]}
                         WHERE id={self.item}
                         
                         """)

        self.controller.conn.commit()

        print("User changed")

    def delete(self):
        self.item = self.controller.item
        self.cur = self.controller.cur

        self.cur.execute(f"""

                        DELETE FROM Assets
                        WHERE id={self.item}

        """)

        self.controller.conn.commit()
        self.controller.show_frame("index")
    
    def save(self):
        self.item = self.controller.item
        self.cur = self.controller.cur

        name = self.txt_ent_name.get()    
        
        
        self.cur.execute(f'''

                        UPDATE Assets
                        SET name = "{name}"
                        WHERE id = {self.item}
                        
''')
        self.controller.conn.commit()
    
    
    
    
    def refresh(self):
        self.item = self.controller.item
        self.cur = (
            self.controller.cur
        )  # Borrowing variables from app class for ease of use

        
        self.data = self.cur.execute(f"""
                                     
                                     SELECT Assets.id, Users.username, Assets.name, Rooms.name
                                     FROM Assets
                                     JOIN Users on Assets.user=Users.id
                                     JOIN Rooms on Assets.location=Rooms.id
                                     WHERE Assets.id={self.item}
                                     
                                     """)  # Grab data needed from the database


        self.unwrapped_data = self.data.fetchone()
        
        self.txt_id.set(f"ID: {self.unwrapped_data[0]}")
        self.txt_user.set(f"USER: {self.unwrapped_data[1]}")
        self.txt_name.set("NAME:")
        self.txt_ent_name.set(self.unwrapped_data[2])

        self.controller.geometry("600x600")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
