import os
import json
import pytest
from models import User, Project, Task
from storage import save_data, load_data

TEST_DB = "test_db.json"

@pytest.fixture(autouse=True)
def cleanup():
    """Ensures a clean testing environment before and after running tests."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_object_relations_and_progress():
    """Verifies object hierarchy and dynamic mathematical progress calculations."""
    user = User("u1", "PJ", "pj@test.com")
    project = Project("p1", "MediConnect", "Backend Setup")
    
    task1 = Task("t1", "Setup DB")
    task2 = Task("t2", "Configure Auth")
    
    project.add_task(task1)
    project.add_task(task2)
    user.add_project(project)
    
    assert len(user.projects) == 1
    assert len(project.tasks) == 2
    assert project.progress == 0.0
    
    # Toggle one task and test dynamic progress recalculation
    task1.toggle_complete()
    assert project.progress == 50.0

def test_file_persistence():
    """Verifies real file system serialization and data integrity checks."""
    user = User("u1", "PJ Nduru", "peter.nduru@student.moringaschool.com", "Admin")
    project = Project("p1", "ProTrack-CLI")
    user.add_project(project)
    
    # Write to local disk
    save_success = save_data(user, filename=TEST_DB)
    assert save_success is True
    assert os.path.exists(TEST_DB)
    
    # Read back from local disk and verify structural matching
    loaded_user = load_data(filename=TEST_DB)
    assert loaded_user is not None
    assert loaded_user.name == "PJ Nduru"
    assert loaded_user.role == "Admin"
    assert len(loaded_user.projects) == 1