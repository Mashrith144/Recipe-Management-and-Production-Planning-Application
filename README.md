# 🍽 Recipe Management and Production Planning Application

## 📌 Overview
The **Recipe Management and Production Planning Application** is a Python-based tool that helps users manage recipes, track raw material requirements, and streamline production planning. The application interacts with an SQLite database to store and retrieve data related to recipes, ingredients, and production.

---

## ⚡ Features
✅ Store and update recipe details (ingredients, quantities, methods)  
✅ Calculate raw material requirements for production  
✅ Manage and modify production schedules  
✅ Automatically update and generate `raw_material_summary.csv`  
✅ View and edit database records using SQLite  

---

## 🚀 Installation Guide

### 1️⃣ Install Python and Dependencies
1. Download and install Python from [python.org](https://python.org/downloads/windows).
2. During installation, **select "Add Python to PATH"**.
3. Verify Python installation:
   ```sh
   python --version
   ```
4. Upgrade pip:
   ```sh
   python -m pip install --upgrade pip
   ```
5. Install required libraries:
   ```sh
   pip install pandas
   ```

### 2️⃣ Set Up the Project
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/RecipePlanner.git
   ```
2. Navigate to the project folder:
   ```sh
   cd RecipePlanner
   ```

### 3️⃣ Running the Application
1. Run the application:
   ```sh
   python app.py
   ```
   - This will create the SQLite database `recipe_planner.db`.
2. Load sample data into the database:
   ```sh
   python database.py
   ```
   - Expected output: `"Sample data inserted successfully!"`

### 4️⃣ Install SQLite Browser (Optional)
If you want to manually inspect or edit the database:
- Download **DB Browser for SQLite** from [sqlitebrowser.org](https://sqlitebrowser.org/).
- Open `recipe_planner.db` in SQLite Browser.

---

## 🛠 How to Use

### 1️⃣ Recipe Management
- Store and update recipe details.
- Retrieve recipe data from the database.

### 2️⃣ Production Planning
- Enter production values and calculate raw material needs.
- View updated production requirements.

### 3️⃣ Database Management
- Store, modify, and delete production data using the SQLite database.

### 4️⃣ CSV Report Generation
- A `raw_material_summary.csv` file is generated automatically.
- Any new production entries update the CSV.

---

## 🧪 Testing the Application
1. Run the app:
   ```sh
   python app.py
   ```
2. Click **"Calculate Requirements"** to compute raw material needs.
3. Modify production values and verify database updates.
4. Open `recipe_planner.db` in SQLite Browser to confirm updates.

---

## 📌 Future Enhancements
🔹 Add functionality to delete recipes  
🔹 Improve user interface for better usability  

---

## 📜 License
This project is licensed under the MIT License.

---

## 💡 Contributing
If you'd like to contribute, feel free to **fork this repo**, create a **feature branch**, and submit a **pull request**!  

---

## 🏆 Acknowledgments
Special thanks for any libraries, tools, or references used in the project.

---

### 📧 Contact
For any issues or questions, feel free to reach out.
