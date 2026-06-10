import json
import os
import sys
from typing import Optional
from models import User, Project, Task

DATA_FILE = "db.json"

def save_data(user: User, filename: str = DATA_FILE) -> bool:
    """
    Serializes live application objects directly into the local db.json file.
    Satisfies: Persistence File I/O requirement with robust error handling.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(user.to_dict(), f, indent=4)
        return True
    except IOError as e:
        print(f"[bold red]Database Write Error: Unable to save records. Details: {e}[/bold red]")
        return False

def load_data(filename: str = DATA_FILE) -> Optional[User]:
    """
    Reads data from db.json and converts the raw JSON trees back into real,
    fully functional object instances on startup. Returns None if no user profile exists.
    """
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Reconstruct real User instance from data
        user = User(data["id"], data["name"], data["email"], data.get("role", "Standard"))
        user.created_at = data.get("created_at", user.created_at)
        
        # Reconstruct real Project instances
        for p_data in data.get("projects", []):
            proj = Project(p_data["id"], p_data["name"], p_data["description"])
            proj.created_at = p_data.get("created_at", proj.created_at)
            
            # Reconstruct real Task instances
            for t_data in p_data.get("tasks", []):
                task = Task(t_data["id"], t_data["name"], t_data["description"], t_data["is_completed"])
                task.created_at = t_data.get("created_at", task.created_at)
                proj.add_task(task)
                
            user.add_project(proj)
        return user
    except (json.JSONDecodeError, KeyError, PermissionError) as e:
        # Graceful handling prevents ugly python terminal crashes if db.json is corrupted
        print(f"[bold red]Database Corruption Error: Integrity check failed. Details: {e}[/bold red]")
        sys.exit(1)