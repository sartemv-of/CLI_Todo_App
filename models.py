from enum import Enum
from datetime import datetime
from typing import Optional

class TaskStatus(Enum):
    TODO = "New"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class TaskPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Task:
    def __init__(self, task_id: int, title: str, description: str = "",
        status: TaskStatus = TaskStatus.TODO, priority: TaskPriority = TaskPriority.MEDIUM):
        if not title or title.isspace():
            raise ValueError("Название задачи не может быть пустым.")

        self.id: int = task_id
        self.title: str = title.strip()
        self.description: str = description
        self.status: TaskStatus = status
        self.priority: TaskPriority = priority
        self.created_at: datetime = datetime.now()
        self.updated_at: Optional[datetime] = None

    def complete(self) -> None:
        self.status = TaskStatus.DONE
        self.updated_at = datetime.now()

    def in_progress(self) -> None:
        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title!r}, status={self.status.name}, priority={self.priority.name})"

    def __str__(self) -> str:
        marker = "🟢" if self.status == TaskStatus.DONE else "🟡" if self.status == TaskStatus.IN_PROGRESS else "🔴"
        prio_stars = "⭐" if self.priority == TaskPriority.LOW else "⭐⭐" if self.priority == TaskPriority.MEDIUM else "⭐⭐⭐"
        updated_str = f" (изменено: {self.updated_at.strftime('%H:%M:%S')})" if self.updated_at else ""
        return f"{marker} [{self.id}] {self.title} | Приоритет: {prio_stars} ({self.status.value}){updated_str}"
