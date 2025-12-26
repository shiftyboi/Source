import tkinter as tk
import sqlite3, os.path, hashlib
from tkinter import messagebox


class fr_login(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.name = "login"

        self.shown = 0

        self.var_username = tk.StringVar()
        self.var_password = tk.StringVar()

        self.lb_username = tk.Label(self, text="Username:", font=("Arial", 15)).grid(
            row=0, column=0, pady=2
        )  # Labels
        self.lb_password = tk.Label(self, text="Password:", font=("Arial", 15)).grid(
            row=1, column=0, pady=2
        )

        self.ent_username = tk.Entry(
            self, textvariable=self.var_username, width=30, font=("Arial", 15)
        )  # Entries
        self.ent_username.grid(row=0, column=1, pady=2)
        self.ent_password = tk.Entry(
            self, textvariable=self.var_password, width=30, show="*", font=("Arial", 15)
        )
        self.ent_password.grid(row=1, column=1, pady=2)

        self.btn_login = tk.Button(
            self, text="Log in", command=lambda: self.login(), font=("Arial", 15)
        )  # Buttons
        self.btn_login.grid(row=2, column=1, pady=2, sticky="e", padx=20)
        self.btn_show = tk.Button(
            self,
            text="Show Password",
            command=lambda: self.toggle_show(),
            font=("Arial", 10),
        )
        self.btn_show.grid(row=1, column=2, pady=2, sticky="w")

        # self.btn_switch = tk.Button(self, text="DEBUG Switch to menu", command=lambda: controller.show_frame("menu"), font=("Arial", 15)).grid(row=2, column=0, pady=2)

    def login(self):
        txt_username = self.var_username.get()
        txt_password = self.var_password.get()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = BASE_DIR + "/../../main.db"

        obj_db = sqlite3.connect(db_path)
        cur = obj_db.cursor()

        hash_password = hashlib.sha1(txt_password.encode()).hexdigest()

        try:
            hash_stored = cur.execute(
                f"SELECT hash FROM Users WHERE username='{txt_username}'"
            ).fetchone()[0]
        except:
            messagebox.showerror("Login failed", "Please check username and password")

        if "hash_stored" in locals():
            if hash_password == hash_stored:
                self.controller.user = txt_username
                self.controller.cur = cur
                self.controller.show_frame("menu")
            else:
                messagebox.showerror(
                    "Login failed", "Please check username and password"
                )

    def toggle_show(self):  # Functionality of show password / hide password button
        if self.shown:
            self.ent_password.config(show="*")
            self.btn_show.config(text="Show Password")
            self.shown = 0

        else:
            self.ent_password.config(show="")
            self.btn_show.config(text="Hide Password")
            self.shown = 1

    def refresh(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
