import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONTACT_FILE = "contacts.json"

# Load contacts
def load_contacts():
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, "r") as f:
            return json.load(f)
    return []

# Save contacts
def save_contacts():
    with open(CONTACT_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

# Add contact
def add_contact():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    
    if not name or not phone or not email:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    
    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts()
    update_contact_list()
    clear_fields()

# Update contact
def update_contact():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Contact", "Please select a contact to update.")
        return
    index = int(selected[0])
    contacts[index] = {
        "name": entry_name.get().strip(),
        "phone": entry_phone.get().strip(),
        "email": entry_email.get().strip()
    }
    save_contacts()
    update_contact_list()
    clear_fields()

# Delete contact
def delete_contact():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Contact", "Please select a contact to delete.")
        return
    index = int(selected[0])
    del contacts[index]
    save_contacts()
    update_contact_list()
    clear_fields()

# Display contacts in list
def update_contact_list():
    tree.delete(*tree.get_children())
    for i, contact in enumerate(contacts):
        tree.insert("", "end", iid=i, values=(contact["name"], contact["phone"], contact["email"]))

# Load selected contact
def on_select(event):
    selected = tree.selection()
    if selected:
        index = int(selected[0])
        entry_name.delete(0, tk.END)
        entry_name.insert(0, contacts[index]["name"])
        entry_phone.delete(0, tk.END)
        entry_phone.insert(0, contacts[index]["phone"])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, contacts[index]["email"])

# Clear input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# -------------------------------
# GUI Code
# -------------------------------

contacts = load_contacts()

root = tk.Tk()
root.title("Contact Manager")
root.geometry("600x400")
root.config(bg="#f0f0f0")

# Input Fields
frame_input = tk.Frame(root, bg="#f0f0f0")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Name:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_input, width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Phone:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
entry_phone = tk.Entry(frame_input, width=30)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Email:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_input, width=30)
entry_email.grid(row=2, column=1, padx=5, pady=5)

# Buttons
frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Add", width=10, bg="#4CAF50", fg="white", command=add_contact).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Update", width=10, bg="#2196F3", fg="white", command=update_contact).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Delete", width=10, bg="#f44336", fg="white", command=delete_contact).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Clear", width=10, command=clear_fields).grid(row=0, column=3, padx=5)

# Treeview to display contacts
tree = ttk.Treeview(root, columns=("Name", "Phone", "Email"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree.bind("<<TreeviewSelect>>", on_select)

update_contact_list()

root.mainloop()
