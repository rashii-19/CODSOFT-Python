import tkinter as tk
from tkinter import messagebox
import json
import re


class ContactBookApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Contact Book")

        self.contacts = {}
        self.load_contacts()

        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self.master, text="Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.phone_label = tk.Label(self.master, text="Phone:")
        self.phone_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.phone_entry = tk.Entry(self.master)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        self.email_label = tk.Label(self.master, text="Email:")
        self.email_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.email_entry = tk.Entry(self.master)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        self.address_label = tk.Label(self.master, text="Address:")
        self.address_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.address_entry = tk.Entry(self.master)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.master, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=4, columnspan=2, padx=5, pady=5)

        self.view_button = tk.Button(self.master, text="View Contacts", command=self.view_contacts)
        self.view_button.grid(row=5, columnspan=2, padx=5, pady=5)

        self.search_label = tk.Label(self.master, text="Search:")
        self.search_label.grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_entry = tk.Entry(self.master)
        self.search_entry.grid(row=6, column=1, padx=5, pady=5)

        self.search_button = tk.Button(self.master, text="Search", command=self.search_contact)
        self.search_button.grid(row=7, columnspan=2, padx=5, pady=5)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone and self.validate_phone(phone) and email and self.validate_email(email):
            self.contacts[name] = {'Phone': phone, 'Email': email, 'Address': address}
            self.save_contacts()
            messagebox.showinfo("Success", "Contact added successfully!")
            self.clear_entries()
        elif not name:
            messagebox.showerror("Error", "Name field is required!")
        elif not phone or not self.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number! It should contain 10 digits.")
        elif not email or not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format! It should be in the format 'example@gmail.com'.")

    def view_contacts(self):
        if self.contacts:
            contact_list = "Contacts:\n"
            for name, details in self.contacts.items():
                contact_list += f"Name: {name}\nPhone: {details['Phone']}\nEmail: {details['Email']}\nAddress: {details['Address']}\n\n"
            messagebox.showinfo("Contacts", contact_list)
        else:
            messagebox.showinfo("Contacts", "No contacts found!")

    def search_contact(self):
        search_term = self.search_entry.get()
        if search_term:
            results = [name for name in self.contacts.keys() if search_term.lower() in name.lower()]
            if results:
                result_string = "Search results:\n"
                for name in results:
                    details = self.contacts[name]
                    result_string += f"Name: {name}\nPhone: {details['Phone']}\nEmail: {details['Email']}\nAddress: {details['Address']}\n\n"
                messagebox.showinfo("Search Results", result_string)
            else:
                messagebox.showinfo("Search Results", "No matching contacts found!")
        else:
            messagebox.showerror("Error", "Please enter a search term!")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def validate_phone(self, phone):
        return bool(re.match(r'^\d{10}$', phone))

    def validate_email(self, email):
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email))

    def save_contacts(self):
        with open("contacts.json", "w") as file:
            json.dump(self.contacts, file)

    def load_contacts(self):
        try:
            with open("contacts.json", "r") as file:
                self.contacts = json.load(file)
        except FileNotFoundError:
            self.contacts = {}


def main():
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
