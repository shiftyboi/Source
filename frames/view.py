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

        # --- TKINTER ITEM DECLARATIONS ---

        self.txt_id = tk.StringVar()
        self.txt_user = tk.StringVar()
        self.txt_name = tk.StringVar()
        self.txt_ent_name = tk.StringVar()
        self.txt_ent_serial = tk.StringVar()

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

        self.lb_serial = tk.Label(self, text="SERIAL:", font=("Arial", 15))
        self.lb_serial.grid(row=3,column=0,sticky="w")

        self.btn_lend = tk.Button(
            self, text="Lend Item", font=("Arial", 15), command=lambda: self.lend()
        )
        self.btn_lend.grid(row=1, column=1, sticky="nw")

        self.btn_delete = tk.Button(
            self, text="Delete Item", font=("Arial", 15), command=lambda: self.delete()
        )
        self.btn_delete.grid(row=0, column=1, sticky="nw")

        self.btn_save = tk.Button(self, text="Save changes", font=("Arial", 15), command=lambda: self.save())
        self.btn_save.grid(row=2, column=1, sticky="")
        
        self.ent_name = tk.Entry(self, textvariable=self.txt_ent_name, font=("Arial", 15))
        self.ent_name.grid(row=2, column=0, sticky="e")

        self.btn_back = tk.Button(self, text="← Back", command=lambda: self.controller.show_frame("index"))
        self.btn_back.grid(row=0, column=2, sticky="")

        self.ent_serial = tk.Entry(self, textvariable=self.txt_ent_serial, font=("Arial", 15))
        self.ent_serial.grid(row=3, column=0, sticky="e")

    def lend(self):
        userid = self.cur.execute(f"""
                         
                         SELECT id FROM Users WHERE username="{self.controller.user}"
                         
                         """) 

        
        userid = userid.fetchall()
        
        currentid = self.cur.execute(f'''

                        SELECT id FROM Users WHERE username="{self.currentuser}"

                            ''') # Get current user's id
        
        self.cur.execute(f"""

                        INSERT INTO Alerts (device, recipient, lender)
                        VALUES ("{self.item}", {currentid.fetchone()[0]}, {userid[0][0]})

                    """) # Create alert

        
        self.cur.execute(f"""
                         
                         UPDATE Assets
                         SET user={userid[0][0]}, date_borrowed=datetime('now')
                         WHERE id={self.item}
                         
                         """) # Update assets to feature new user

        self.controller.conn.commit()

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
        serial = self.txt_ent_serial.get()
        
        
        self.cur.execute(f'''

                        UPDATE Assets
                        SET name = "{name}",
                        "serial number" = "{serial}"
                        WHERE id = {self.item}
                        
''')
        self.controller.conn.commit()
    
    
    
    
    def refresh(self):
        self.item = self.controller.item
        self.cur = (
            self.controller.cur
        )  # Borrowing variables from app class for ease of use

        
        self.data = self.cur.execute(f"""
                                     
                                     SELECT Assets.id, Users.username, Assets.name, Rooms.name, Assets."serial number"
                                     FROM Assets
                                     JOIN Users on Assets.user=Users.id
                                     JOIN Rooms on Assets.location=Rooms.id
                                     WHERE Assets.id={self.item}
                                     
                                     """)  # Grab data needed from the database


        self.unwrapped_data = self.data.fetchone()
        
        self.txt_id.set(f"ID: {self.unwrapped_data[0]}")
        self.currentuser = self.unwrapped_data[1]
        self.txt_user.set(f"USER: {self.unwrapped_data[1]}")
        self.txt_name.set("NAME:")
        self.txt_ent_name.set(self.unwrapped_data[2])
        self.txt_ent_serial.set(self.unwrapped_data[4])

        self.controller.geometry("600x600")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
