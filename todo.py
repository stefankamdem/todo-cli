import json
from rich.console import Console
from rich.table import Table
from pathlib import Path

console = Console()
DATA_FILE = Path("task.json")

def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []

def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=2))

def list_tasks():
    tasks = load_tasks()
    table = Table(title="To-Do List")
    table.add_column("ID", justify="right")
    table.add_column("Task")
    table.add_column("Status")

    for i, t in enumerate(tasks, 1):
        table.add_row(str(i), t["task"],"✅" if t["done"] else "❌")
    console.print(table)

def add_task(task):
    tasks = load_tasks()
    tasks.append({"task": task, "done": False})
    save_tasks(tasks)
    console.print(f"[green] Added:[/green] {task}")

def delete_task(task_id):
    tasks = load_tasks()
    if 0 < task_id <= len(tasks):
        removed = tasks.pop(task_id-1)
        save_tasks(tasks)
        console.print(f"[red]Deleted:[/red] {removed['task']}")
    else:
        console.print("[yellow]Invalid task ID[/yellow]")

def clear_tasks():
    confirm = input("Are you sure you want to delete ALL tasks? (y/n): ")
    if confirm.lower() == "y":
        save_tasks([])
        console.print("[red]All tasks cleared![/red]")
    else:
        console.print("[green]Cancelled[/green]")

def complete_task(task_id):
    tasks = load_tasks()
    if 0 < task_id <= len(tasks):
        tasks[task_id-1]["done"] = True
        save_tasks(tasks)
        console.print(f"[blue]Complete:[/blue] {tasks[task_id-1]['task']}")

if __name__ == "__main__":
    console.print("[bold]Simple To-Do CLI[/bold]")
    console.print("1. List tasks\n2. Add task\n3. Complete task\n4. Delete task\n5. Clear all tasks\n6. Exit")

    choice = input("Choose: ")
    if choice == "1":
        list_tasks()
    elif choice == "2":
        add_task(input("Task: "))
    elif choice == "3":
        complete_task(int(input("Task ID: ")))
    elif choice == "4":
        delete_task(int(input("Task ID to delete: ")))
    elif choice == "5":
        clear_tasks()
    else:
        console.print("[yellow]Goodbye![/yellow]")