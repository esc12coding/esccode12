import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

TASKS_LOCATION = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_LOCATION):
        with open(TASKS_LOCATION, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASKS_LOCATION, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(tasks, description, due_date, due_time):
    tasks.append({"description": description, "due_date": due_date, "due_time": due_time, "completed": False, "notified": False})
    save_tasks(tasks)
    update_task_list()

def update_task_list():
    task_list.delete(0, tk.END)
    for task in tasks:
        status = "✔" if task["completed"] else "✘"
        task_list.insert(tk.END, f"{task['description']} - Due: {task['due_date']} {task['due_time']} - {status}")

def on_add_task():
    description = simpledialog.askstring("Task Description", "Enter task description:")
    if description is None:
        return
    due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
    if due_date is None:
        return
    try:
        datetime.strptime(due_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
        return
    due_time = simpledialog.askstring("Due Time", "Enter due time (HH:MM):")
    if due_time is None:
        return
    try:
        datetime.strptime(due_time, '%H:%M')
    except ValueError:
        messagebox.showerror("Invalid Time", "Please enter a valid time in HH:MM format.")
        return
    add_task(tasks, description, due_date, due_time)

def mark_task_completed():
    selected_index = task_list.curselection()
    if not selected_index:
        messagebox.showwarning("Select Task", "Please select a task to mark as completed.")
        return
    tasks[selected_index[0]]["completed"] = True
    save_tasks(tasks)
    update_task_list()

def delete_task():
    selected_index = task_list.curselection()
    if not selected_index:
        messagebox.showwarning("Select Task", "Please select a task to delete.")
        return
    tasks.pop(selected_index[0])
    save_tasks(tasks)
    update_task_list()

def check_alarms():
    current_time = datetime.now()
    for task in tasks:
        if not task["completed"] and not task["notified"]:
            task_due = datetime.strptime(task["due_date"] + " " + task["due_time"], "%Y-%m-%d %H:%M")
            if current_time >= task_due:
                messagebox.showinfo("Task Due", f"The task '{task['description']}' is due now!")
                task["notified"] = True
                save_tasks(tasks)
                update_task_list()
    app.after(60000, check_alarms)  

app = tk.Tk()
app.title("Task Manager")

tasks = load_tasks()

frame = tk.Frame(app)
frame.pack(pady=10)

task_list = tk.Listbox(frame, width=50, height=10)
task_list.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

task_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_list.yview)

button_frame = tk.Frame(app)
button_frame.pack(pady=10)

add_task_button = tk.Button(button_frame, text="Add Task", command=on_add_task)
add_task_button.grid(row=0, column=0, padx=5)

mark_completed_button = tk.Button(button_frame, text="Mark Completed", command=mark_task_completed)
mark_completed_button.grid(row=0, column=1, padx=5)

delete_task_button = tk.Button(button_frame, text="Delete Task", command=delete_task)
delete_task_button.grid(row=0, column=2, padx=5)

update_task_list()

check_alarms()

app.mainloop()