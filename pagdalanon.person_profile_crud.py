import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS person_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        city TEXT NOT NULL,
        age INTEGER NOT NULL,
        occupation TEXT NOT NULL
    )
""")

conn.commit()

def add_person():
    full_name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    city = city_entry.get()
    age = age_entry.get()
    occupation = occupation_entry.get()

    if (full_name == "" or email == "" or phone == "" or
            city == "" or age == "" or occupation == ""):
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute("""
        INSERT INTO person_profiles
        (full_name, email, phone, city, age, occupation)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (full_name, email, phone, city, age, occupation))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Person added successfully."
    )

    clear_fields()
    display_persons()

def display_persons():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM person_profiles")
    persons = cursor.fetchall()

    for person in persons:
        tree.insert("", tk.END, values=person)

def update_person():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a person to update."
        )
        return

    person_id = tree.item(selected[0])["values"][0]

    full_name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    city = city_entry.get()
    age = age_entry.get()
    occupation = occupation_entry.get()

    if (full_name == "" or email == "" or phone == "" or
            city == "" or age == "" or occupation == ""):
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return

    cursor.execute("""
        UPDATE person_profiles
        SET full_name = ?,
            email = ?,
            phone = ?,
            city = ?,
            age = ?,
            occupation = ?
        WHERE id = ?
    """, (
        full_name,
        email,
        phone,
        city,
        age,
        occupation,
        person_id
    ))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Person updated successfully."
    )

    clear_fields()
    display_persons()

def delete_person():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a person to delete."
        )
        return

    person_id = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this person?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM person_profiles WHERE id = ?",
            (person_id,)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Person deleted successfully."
        )

        clear_fields()
        display_persons()
        
def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    occupation_entry.delete(0, tk.END)

def select_person(event):
    selected = tree.selection()

    if selected:
        person = tree.item(selected[0])["values"]

        clear_fields()

        name_entry.insert(0, person[1])
        email_entry.insert(0, person[2])
        phone_entry.insert(0, person[3])
        city_entry.insert(0, person[4])
        age_entry.insert(0, person[5])
        occupation_entry.insert(0, person[6])

root = tk.Tk()
root.title("Person Profile Management System")
root.geometry("1000x650")

title_label = tk.Label(
    root,
    text="Person Profile Management System",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=15)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(
    input_frame,
    text="Full Name:"
).grid(row=0, column=0, padx=5, pady=5, sticky="e")

name_entry = tk.Entry(
    input_frame,
    width=35
)
name_entry.grid(row=0, column=1, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Email:"
).grid(row=1, column=0, padx=5, pady=5, sticky="e")

email_entry = tk.Entry(
    input_frame,
    width=35
)
email_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(
    input_frame,
    text="Phone:"
).grid(row=2, column=0, padx=5, pady=5, sticky="e")

phone_entry = tk.Entry(
    input_frame,
    width=35
)
phone_entry.grid(row=2, column=1, padx=5, pady=5)


tk.Label(
    input_frame,
    text="City:"
).grid(row=3, column=0, padx=5, pady=5, sticky="e")

city_entry = tk.Entry(
    input_frame,
    width=35
)
city_entry.grid(row=3, column=1, padx=5, pady=5)


tk.Label(
    input_frame,
    text="Age:"
).grid(row=4, column=0, padx=5, pady=5, sticky="e")

age_entry = tk.Entry(
    input_frame,
    width=35
)
age_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(
    input_frame,
    text="Occupation:"
).grid(row=5, column=0, padx=5, pady=5, sticky="e")

occupation_entry = tk.Entry(
    input_frame,
    width=35
)
occupation_entry.grid(row=5, column=1, padx=5, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="Add Person",
    command=add_person,
    width=12
).grid(row=0, column=0, padx=5)


tk.Button(
    button_frame,
    text="Update",
    command=update_person,
    width=12
).grid(row=0, column=1, padx=5)


tk.Button(
    button_frame,
    text="Delete",
    command=delete_person,
    width=12
).grid(row=0, column=2, padx=5)


tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    width=12
).grid(row=0, column=3, padx=5)


table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill="both", expand=True)

tree = ttk.Treeview(
    table_frame,
    columns=(
        "ID",
        "Full Name",
        "Email",
        "Phone",
        "City",
        "Age",
        "Occupation"
    ),
    show="headings",
    height=12
)


tree.heading("ID", text="ID")
tree.heading("Full Name", text="Full Name")
tree.heading("Email", text="Email")
tree.heading("Phone", text="Phone")
tree.heading("City", text="City")
tree.heading("Age", text="Age")
tree.heading("Occupation", text="Occupation")


tree.column("ID", width=50)
tree.column("Full Name", width=150)
tree.column("Email", width=180)
tree.column("Phone", width=120)
tree.column("City", width=120)
tree.column("Age", width=60)
tree.column("Occupation", width=130)


tree.pack(fill="both", expand=True)

tree.bind("<ButtonRelease-1>", select_person)

display_persons()

root.mainloop()
conn.close()
