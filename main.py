import customtkinter as ctk
from tkinter import *
import math
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("database.db")

class Navbar(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tour Creator")
        self.geometry("1400x1000")
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
        for text in ["Map", "Add Location", "Add Informations", "Edit Location", "Edit Informations"]:
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
    table_active = False
    def navigate_to(self, page_name, id = -1):
        if self.form_active: 
            self.content_frame.form_frame.pack_forget()
            self.form_active = False
        if self.table_active: 
            self.content_frame.table_frame.pack_forget()
            self.table_active = False
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
                self.location_message = ctk.CTkLabel(self.content_frame.form_frame, text="")
                self.location_message.pack(pady=(0, 10))
            case "Add Informations":
                self.content_label.pack_forget()
                self.content_frame.form_frame = ctk.CTkScrollableFrame(
                    self.content_frame,
                    fg_color="#000000",
                )
                self.content_frame.form_frame.pack(
                    fill="both", expand=True, padx=20, pady=20
                )
                self.form_active = True
                self.location_inputs = ["Name", "Opening Time", "Closing Time", "Visit Duration", "Entry Price", "Country", "City", "Address", "Description"]
                self.location_values = []
                for input in self.location_inputs:
                    input_frame = Frame(self.content_frame.form_frame, bg="#000000", pady=20)
                    input_frame.pack()
                    if(input == "Name"):
                        label = ctk.CTkLabel(input_frame, text="Select Location " + input + ": ", width=200)
                        label.pack(side="left")
                        locations = self.get_all_locations_id_name()
                        select = ctk.CTkOptionMenu(input_frame, values=locations, fg_color="#343638", button_color="#232527") 
                        select.pack(side="right")
                        self.location_values.append(select)
                    elif(input == "Description"):
                        label = ctk.CTkLabel(input_frame, text="Enter Location " + input + ": ", width=200)
                        label.pack(side="left")
                        textbox = ctk.CTkTextbox(input_frame)
                        textbox.pack(side="right")
                        self.location_values.append(textbox)
                    else:
                        label = ctk.CTkLabel(input_frame, text="Enter Location " + input + ": ", width=200)
                        label.pack(side="left")
                        textbox = ctk.CTkEntry(input_frame)
                        textbox.pack(side="right")
                        self.location_values.append(textbox)
                input_frame = Frame(self.content_frame.form_frame, bg="#000000", pady=20)
                input_frame.pack()
                button = ctk.CTkButton(input_frame, text="Submit", command=self.add_description, fg_color="#343638")
                button.pack(side="left")
                self.location_message = ctk.CTkLabel(self.content_frame.form_frame, text="")
                self.location_message.pack(pady=(0, 10))
            case "Edit Location":
                self.content_label.pack_forget()
                self.content_frame.table_frame = ctk.CTkScrollableFrame(
                                    self.content_frame,
                                    fg_color="#000000",
                                )
                self.content_frame.table_frame.pack(
                                    fill="both", expand=True, padx=20, pady=20
                                )
                self.table_active = True
                locations = self.get_all_locations_full()
                headers = ["ID", "Location Name", "X-Coordinate", "Y-Coordinate", "Edit", "Delete"]
                for i in range(len(headers)):
                    label = ctk.CTkLabel(self.content_frame.table_frame, text=headers[i], font=("Arial", 16, "bold"))
                    label.grid(row=0, column=i, padx=5, pady=5)
                for i in range(len(locations)):
                    label = ctk.CTkLabel(self.content_frame.table_frame, text=locations[i]["place_id"], font=("Arial", 12))
                    label.grid(row=i+1, column=0, padx=5, pady=5)
                    label = ctk.CTkLabel(self.content_frame.table_frame, text=locations[i]["name"], font=("Arial", 12))
                    label.grid(row=i+1, column=1, padx=5, pady=5)
                    label = ctk.CTkLabel(self.content_frame.table_frame, text=locations[i]["coordinate_x"], font=("Arial", 12))
                    label.grid(row=i+1, column=2, padx=5, pady=5)
                    label = ctk.CTkLabel(self.content_frame.table_frame, text=locations[i]["coordinate_y"], font=("Arial", 12))
                    label.grid(row=i+1, column=3, padx=5, pady=5)
                    update_button = ctk.CTkButton(self.content_frame.table_frame, text="Edit",  command=lambda x="EL", y=locations[i]["place_id"]: self.navigate_to(x, y), fg_color="#198926")
                    update_button.grid(row=i+1, column=4, padx=5, pady=5)
                    delete_button = ctk.CTkButton(self.content_frame.table_frame, text="Delete",  command=lambda x=locations[i]["place_id"]: self.delete_location(x), fg_color="#C30D0D")
                    delete_button.grid(row=i+1, column=5, padx=5, pady=5)
            case "EL":
                self.content_label.pack_forget()
                self.content_frame.form_frame = Frame(self.content_frame, bg="#000000", height=600, width=600, pady=20, padx=50)
                self.content_frame.form_frame.pack()
                self.form_active = True
                locations = self.get_all_locations_full()
                location = ["NULL","NULL","NULL"]
                for i in range(len(locations)):
                    if(locations[i]["place_id"] == id):
                        location[0] = locations[i]["name"]
                        location[1] = locations[i]["coordinate_x"]
                        location[2] = locations[i]["coordinate_y"]
                self.location_inputs = ["Name", "X-Coordinate", "Y-Coordinate"]
                self.location_values = []
                for i, input in enumerate(self.location_inputs):
                    input_frame = Frame(self.content_frame.form_frame, bg="#000000", pady=20)
                    input_frame.pack()
                    label = ctk.CTkLabel(input_frame, text="Enter Location " + input + ": ", width=200)
                    label.pack(side="left")
                    textbox = ctk.CTkEntry(input_frame)
                    textbox.insert(0, location[i])
                    textbox.pack(side="right")
                    self.location_values.append(textbox)
                input_frame = Frame(self.content_frame.form_frame, bg="#000000", pady=20)
                input_frame.pack()
                button = ctk.CTkButton(input_frame, text="Update", command=lambda x=id: self.update_location(x), fg_color="#343638")
                button.pack(side="left")
                self.location_message = ctk.CTkLabel(self.content_frame.form_frame, text="")
                self.location_message.pack(pady=(0, 10))
            case "Edit Informations":
                self.content_label.pack_forget()
                self.content_frame.table_frame = ctk.CTkScrollableFrame(
                                    self.content_frame,
                                    fg_color="#000000",
                                )
                self.content_frame.table_frame.pack(
                                    fill="both", expand=True, padx=20, pady=20
                                )
                self.table_active = True
                descriptions = self.get_all_description_full()
                locations = self.get_all_locations_full()
                data = []
                for i in range(len(descriptions)):
                    record = [descriptions[i]["description_id"],descriptions[i]["place_id"],"NULL",descriptions[i]["opening_time"],descriptions[i]["closing_time"],descriptions[i]["visit_duration"],descriptions[i]["entry_price"],descriptions[i]["country"],descriptions[i]["city"],descriptions[i]["address"]," ".join(descriptions[i]["description"].split()[:5])]
                    for j in range(len(locations)):
                        if(descriptions[i]["place_id"] == locations[j]["place_id"]):
                            record[2] = locations[j]["name"]
                    data.append(record)

                headers = ["ID", "Location ID", "Location Name", "Opening Time", "Closing Time", "Visit Duration", "Entry Price", "Country", "City", "Address", "Description", "Edit", "Delete"]
                for i in range(len(headers)):
                    label = ctk.CTkLabel(self.content_frame.table_frame, text=headers[i], font=("Arial", 16, "bold"))
                    label.grid(row=0, column=i, padx=5, pady=5)
                for i in range(len(data)):
                    for j in range(len(data[i])):
                        label = ctk.CTkLabel(self.content_frame.table_frame, text=data[i][j], font=("Arial", 12))
                        label.grid(row=i+1, column=j, padx=5, pady=5)
                    update_button = ctk.CTkButton(self.content_frame.table_frame, text="Edit",  command=lambda x="EI", y=data[i][1]: self.navigate_to(x, y), fg_color="#198926")
                    update_button.grid(row=i+1, column=j+1, padx=5, pady=5)
                    delete_button = ctk.CTkButton(self.content_frame.table_frame, text="Delete",  command=lambda x=data[i][1]: self.delete_description(x), fg_color="#C30D0D")
                    delete_button.grid(row=i+1, column=j+2, padx=5, pady=5)
            case "EI":
                self.content_label.pack_forget()
                self.content_frame.form_frame = Frame(self.content_frame, bg="#000000", height=600, width=600, pady=20, padx=50)
                self.content_frame.form_frame.pack()
                self.form_active = True
                descriptions = self.get_all_description_full()
                description = ["NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL"]
                for i in range(len(descriptions)):
                    if(descriptions[i]["description_id"] == id):
                        locations = self.get_all_locations_id_name()
                        for location in locations:
                            if location.split()[0].strip() == str(descriptions[i]["place_id"]):
                                description[0] = location
                        description[1] = descriptions[i]["opening_time"]
                        description[2] = descriptions[i]["closing_time"]
                        description[3] = descriptions[i]["visit_duration"]
                        description[4] = descriptions[i]["entry_price"]
                        description[5] = descriptions[i]["country"]  
                        description[6] = descriptions[i]["city"]
                        description[7] = descriptions[i]["address"]
                        description[8] = descriptions[i]["description"]                     
                self.location_message = ctk.CTkLabel(self.content_frame.form_frame, text="")
                self.location_message.pack(pady=(0, 10))
                self.form_active = True
                self.location_inputs = ["Name", "Opening Time", "Closing Time", "Visit Duration", "Entry Price", "Country", "City", "Address", "Description"]
                self.location_values = []
                for i,input in enumerate(self.location_inputs):
                    input_frame = Frame(self.content_frame.form_frame, bg="#000000", pady=20)
                    input_frame.pack()
                    if(input == "Name"):
                        label = ctk.CTkLabel(input_frame, text="Select Location " + input + ": ", width=200)
                        label.pack(side="left")
                        locations = self.get_all_locations_id_name()
                        select = ctk.CTkOptionMenu(input_frame, values=locations, fg_color="#343638", button_color="#232527") 
                        select.set(description[i])
                        select.pack(side="right")
                        self.location_values.append(select)
                    elif(input == "Description"):
                        label = ctk.CTkLabel(input_frame, text="Enter Location " + input + ": ", width=200)
                        label.pack(side="left")
                        textbox = ctk.CTkTextbox(input_frame)
                        textbox.insert("1.0", description[i])
                        textbox.pack(side="right")
                        self.location_values.append(textbox)
                    else:
                        label = ctk.CTkLabel(input_frame, text="Enter Location " + input + ": ", width=200)
                        label.pack(side="left")
                        textbox = ctk.CTkEntry(input_frame)
                        textbox.insert(0, description[i])
                        textbox.pack(side="right")
                        self.location_values.append(textbox)
                input_frame = Frame(self.content_frame.form_frame, bg="#000000", pady=20)
                input_frame.pack()
                button = ctk.CTkButton(input_frame, text="Update", command=lambda x=id: self.update_description(x), fg_color="#343638")
                button.pack(side="left")
                self.location_message = ctk.CTkLabel(self.content_frame.form_frame, text="")
                self.location_message.pack(pady=(0, 10))
            case _:
                self.content_label = Label(self.content_frame, text="Tour Creator", bg="#1f6b2e", font=("Arial", 24), anchor="center")
                self.content_label.pack(expand=True)
                print("XD")
            

    def add_location(self):
        """Validate form fields and save a new place to the SQLite database."""
        name, x_coordinate, y_coordinate = (
            textbox.get().strip() for textbox in self.location_values
        )

        if not name:
            self.location_message.configure(
                text="Podaj nazwę lokalizacji.", text_color="#ff6b6b"
            )
            return

        try:
            x_coordinate = float(x_coordinate)
            y_coordinate = float(y_coordinate)
            if not math.isfinite(x_coordinate) or not math.isfinite(y_coordinate):
                raise ValueError
        except ValueError:
            self.location_message.configure(
                text="Współrzędne muszą być liczbami.", text_color="#ff6b6b"
            )
            return

        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute(
                    """
                    INSERT INTO places (name, coordinate_x, coordinate_y)
                    VALUES (?, ?, ?)
                    """,
                    (name, x_coordinate, y_coordinate),
                )
        except sqlite3.Error as error:
            self.location_message.configure(
                text=f"Nie udało się zapisać lokalizacji: {error}", text_color="#ff6b6b"
            )
            return

        for textbox in self.location_values:
            textbox.delete(0, END)
        self.location_message.configure(
            text="Lokalizacja została dodana.", text_color="#61d46b"
        )

    def add_description(self):
        """Validate and save information associated with the selected place."""
        (
            place,
            opening_time,
            closing_time,
            visit_duration,
            entry_price,
            country,
            city,
            address,
        ) = (textbox.get().strip() for textbox in self.location_values[:-1])
        description = self.location_values[-1].get("1.0", "end").strip()

        try:
            place_id = int(place.split(maxsplit=1)[0])
        except (IndexError, ValueError):
            self.location_message.configure(
                text="Wybierz poprawną lokalizację.", text_color="#ff6b6b"
            )
            return

        hours, separator, minutes = visit_duration.partition(":")
        if (
            not separator
            or not hours.isdigit()
            or not minutes.isdigit()
            or int(minutes) > 59
        ):
            self.location_message.configure(
                text="Czas wizyty podaj w formacie godziny:minuty, np. 1:30.",
                text_color="#ff6b6b",
            )
            return
        visit_duration = f"{int(hours)}:{int(minutes):02d}"

        try:
            entry_price = float(entry_price)
            if not math.isfinite(entry_price) or entry_price < 0:
                raise ValueError
        except ValueError:
            self.location_message.configure(
                text="Cena wstępu musi być liczbą większą lub równą 0.",
                text_color="#ff6b6b",
            )
            return

        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                place_exists = connection.execute(
                    "SELECT 1 FROM places WHERE place_id = ?", (place_id,)
                ).fetchone()
                if place_exists is None:
                    self.location_message.configure(
                        text="Wybrana lokalizacja nie istnieje w bazie.",
                        text_color="#ff6b6b",
                    )
                    return

                connection.execute(
                    """
                    INSERT INTO descriptions (
                        place_id, opening_time, closing_time, visit_duration,
                        entry_price, country, city, address, description
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        place_id,
                        opening_time,
                        closing_time,
                        visit_duration,
                        entry_price,
                        country,
                        city,
                        address,
                        description,
                    ),
                )
        except sqlite3.Error as error:
            self.location_message.configure(
                text=f"Nie udało się zapisać informacji: {error}",
                text_color="#ff6b6b",
            )
            return

        for textbox in self.location_values[1:-1]:
            textbox.delete(0, END)
        self.location_values[-1].delete("1.0", "end")
        self.location_message.configure(
            text="Informacje zostały dodane.", text_color="#61d46b"
        )

    def get_all_locations_id_name(self):
        """Return all places as dictionaries containing their ID and name."""
        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                rows = connection.execute(
                    "SELECT place_id, name FROM places ORDER BY name"
                ).fetchall()
        except sqlite3.Error as error:
            print(f"Nie udało się odczytać lokalizacji: {error}")
            return []

        return [str(place_id)+" "+name for place_id, name in rows]

    def get_all_locations_full(self):
        """Return every place record as a dictionary."""
        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.row_factory = sqlite3.Row
                rows = connection.execute(
                    """
                    SELECT place_id, name, coordinate_x, coordinate_y
                    FROM places
                    ORDER BY place_id
                    """
                ).fetchall()
        except sqlite3.Error as error:
            print(f"Nie udało się odczytać lokalizacji: {error}")
            return []

        return [dict(row) for row in rows]

    def get_all_description_full(self):
        """Return every description record as a dictionary."""
        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.row_factory = sqlite3.Row
                rows = connection.execute(
                    """
                    SELECT
                        description_id, place_id, opening_time, closing_time,
                        visit_duration, entry_price, country, city, address,
                        description
                    FROM descriptions
                    ORDER BY description_id
                    """
                ).fetchall()
        except sqlite3.Error as error:
            print(f"Nie udało się odczytać opisów: {error}")
            return []

        return [dict(row) for row in rows]

    def delete_location(self, id):
        """Delete a place and the descriptions connected to it."""
        try:
            place_id = int(id)
        except (TypeError, ValueError):
            return False, self.navigate_to("Edit Location")

        if place_id < 1:
            return False, self.navigate_to("Edit Location")

        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                location_exists = connection.execute(
                    "SELECT 1 FROM places WHERE place_id = ?", (place_id,)
                ).fetchone()
                if location_exists is None:
                    return False, self.navigate_to("Edit Location")

                # The schema does not define ON DELETE CASCADE, so remove child
                # records first to keep the database consistent.
                connection.execute(
                    "DELETE FROM descriptions WHERE place_id = ?", (place_id,)
                )
                connection.execute(
                    "DELETE FROM places WHERE place_id = ?", (place_id,)
                )
        except sqlite3.Error as error:
            print(f"Nie udało się usunąć lokalizacji: {error}")
            return False, self.navigate_to("Edit Location")

        return True, self.navigate_to("Edit Location")

    def delete_description(self, id):
        """Delete the description identified by ``id``."""
        try:
            description_id = int(id)
        except (TypeError, ValueError):
            return False, self.navigate_to("Edit Informations")

        if description_id < 1:
            return False, self.navigate_to("Edit Informations")

        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                cursor = connection.execute(
                    "DELETE FROM descriptions WHERE description_id = ?",
                    (description_id,),
                )
        except sqlite3.Error as error:
            print(f"Nie udało się usunąć opisu: {error}")
            return False, self.navigate_to("Edit Informations")

        return cursor.rowcount > 0, self.navigate_to("Edit Informations")

    def update_location(self, id):
        """Update the supplied fields of a place and return whether it exists."""
        try:
            place_id = int(id)
        except (TypeError, ValueError):
            return False, self.navigate_to("Edit Location")
        name, coordinate_x, coordinate_y = (
                    textbox.get().strip() for textbox in self.location_values
                )

        if place_id < 1:
            return False, self.navigate_to("Edit Location")

        fields = []
        values = []

        if name is not None:
            name = str(name).strip()
            if not name:
                return False
            fields.append("name = ?")
            values.append(name)

        for column, coordinate in (
            ("coordinate_x", coordinate_x),
            ("coordinate_y", coordinate_y),
        ):
            if coordinate is None:
                continue
            try:
                coordinate = float(coordinate)
                if not math.isfinite(coordinate):
                    raise ValueError
            except (TypeError, ValueError):
                return False
            fields.append(f"{column} = ?")
            values.append(coordinate)

        if not fields:
            return False, self.navigate_to("Edit Location")

        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                cursor = connection.execute(
                    f"UPDATE places SET {', '.join(fields)} WHERE place_id = ?",
                    (*values, place_id),
                )
        except sqlite3.Error as error:
            print(f"Nie udało się zaktualizować lokalizacji: {error}")
            return False, self.navigate_to("Edit Location")

        return cursor.rowcount > 0, self.navigate_to("Edit Location")

    def update_description(self, id):
        """Update the supplied fields of a description and return whether it exists."""
        try:
            description_id = int(id)
        except (TypeError, ValueError):
            return False

        if description_id < 1:
            return False

        fields = []
        values = []

        (
            place,
            opening_time,
            closing_time,
            visit_duration,
            entry_price,
            country,
            city,
            address,
        ) = (textbox.get().strip() for textbox in self.location_values[:-1])
        description = self.location_values[-1].get("1.0", "end").strip()

        try:
            place_id = int(place.split(maxsplit=1)[0])
        except (IndexError, ValueError):
            self.location_message.configure(
                text="Wybierz poprawną lokalizację.", text_color="#ff6b6b"
            )
            return

        if place_id is not None:
            try:
                place_id = int(place_id)
            except (TypeError, ValueError):
                return False
            if place_id < 1:
                return False
            fields.append("place_id = ?")
            values.append(place_id)

        for column, value in (
            ("opening_time", opening_time),
            ("closing_time", closing_time),
            ("visit_duration", visit_duration),
            ("country", country),
            ("city", city),
            ("address", address),
            ("description", description),
        ):
            if value is not None:
                fields.append(f"{column} = ?")
                values.append(str(value).strip())

        if entry_price is not None:
            try:
                entry_price = float(entry_price)
                if not math.isfinite(entry_price) or entry_price < 0:
                    raise ValueError
            except (TypeError, ValueError):
                return False
            fields.append("entry_price = ?")
            values.append(entry_price)

        if not fields:
            return False

        try:
            with sqlite3.connect(DATABASE_PATH) as connection:
                connection.execute("PRAGMA foreign_keys = ON")
                if place_id is not None:
                    place_exists = connection.execute(
                        "SELECT 1 FROM places WHERE place_id = ?", (place_id,)
                    ).fetchone()
                    if place_exists is None:
                        return False, self.navigate_to("Edit Informations")

                cursor = connection.execute(
                    f"UPDATE descriptions SET {', '.join(fields)} "
                    "WHERE description_id = ?",
                    (*values, description_id),
                )
        except sqlite3.Error as error:
            print(f"Nie udało się zaktualizować opisu: {error}")
            return False

        return cursor.rowcount > 0, self.navigate_to("Edit Informations")

if __name__ == "__main__":
    app = Navbar()
    app.mainloop()
