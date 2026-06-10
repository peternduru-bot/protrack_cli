#!/usr/bin/env python3
"""
ProTrack-CLI: Pure Command-Line Project Management Tool.
Main execution entry point.
"""
import sys
from cli import run_cli

def main():
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\n[bold red]Process Terminated Safely.[/bold red] Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()