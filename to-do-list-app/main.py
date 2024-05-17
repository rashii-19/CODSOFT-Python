import tkinter as tk
from tkinter import messagebox

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        self.tasks = []

        self.task_var = tk.StringVar()

        self.create_widgets()

        # Load tasks from file when the app starts
        self.load_tasks()

        # Bind Enter key to add_task function
        self.root.bind("<Return>", self.add_task)

        # Automatically save tasks when modified
        self.root.bind("<FocusOut>", self.save_tasks)

    def create_widgets(self):
        # Entry widget to add tasks
        self.entry = tk.Entry(self.root, textvariable=self.task_var, width=40)
        self.entry.pack(pady=10)

        # Add task button
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=40, height=10)
        self.task_listbox.pack(pady=10)

        # Update and Delete buttons
        self.update_button = tk.Button(self.root, text="Update Task", command=self.update_task)
        self.update_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.RIGHT, padx=10)

    def add_task(self, event=None):
        task = self.task_var.get()
        if task:
            self.tasks.append(task)
            self.update_task_listbox()
            self.task_var.set("")
            self.save_tasks()  # Save tasks after adding
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(self, event=None):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
            self.save_tasks()  # Save tasks after deletion
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def update_task(self, event=None):
        try:
            selected_index = self.task_listbox.curselection()[0]
            new_task = self.task_var.get()
            if new_task:
                self.tasks[selected_index] = new_task
                self.update_task_listbox()
                self.task_var.set("")
                self.save_tasks()  # Save tasks after update
            else:
                messagebox.showwarning("Warning", "You must enter a new task.")
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to update.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def save_tasks(self, event=None):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = [line.strip() for line in file.readlines()]
                self.update_task_listbox()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No tasks file found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
