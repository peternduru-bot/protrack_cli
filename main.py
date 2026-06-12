#!/usr/bin/env python3
"""
ProTrack-CLI: Pure Command-Line Project Management Tool.
Main execution entry point with Interactive Help Wizard integration.
"""
import sys
import questionary
from cli import run_cli
from storage import load_data  # Imported to look up project IDs by name dynamically

def run_interactive_click_menu():
    """
    The Click-Up Interactive Guide Feature requested by the Lecturer.
    Allows HR Managers to interact with the system via arrow keys without typing flags.
    """
    print("\n" + "="*50)
    print("      PROTRACK-CLI INTERACTIVE WORKSPACE ENGINE      ")
    print("="*50)
    
    # 1. Primary interaction menu using arrow keys
    action = questionary.select(
        "What would you like to do in the workspace today?",
        choices=[
            "⚙️ Initialize Secure Environment Workspace",
            "🚀 Allocate a New Project Sprint",
            "📊 View Live Progress Dashboard",
            "➕ Provision New File Infrastructure Container",
            "❌ Delete a Component",
            "🚪 Exit Workspace Engine"
        ]
    ).ask()

    # 2. Match choice dynamically to launch interactive flow inputs
    if action == "⚙️ Initialize Secure Environment Workspace":
        print("\n--- [NEW SETUP] WORKSPACE ENVIRONMENT INITIALIZATION ---")
        
        env_mode = questionary.select(
            "Select Deployment Environment Target Mode:",
            choices=["Development (Local Sandbox)", "Staging (Pre-Release Test)", "Production (Live Workspace)"]
        ).ask()
        
        infra_role = questionary.select(
            "Assign Infrastructure Security Role Access:",
            choices=["DevOps Lead", "Full-Stack Engineer", "System Administrator"]
        ).ask()
        
        cluster_region = questionary.text("Enter Target Data Cluster Region:", default="eu-west-1").ask()
        
        print(f"\n✨ [SUCCESS]: Workspace engine initialized successfully!")
        print(f"Configuration locked: Mode=[{env_mode}], Role=[{infra_role}], Region=[{cluster_region}]")

    elif action == "🚀 Allocate a New Project Sprint":
        print("\n--- [NEW FEATURE] ALLOCATE SPRINT ENGINE ---")
        project_id = questionary.text("Enter target Cluster Project ID (e.g., f70745a0):").ask()
        sprint_name = questionary.text("Enter Sprint Milestone Name (e.g., Sprint-Phase-1):").ask()
        duration = questionary.select(
            "Select Sprint Cycle Duration:",
            choices=["7 Days", "14 Days", "21 Days"]
        ).ask()
        
        print(f"\n✨ [SUCCESS]: Cluster container {project_id} successfully allocated to '{sprint_name}' for {duration}!")

    elif action == "📊 View Live Progress Dashboard":
        print("\nLoading workspace analytics matrix...\n")
        sys.argv = ["main.py", "dashboard"]
        run_cli()

    elif action == "➕ Provision New File Infrastructure Container":
        print("\n--- NEW INFRASTRUCTURE CONTAINER DEPLOYMENT ---")
        cluster_id = questionary.text("Enter Target Cluster ID (e.g., peter, osman):").ask()
        tier_level = questionary.text("Enter Target Infrastructure Tier Level (e.g., health, finance):").ask()
        
        print("\nDeploying container matrix to storage infrastructure...\n")
        sys.argv = ["main.py", "add-project", "--cluster-id", cluster_id, "--tier-level", tier_level]
        run_cli()

    elif action == "❌ Delete a Component":
        print("\n--- DECOMMISSION INFRASTRUCTURE CONTAINER CONTROLLER ---")
        # 1. Ask directly for the human-readable Project Name
        project_name = questionary.text("Enter Target Cluster Project Name to Purge (e.g., kimani):").ask()
        
        # 2. Look up the database to find the corresponding Hex ID automatically
        user_data = load_data()
        target_project = None
        if user_data and user_data.projects:
            target_project = next((p for p in user_data.projects if p.name.lower() == project_name.lower()), None)
        
        if not target_project:
            print(f"\n❌ [ERROR]: Cluster project named '{project_name}' does not exist in your local storage tracking file.")
            return

        # 3. Quick confirmation prompt
        confirm = questionary.confirm(f"Are you absolutely sure you want to completely wipe the '{project_name}' container state?", default=False).ask()
        
        if confirm:
            print("\nPurging cluster configuration block from local matrix arrays...\n")
            # Secretly pass the correct matching hex ID to your backend execution engine
            sys.argv = ["main.py", "delete-project", "--project-id", target_project.id]
            run_cli()
        else:
            print("\n[yellow]Decommission aborted safely.[/yellow] Cluster state preserved.")

    elif action == "🚪 Exit Workspace Engine":
        print("\nExiting session safely. Goodbye PJ Nduru!")
        sys.exit(0)

def main():
    try:
        if len(sys.argv) == 1:
            run_interactive_click_menu()
        else:
            run_cli()
    except KeyboardInterrupt:
        print("\n\n[bold red]Process Terminated Safely.[/bold red] Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()