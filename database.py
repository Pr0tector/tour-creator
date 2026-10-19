import sqlite3

DATABASE_NAME = "database.db"

def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Table with places
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS places (
            place_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            coordinate_x REAL,
            coordinate_y REAL
        )
    """)

    # Table with visiting information and descriptions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS descriptions (
            description_id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_id INTEGER NOT NULL,
            opening_time TEXT,
            closing_time TEXT,
            visit_duration TEXT,
            entry_price REAL,
            country TEXT,
            city TEXT,
            address TEXT,
            description TEXT,

            FOREIGN KEY (place_id)
                REFERENCES places(place_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database and tables were created successfully.")


def add_example_data():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Add example places
    cursor.execute("""
        INSERT INTO places (name, coordinate_x, coordinate_y)
        VALUES (?, ?, ?)
    """, ("Wawel Royal Castle", 50.0541115, 19.935423))

    wawel_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO places (name, coordinate_x, coordinate_y)
        VALUES (?, ?, ?)
    """, ("Main Market Square", 50.0618971, 19.934181))

    market_square_id = cursor.lastrowid

    # Add information connected to Wawel Royal Castle
    cursor.execute("""
        INSERT INTO descriptions (
            place_id,
            opening_time,
            closing_time,
            visit_duration,
            entry_price,
            country,
            city,
            address,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        wawel_id,
        "9:00",
        "17:00",
        "2 hours",
        35.00,
        "Poland",
        "Krakow",
        "Wawel 5, 31-001 Krakow",
        "Historic royal castle and museum."
    ))

    # Add information connected to Main Market Square
    cursor.execute("""
        INSERT INTO descriptions (
            place_id,
            opening_time,
            closing_time,
            visit_duration,
            entry_price,
            country,
            city,
            address,
            description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        market_square_id,
        "00:00",
        "24:00",
        "1 hour 30 minutes",
        0.00,
        "Poland",
        "Krakow",
        "Rynek Glowny, 31-422 Krakow",
        "The central square of Krakow."
    ))

    connection.commit()
    connection.close()

    print("Example data was added successfully.")


if __name__ == "__main__":
    create_database()
    add_example_data()