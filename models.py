from datetime import datetime
from typing import List, Dict, Any

class BaseModel:
    """
    Abstract baseline class providing unique IDs and timestamps.
    Satisfies: OOP Inheritance requirement.
    """
    def __init__(self, id_str: str, name: str):
        self._id = id_str        # Protected attribute for encapsulation
        self.name = name
        self.created_at = datetime.now().isoformat()

    @property
    def id(self) -> str:
        """Getter for the protected ID variable."""
        return self._id


class Task(BaseModel):
    """
    Encapsulates a single actionable checklist item.
    """
    def __init__(self, task_id: str, name: str, description: str = "", is_completed: bool = False):
        super().__init__(task_id, name)
        self.description = description
        self.is_completed = is_completed

    def toggle_complete(self) -> None:
        """Inverts the completion status of the task."""
        self.is_completed = not self.is_completed

    def to_dict(self) -> Dict[str, Any]:
        """Converts object data into a standard dictionary for storage."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_completed": self.is_completed,
            "created_at": self.created_at
        }


class Project(BaseModel):
    """
    Manages a collection of tasks and calculates project progress dynamically.
    """
    def __init__(self, project_id: str, name: str, description: str = ""):
        super().__init__(project_id, name)
        self.description = description
        self._tasks: List[Task] = []  # Encapsulated task list

    @property
    def tasks(self) -> List[Task]:
        return self._tasks

    @property
    def progress(self) -> float:
        """
        Calculates project completion percentage dynamically.
        Satisfies: Dynamic calculation behavior.
        """
        if not self._tasks:
            return 0.0
        completed = sum(1 for t in self._tasks if t.is_completed)
        return round((completed / len(self._tasks)) * 100, 1)

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "tasks": [t.to_dict() for t in self._tasks]
        }


class User(BaseModel):
    """
    Top-level user profile managing multiple separate projects.
    """
    def __init__(self, user_id: str, name: str, email: str, role: str = "Standard"):
        super().__init__(user_id, name)
        self.email = email
        self.role = role
        self._projects: List[Project] = []  # Encapsulated project list

    @property
    def projects(self) -> List[Project]:
        return self._projects

    def add_project(self, project: Project) -> None:
        self._projects.append(project)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "projects": [p.to_dict() for p in self._projects]
        }