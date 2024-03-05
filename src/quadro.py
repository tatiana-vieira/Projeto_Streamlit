import tkinter as tk

class Task:
    def __init__(self, description, status):
        self.description = description
        self.status = status

class KanbanBoard(tk.Tk):
    def __init__(self, tasks):
        super().__init__()

        self.tasks = tasks

        self.title("Kanban Board")

        self.columns = ["To Do", "Doing", "Done"]

        self.lists = {}

        for col in self.columns:
            self.lists[col] = tk.Listbox(self, selectmode=tk.SINGLE)
            self.lists[col].bind("<<ListboxSelect>>", self.on_select)
            self.lists[col].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for task in self.tasks:
            self.lists[task.status].insert(tk.END, task.description)

    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
            task_index = selection[0]
            task = self.tasks[task_index]
            print(f"Selected task: {task.description}, Status: {task.status}")

if __name__ == "__main__":
    tasks = [
        Task("Task 1", "To Do"),
        Task("Task 2", "Doing"),
        Task("Task 3", "Done")
    ]

    app = KanbanBoard(tasks)
    app.mainloop()
