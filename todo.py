import json
from rich.console import Console
from rich.table import Table
from pathlib import Path

#Rich console object for styled printing
console = Console()
#"task.json" is the file where tasks will be stored
DATA_FILE = Path("task.json")

# Returns all the tasks in the JSON file, and if there are no tasks an emty list will be returned
def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []

# Saves the tasks in the JSON file
def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=2))

# Displays all the tasks in a table
def list_tasks():
    tasks = load_tasks()

    # Creates a table with three columns (ID, Task, Status)
    table = Table(title="To-Do List")
    table.add_column("ID", justify="right")
    table.add_column("Task")
    table.add_column("Status")

    # Adds rows to the table for each task
    for i, t in enumerate(tasks, 1):
        table.add_row(str(i), t["task"],"✅" if t["done"] else "❌")
    console.print(table)


#Adds a task to the JSON file
def add_task(task):
    tasks = load_tasks()
    tasks.append({"task": task, "done": False}) # Assigns the tasks its name and the done value to False
    save_tasks(tasks)#Saves tasks in the JSON file
    console.print(f"[green] Added:[/green] {task}") # Notifies that the task is added

# Deltes the chosen task
def delete_task(task_id):
    tasks = load_tasks() 
    if 0 < task_id <= len(tasks): # Makes sure that a valid ID is chosen (from 1 to the numebr of tasks)
        removed = tasks.pop(task_id-1) # Removes the task from the JSON file
        save_tasks(tasks) # Saves the tasks after the removal in the JSON file
        console.print(f"[red]Deleted:[/red] {removed['task']}") # Notifies that the the task was removed
    else:
        console.print("[yellow]Invalid task ID[/yellow]") # Displays if an invalid ID is chosen

def clear_tasks():
    confirm = input("Are you sure you want to delete ALL tasks? (y/n): ")
    if confirm.lower() == "y":
        save_tasks([])
        console.print("[red]All tasks cleared![/red]")
    else:
        console.print("[green]Cancelled[/green]")

# Marks the chosen task as completed
def complete_task(task_id):
    tasks = load_tasks()
    if 0 < task_id <= len(tasks): # Makes sure that a valid ID is chosen (from 1 to the numebr of tasks)
        tasks[task_id-1]["done"] = True # Changes the task's "done" value to True
        save_tasks(tasks) # Saves the task in the JSON file
        console.print(f"[blue]Complete:[/blue] {tasks[task_id-1]['task']}") # Notifies that the task is completed

if __name__ == "__main__":
    # Prints the menu
    while True:
        console.print("[bold]Simple To-Do CLI[/bold]")
        console.print(
            "1. List tasks\n"
            "2. Add task\n"
            "3. Complete task\n"
            "4. Delete task\n"
            "5. Clear all tasks\n"
            "6. Exit"
        )

        choice = input("Choose: ")

        #Handles the user's choice
        if choice == "1":
            list_tasks()
        elif choice == "2":
            add_task(input("Task: ").strip())
        elif choice == "3":
            try:
                complete_task(int(input("Task ID: ").strip()))
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
        elif choice == "4":
            try:
                delete_task(int(input("Task ID to delete: ").strip()))
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
        elif choice == "5":
            clear_tasks()
        elif choice == "6":
            console.print("[yellow]Goodbye![/yellow]")
            break
        else:
            console.print("[red]Invalid choice, please try again.[/red]")