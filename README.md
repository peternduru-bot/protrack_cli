# ProTrack-CLI: Project Workspace Engine

ProTrack-CLI is a lightweight, terminal-based project management tool built to help software engineers break down massive, overwhelming applications into organized, manageable tasks. It acts as a smart digital checklist, automatically calculating real-time progress percentages and rendering active progress bars directly in the terminal console.

## 🚀 Features
* **Dynamic Progress Tracking:** Automatically calculates how close you are to completing a project based on completed tasks.
* **Local State Serialization:** Stores user and workspace data safely on local disk storage via a structured JSON schema.
* **Visual Dashboard Interface:** Uses rich-text table grids and functional tracking layout displays inside the command-line interface.
* **Automated Logic Validation:** Built-in verification architecture running on Pytest to guarantee app performance run-time safety.

---

## 📂 Project Architecture & Layout

```text
protrack_cli/
│
├── models.py         # Blueprint structures (User, Project, Task)
├── storage.py        # Local JSON database load and save engines
├── utils.py          # Helper functions and styling utilities
├── main.py           # Application routing and entry point
├── cli.py            # Terminal command argument handling
├── test_app.py       # Automated testing test suite
├── requirements.txt  # Python package dependencies
└── db.json           # Active local state database file
