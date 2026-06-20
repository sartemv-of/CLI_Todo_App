import json
from pathlib import Path
from typing import Any
from models import Task, TaskStatus, TaskPriority, datetime

class TaskManager:
    def __init__(self, storage_path: str | Path = "tasks.json"):
        self.storage_path = Path(storage_path)
        self.tasks: list[Task] = []
        self.load_tasks()

    def add_task(self, title: str, description: str = "", priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        next_id = self.tasks[-1].id + 1 if self.tasks else 1
        new_task = Task(task_id=next_id, title=title, description=description, priority=priority)
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def _task_to_dict(self, task: Task) -> dict[str, Any]:
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status.name,
            "priority": task.priority.name,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }

    def _dict_to_task(self, data: dict[str, Any]) -> Task:
        task = Task(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            status=TaskStatus[data["status"]],
            priority=TaskPriority[data["priority"]]
        )
        task.created_at = datetime.fromisoformat(data["created_at"])
        if data["updated_at"]:
            task.updated_at = datetime.fromisoformat(data["updated_at"])
        return task

    def save_tasks(self) -> None:
        tasks_data = [self._task_to_dict(task) for task in self.tasks]
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, indent=4, ensure_ascii=False)

    def load_tasks(self) -> None:
        if not self.storage_path.exists():
            self.tasks = []
            return

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self.tasks = [self._dict_to_task(item) for item in raw_data]
        except (json.JSONDecodeError, ValueError):
            self.tasks = []

    def get_all_tasks(self) -> list[Task]:
        return self.tasks

    def remove_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return True
        return False
