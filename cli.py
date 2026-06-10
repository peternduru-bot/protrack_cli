import argparse
import sys
from models import User, Project, Task
from storage import load_data, save_data
from utils import console, generate_id, display_dashboard, display_admin_diagnostics

def run_cli() -> None:
    """
    Parses live incoming command line parameters and executes real-time updates.
    Satisfies: Clean separation of interface layers and absolute zero mock structures.
    """
    parser = argparse.ArgumentParser(
        description="ProTrack-CLI: Production-Grade Project Management Tool.",
        epilog="Execute commands sequentially to seamlessly manage local workloads."
    )
    subparsers = parser.add_subparsers(dest="command", help="Operational workflows")

    # Command: init
    init_parser = subparsers.add_parser("init", help="Provision a clean workspace profile.")
    init_parser.add_argument("--name", required=True, help="Your official account profile name.")
    init_parser.add_argument("--email", required=True, help="Your official communication email.")
    init_parser.add_argument("--role", choices=["Standard", "Admin"], default="Standard", help="Account structural authorization.")

    # Command: dashboard
    subparsers.add_parser("dashboard", help="Render the live project tracking matrix.")

    # Command: admin-view
    subparsers.add_parser("admin-view", help="Render diagnostic system profiles (Admin authorization required).")

    # Command: add-project
    proj_parser = subparsers.add_parser("add-project", help="Append a project container to the workspace.")
    proj_parser.add_argument("--name", required=True, help="Title of the workspace container.")
    proj_parser.add_argument("--desc", default="", help="Narrative detailing project boundaries.")

    # Command: add-task
    task_parser = subparsers.add_parser("add-task", help="Append an executable checklist item to a project.")
    task_parser.add_argument("--project-id", required=True, help="Target project tracking identification code.")
    task_parser.add_argument("--name", required=True, help="Actionable description of the core assignment.")
    task_parser.add_argument("--desc", default="", help="Granular baseline expectations.")

    # Command: toggle-task
    toggle_parser = subparsers.add_parser("toggle-task", help="Invert the completion status of a target checklist item.")
    toggle_parser.add_argument("--project-id", required=True, help="Target project tracking identification code.")
    toggle_parser.add_argument("--task-id", required=True, help="Target task verification code.")

    # Execution Phase
    args = parser.parse_args()
    user = load_data()

    # Guard clause enforcing structural framework provision
    if args.command != "init" and user is None:
        console.print("[bold red]Workspace Missing:[/bold red] No live data found. Initialize your profile using:")
        console.print("  [cyan]python main.py init --name \"Your Name\" --email \"name@domain.com\"[/cyan]\n")
        sys.exit(0)

    if args.command == "init":
        if user is not None:
            console.print("[yellow]Alert: Active workspace profile detected. Initialization skipped to protect existing logs.[/yellow]\n")
            return
        new_user = User(generate_id(), args.name, args.email, args.role)
        if save_data(new_user):
            console.print(f"[bold green]Success![/bold green] Real workspace configured cleanly for [cyan]{args.name}[/cyan].")
            console.print("Type [yellow]python main.py dashboard[/yellow] to open your workspace console view.\n")

    elif args.command == "dashboard":
        display_dashboard(user)

    elif args.command == "admin-view":
        display_admin_diagnostics(user)

    elif args.command == "add-project":
        new_proj = Project(generate_id(), args.name, args.desc)
        user.add_project(new_proj)
        if save_data(user):
            console.print(f"[bold green]Success:[/bold green] Project '{args.name}' provisioned as ID: [cyan]{new_proj.id}[/cyan]\n")

    elif args.command == "add-task":
        target_project = next((p for p in user.projects if p.id == args.project_id), None)
        if not target_project:
            console.print(f"[bold red]Execution Error:[/bold red] Project target ID [yellow]{args.project_id}[/yellow] does not exist.\n")
            sys.exit(1)
        
        new_task = Task(generate_id(), args.name, args.desc)
        target_project.add_task(new_task)
        if save_data(user):
            console.print(f"[bold green]Success:[/bold green] Task safely linked. Task ID: [cyan]{new_task.id}[/cyan] inside Project: [yellow]{target_project.id}[/yellow]\n")

    elif args.command == "toggle-task":
        target_project = next((p for p in user.projects if p.id == args.project_id), None)
        if not target_project:
            console.print(f"[bold red]Execution Error:[/bold red] Project target ID [yellow]{args.project_id}[/yellow] does not exist.\n")
            sys.exit(1)
            
        target_task = next((t for t in target_project.tasks if t.id == args.task_id), None)
        if not target_task:
            console.print(f"[bold red]Execution Error:[/bold red] Task target ID [yellow]{args.task_id}[/yellow] does not exist inside this project container.\n")
            sys.exit(1)
            
        target_task.toggle_complete()
        if save_data(user):
            status_text = "[green]COMPLETED[/green]" if target_task.is_completed else "[yellow]PENDING[/yellow]"
            console.print(f"[bold green]Success:[/bold green] Task [cyan]{target_task.id}[/cyan] updated. Status is now {status_text}.\n")
            console.print(f"[bold cyan]Project Progress Update:[/bold cyan] {target_project.name} is now at [magenta]{target_project.progress}%[/magenta]\n")

    else:
        parser.print_help()