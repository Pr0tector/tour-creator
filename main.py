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
        for text in ["Map", "Add Location", "Add Informations", "Edit Location", "Edit Informations", "Delete Location", "Delete Informations"]:
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

    form_active = False
    def navigate_to(self, page_name):
        if self.form_active: 
            self.content_frame.form_frame.pack_forget()
        match page_name:
            case "Add Location":
                self.content_label.pack_forget()
                self.content_frame.form_frame = Frame(self.content_frame, bg="#000000", height=600, width=600, pady=20, padx=50)
                self.content_frame.form_frame.pack()
                self.form_active = True
                self.location_inputs = ["Name", "X-Coordinate", "Y-Coordinate"]
                self.location_values = []
                for input in self.location_inputs:
                    input_frame = Frame(self.content_frame.form_frame, bg="#000000", pady=20)
                    input_frame.pack()
                    label = ctk.CTkLabel(input_frame, text="Enter Location " + input + ": ", width=200)
                    label.pack(side="left")
                    textbox = ctk.CTkEntry(input_frame)
                    textbox.pack(side="right")
                    self.location_values.append(textbox)
                input_frame = Frame(self.content_frame.form_frame, bg="#000000", pady=20)
                input_frame.pack()
                button = ctk.CTkButton(input_frame, text="Submit", command=self.add_location, fg_color="#343638")
                button.pack(side="left")
            case _:
                self.content_label = Label(self.content_frame, text="Tour Creator", bg="#1f6b2e", font=("Arial", 24), anchor="center")
                self.content_label.pack(expand=True)
                print("XD")

    def add_location(self):
        values = [textbox.get().strip() for textbox in self.location_values]
        print(values)
        #walidacja danych i dodawanie nowych lokalizacji do bazy danyuch Mikołaj

    def get_all_locations(self):
        print("XD")
        #zwracanie listy nazw i id wszystkich lokalizacji z bazy danych najlepiej w formie słownika np.: locations = [{"Id": value, "Name": value}] Mikołaj
    

app = Navbar()
app.mainloop()

