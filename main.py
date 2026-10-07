import customtkinter as ctk
from tkinter import *

class Navbar(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tour Creator")
        self.geometry("1200x800")
        ctk.set_appearance_mode("dark")

        self.navbar_expand = True

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.navbar_frame = Frame(self, bg="#3b9404", width=1200, height=200)
        self.navbar_frame.grid(row=0,column=0, sticky="we")

        self.content_frame = Frame(self, bg="#1c211d")
        self.content_frame.grid(row=1,column=0, sticky="wsne")

        self.toggle_button = Button(self.navbar_frame, text="=", bg="#065c0e", fg="#FFFFFF", cursor="hand2", font=("Arial", 16), relief="flat", command=self.toggle_navbar)
        self.toggle_button.pack(padx=10,pady=10, anchor="w", side="left")

        self.nav_buttons = []
        for text in ["Map", "Add Location", "Add Informations"]:
            btn = Button(self.navbar_frame, text=text, bg="#1c8c25", fg="#FFFFFF", font=("Arial, 14"), relief="flat",cursor="hand2", anchor="center", command=lambda t=text: self.navigate_to(t))
            btn.pack(fill="x", pady=5, padx=10, side="left")
            self.nav_buttons.append(btn)

        self.content_label = Label(self.content_frame, text="Tour Creator", bg="#1f6b2e", font=("Arial", 24), anchor="center")
        self.content_label.pack(expand=True)

    def toggle_navbar(self):
        if self.navbar_expand:
            self.navbar_frame.config(height=50)
            self.toggle_button.config(text="x", font=("Arial", 12))
            for btn in self.nav_buttons:
                btn.pack_forget()
            self.navbar_expand = False
        else:
            self.navbar_frame.config(height=200)
            self.toggle_button.config(text="=", font=("Arial", 16), relief="flat")
            for btn in self.nav_buttons:
                btn.pack(fill="x", pady=5, padx=10, side="left")
            self.navbar_expand = True

    def navigate_to(self, page_name):
        self.content_label.config(text=f"{page_name}")

app = Navbar()
app.mainloop()

# window = ctk.CTk()
# window.title("Tour Creator")
# window.geometry("1200x800")
# ctk.set_appearance_mode("dark")
# window.mainloop()