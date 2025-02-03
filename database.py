import sqlite3

# Connect to the database
conn = sqlite3.connect("recipe_planner.db")
cursor = conn.cursor()

# Sample recipe data
recipe_data = [
    ("R001", "Beef Sausage", "RM001", "Beef Meat", 10),
    ("R001", "Beef Sausage", "RM002", "Pork Fat", 2),
    ("R001", "Beef Sausage", "RM003", "Spices", 0.5),
    ("R002", "Chicken Patties", "RM004", "Chicken Meat", 8),
    ("R002", "Chicken Patties", "RM005", "Breading", 1.5),
    ("R002", "Chicken Patties", "RM003", "Spices", 0.2),
]

# Insert recipe data
cursor.executemany("INSERT INTO recipes VALUES (?, ?, ?, ?, ?)", recipe_data)

# Sample production data
production_data = [
    ("2025-02-05", "R001", 50),
    ("2025-02-05", "R002", 30),
]

# Insert production data
cursor.executemany("INSERT INTO production VALUES (?, ?, ?)", production_data)

# Commit and close
conn.commit()
conn.close()

print("Sample data inserted successfully!")