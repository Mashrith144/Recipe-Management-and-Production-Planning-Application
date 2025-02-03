import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Function to fetch raw material requirements
def fetch_materials():
    production_date = date_entry.get()
    conn = sqlite3.connect("recipe_planner.db")
    cursor = conn.cursor()

    query = """
    SELECT rm.RawMaterialID, rm.RawMaterialName, 
           SUM(r.QuantityPerBatch * p.BatchQuantity) AS TotalRequired
    FROM recipes r
    JOIN production p ON r.RecipeID = p.RecipeID
    JOIN raw_materials rm ON r.RawMaterialID = rm.RawMaterialID
    WHERE p.ProductionDate = ?
    GROUP BY rm.RawMaterialID;
    """
    
    cursor.execute(query, (production_date,))
    data = cursor.fetchall()
    conn.close()

    # Clear existing table data
    for row in tree.get_children():
        tree.delete(row)

    if data:
        for row in data:
            tree.insert("", "end", values=row)
    else:
        messagebox.showinfo("No Data", f"No production data found for {production_date}")

# Create GUI window
root = tk.Tk()
root.title("Raw Material Calculator")
root.geometry("500x400")

# Input field
tk.Label(root, text="Enter Production Date (YYYY-MM-DD):").pack(pady=5)
date_entry = tk.Entry(root)
date_entry.pack(pady=5)

# Fetch button
fetch_button = tk.Button(root, text="Get Raw Material Requirements", command=fetch_materials)
fetch_button.pack(pady=10)

# Table to display data
columns = ("Raw Material ID", "Raw Material Name", "Total Required (kg)")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(pady=10, fill="both", expand=True)

# Run the GUI app
root.mainloop()