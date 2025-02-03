import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import os

# Create database and tables
def setup_db():
    conn = sqlite3.connect("recipe_planner.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
                        recipe_id TEXT,
                        recipe_name TEXT,
                        raw_material_id TEXT,
                        raw_material_name TEXT,
                        quantity_per_batch REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS production (
                        production_date TEXT,
                        recipe_id TEXT,
                        batch_quantity INTEGER)''')

    conn.commit()
    conn.close()

setup_db()  # Run this once when the app starts


# Function to insert recipe data
def add_recipe():
    conn = sqlite3.connect("recipe_planner.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes VALUES (?, ?, ?, ?, ?)", 
                   (recipe_id_var.get(), recipe_name_var.get(), raw_material_id_var.get(), raw_material_name_var.get(), quantity_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Recipe added successfully!")
    recipe_id_var.set("")
    recipe_name_var.set("")
    raw_material_id_var.set("")
    raw_material_name_var.set("")
    quantity_var.set("")


# Function to insert production data
def add_production():
    conn = sqlite3.connect("recipe_planner.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO production VALUES (?, ?, ?)", 
                   (production_date_var.get(), production_recipe_id_var.get(), batch_quantity_var.get()))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Production schedule added successfully!")
    production_date_var.set("")
    production_recipe_id_var.set("")
    batch_quantity_var.set("")


# Function to calculate raw material requirements
def calculate_requirements():
    conn = sqlite3.connect("recipe_planner.db")
    
    df_production = pd.read_sql("SELECT * FROM production", conn)
    df_recipes = pd.read_sql("SELECT * FROM recipes", conn)
    conn.close()

    # Ensure recipe_id is considered to distinguish different batch quantities
    df = df_production.merge(df_recipes, on=["recipe_id"])
    df["total_required"] = df["batch_quantity"] * df["quantity_per_batch"]

    # Group by recipe_id, raw_material_id, and raw_material_name to distinguish materials per recipe
    summary = df.groupby(["recipe_id", "raw_material_id", "raw_material_name"])["total_required"].sum().reset_index()

    # Clear the treeview
    for row in summary_tree.get_children():
        summary_tree.delete(row)

    # Insert new data
    for _, row in summary.iterrows():
        summary_tree.insert("", "end", values=(row["recipe_id"], row["raw_material_id"], row["raw_material_name"], row["total_required"]))

    # Export data to CSV
    summary.to_csv("raw_material_summary.csv", index=False)
    messagebox.showinfo("Export", "Raw material requirements saved as raw_material_summary.csv!")

# Function to delete a production entry
def delete_production():
    conn = sqlite3.connect("recipe_planner.db")
    cursor = conn.cursor()

    production_date = delete_production_date_var.get()
    recipe_id = delete_production_recipe_id_var.get()
    batch_quantity = delete_batch_quantity_var.get()


    cursor.execute("DELETE FROM production WHERE production_date = ? AND recipe_id = ? AND batch_quantity = ?", 
                   (production_date, recipe_id, batch_quantity))

    if cursor.rowcount > 0:
        messagebox.showinfo("Success", f"Deleted production entry for Recipe ID {recipe_id} on {production_date} with batch quantity {batch_quantity}.")
    else:
        messagebox.showwarning("Not Found", "No matching entry found.")

    conn.commit()
    conn.close()

    delete_production_date_var.set("")
    delete_production_recipe_id_var.set("")
    delete_batch_quantity_var.set("")


# Create Tkinter GUI
root = tk.Tk()
root.title("Recipe & Production Planner")
root.geometry("600x600")

# Recipe Section
ttk.Label(root, text="Add Recipe", font=("Arial", 12, "bold")).pack(pady=5)

frame1 = ttk.Frame(root)
frame1.pack(pady=5)

recipe_id_var = tk.StringVar()
recipe_name_var = tk.StringVar()
raw_material_id_var = tk.StringVar()
raw_material_name_var = tk.StringVar()
quantity_var = tk.DoubleVar()

ttk.Label(frame1, text="Recipe ID:").grid(row=0, column=0, padx=5, pady=2)
ttk.Entry(frame1, textvariable=recipe_id_var).grid(row=0, column=1)

ttk.Label(frame1, text="Recipe Name:").grid(row=1, column=0, padx=5, pady=2)
ttk.Entry(frame1, textvariable=recipe_name_var).grid(row=1, column=1)

ttk.Label(frame1, text="Raw Material ID:").grid(row=2, column=0, padx=5, pady=2)
ttk.Entry(frame1, textvariable=raw_material_id_var).grid(row=2, column=1)

ttk.Label(frame1, text="Raw Material Name:").grid(row=3, column=0, padx=5, pady=2)
ttk.Entry(frame1, textvariable=raw_material_name_var).grid(row=3, column=1)

ttk.Label(frame1, text="Quantity per Batch (kg):").grid(row=4, column=0, padx=5, pady=2)
ttk.Entry(frame1, textvariable=quantity_var).grid(row=4, column=1)

ttk.Button(frame1, text="Add Recipe", command=add_recipe).grid(row=5, columnspan=2, pady=5)


# Production Section
ttk.Label(root, text="Add Production Schedule", font=("Arial", 12, "bold")).pack(pady=5)

frame2 = ttk.Frame(root)
frame2.pack(pady=5)

production_date_var = tk.StringVar()
production_recipe_id_var = tk.StringVar()
batch_quantity_var = tk.IntVar()

ttk.Label(frame2, text="Production Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2)
ttk.Entry(frame2, textvariable=production_date_var).grid(row=0, column=1)

ttk.Label(frame2, text="Recipe ID:").grid(row=1, column=0, padx=5, pady=2)
ttk.Entry(frame2, textvariable=production_recipe_id_var).grid(row=1, column=1)

ttk.Label(frame2, text="Batch Quantity:").grid(row=2, column=0, padx=5, pady=2)
ttk.Entry(frame2, textvariable=batch_quantity_var).grid(row=2, column=1)

ttk.Button(frame2, text="Add Production", command=add_production).grid(row=3, columnspan=2, pady=5)


# Raw Material Summary
ttk.Label(root, text="Raw Material Requirements", font=("Arial", 12, "bold")).pack(pady=5)

frame3 = ttk.Frame(root)
frame3.pack(pady=5)

summary_tree = ttk.Treeview(frame3, columns=("Material ID", "Material Name", "Recipe ID", "Total Required"), show="headings")
summary_tree.heading("Material ID", text="Material ID")
summary_tree.heading("Material Name", text="Material Name")
summary_tree.heading("Recipe ID", text="Recipe ID")
summary_tree.heading("Total Required", text="Total Required (kg)")
summary_tree.pack()

ttk.Button(root, text="Calculate Requirements", command=calculate_requirements).pack(pady=10)

# Production Deletion Section
ttk.Label(root, text="Delete Production Entry", font=("Arial", 12, "bold")).pack(pady=5)

frame4 = ttk.Frame(root)
frame4.pack(pady=5)

delete_production_date_var = tk.StringVar()
delete_production_recipe_id_var = tk.StringVar()
delete_batch_quantity_var = tk.IntVar()

ttk.Label(frame4, text="Production Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2)
ttk.Entry(frame4, textvariable=delete_production_date_var).grid(row=0, column=1)

ttk.Label(frame4, text="Recipe ID:").grid(row=1, column=0, padx=5, pady=2)
ttk.Entry(frame4, textvariable=delete_production_recipe_id_var).grid(row=1, column=1)

ttk.Label(frame4, text="Batch Quantity:").grid(row=2, column=0, padx=5, pady=2)
ttk.Entry(frame4, textvariable=delete_batch_quantity_var).grid(row=2, column=1)

ttk.Button(frame4, text="Delete Production Entry", command=delete_production).grid(row=3, columnspan=2, pady=5)


# Run the GUI
root.mainloop()