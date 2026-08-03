import sys
import uuid
import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

from mentor.database import engine, Base
from mentor.database.init_db import init_db as db_initializer
from mentor.database import Sessions, Progresstable
from sqlalchemy.orm import Session
from sqlalchemy import select

from mentor.agent import run_agent_turn
from mentor.workspace import list_project_files, is_safe_workspace_path
from mentor.prompt import create_review_prompt, create_agent_system_prompt
from mentor.services import session_service, message_service, progress_service

app = typer.Typer(
    name="ai-mentor",
    help="AI Learning Mentor — Stack-Agnostic Senior Staff Engineering Coach",
    add_completion=False,
)
console = Console()


@app.command("init-db")
def init_db(
    force: bool = typer.Option(False, "--force", "-f", help="Re-initialize database tables")
):
    """Initialize PostgreSQL database tables for AI Mentor."""
    console.print(Panel("[bold green]Initializing PostgreSQL Database Tables...[/bold green]", title="AI Mentor DB"))
    try:
        db_initializer(force=force)
        console.print("[bold green]✓ Database tables successfully initialized![/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Failed to initialize database: {e}[/bold red]")


@app.command("progress")
def show_progress():
    """Display learning progress and completed milestones."""
    with Session(engine) as db:
        milestones = db.scalars(select(Progresstable).order_by(Progresstable.milestone_order)).all()

        if not milestones:
            console.print(Panel("[yellow]No milestones recorded yet. Start a session to create learning milestones![/yellow]", title="Progress"))
            return

        table = Table(title="📊 AI Mentor Learning Milestones", show_header=True, header_style="bold magenta")
        table.add_column("Order", style="dim", width=6)
        table.add_column("Milestone Name", style="bold cyan")
        table.add_column("Status", justify="center")

        for m in milestones:
            status_str = "[bold green]✓ Completed[/bold green]" if m.status == "completed" else "[bold yellow]In Progress[/bold yellow]"
            table.add_row(str(m.milestone_order), m.milestone_name, status_str)

        console.print(table)


@app.command("review")
def review_file(
    file_path: str = typer.Argument(None, help="Optional relative path to file. If omitted, reviews all workspace files.")
):
    """Perform a production-grade AI code review on workspace files."""
    files = list_project_files()
    if not files:
        console.print("[yellow]Workspace is empty. No files to review yet![/yellow]")
        return

    if file_path:
        is_safe, target_path = is_safe_workspace_path(file_path)
        if not is_safe or not target_path.exists():
            console.print(f"[bold red]❌ Error: File '{file_path}' does not exist inside workspace.[/bold red]")
            return
        content = target_path.read_text(encoding="utf-8")
        console.print(Panel(f"[bold blue]Conducting Production Review for '{file_path}'...[/bold blue]", title="AI Code Review"))
        prompt = create_review_prompt(file_path, content)
    else:
        console.print(Panel(f"[bold blue]Conducting Full Workspace Production Review across {len(files)} file(s)...[/bold blue]", title="AI Project Review"))
        combined_sources = []
        for f in files:
            _, p = is_safe_workspace_path(f)
            combined_sources.append(f"--- File: {f} ---\n" + p.read_text(encoding="utf-8"))
        prompt = create_review_prompt("Full Project Workspace", "\n\n".join(combined_sources))

    session_id = f"review-{uuid.uuid4().hex[:8]}"
    session_service.create_session_if_not_exists(session_id, "workspace")

    with console.status("[bold green]Senior Staff Engineer is reviewing your code...[/bold green]"):
        try:
            review_text = run_agent_turn(session_id, prompt)
            console.print(Markdown(review_text))
        except Exception as e:
            console.print(f"[bold red]❌ Review failed: {e}[/bold red]")


@app.command("start")
def start_session(
    session_id: str = typer.Option(None, "--session", "-s", help="Specific session ID to load"),
    new_session: bool = typer.Option(False, "--new", "-n", help="Start a brand new session instead of resuming")
):
    """Start an interactive, continuous engineering coaching session with persistent memory."""
    with Session(engine) as db:
        if new_session or (not session_id):
            if not new_session:
                last_session = db.scalar(select(Sessions.session_id).order_by(Sessions.session_id.desc()))
                if last_session:
                    session_id = last_session

            if not session_id or new_session:
                session_id = f"session-{uuid.uuid4().hex[:8]}"

    session_service.create_session_if_not_exists(session_id, "workspace")
    history_msgs = message_service.load_messages(session_id)
    history_count = len(history_msgs)

    status_msg = f"Resumed session '{session_id}' ({history_count} previous message(s) loaded)." if history_count > 0 else f"Started new session '{session_id}'."

    console.print(
        Panel(
            f"[bold cyan]Welcome to AI Learning Mentor![/bold cyan]\n\n"
            f"[bold green]✓ {status_msg}[/bold green]\n"
            "I am your Senior Staff Engineering Coach. Let's continue building!\n"
            "[dim]In-Session Commands: /progress, /review [file], /files, /help, /exit[/dim]",
            title="🚀 Interactive Mentoring Session",
            border_style="cyan",
        )
    )

    while True:
        try:
            user_input = console.input("\n[bold green]👤 You > [/bold green]").strip()
            if not user_input:
                continue

            if user_input.lower() in ["/exit", "exit", "quit", "/quit"]:
                console.print("[yellow]Ending session. Keep building and learning![/yellow]")
                break

            elif user_input.lower() == "/progress":
                show_progress()
                continue

            elif user_input.lower() == "/files":
                files = list_project_files()
                console.print(Panel("\n".join([f"• {f}" for f in files]) if files else "(Workspace is empty)", title="📁 Workspace Files"))
                continue

            elif user_input.lower().startswith("/review"):
                parts = user_input.split(maxsplit=1)
                target = parts[1] if len(parts) > 1 else None
                review_file(target)
                continue

            elif user_input.lower() == "/help":
                console.print(
                    "[bold yellow]In-Session Slash Commands:[/bold yellow]\n"
                    "  • [cyan]/progress[/cyan] - View current milestone progress table\n"
                    "  • [cyan]/review [file][/cyan] - Code review (omit file to review entire workspace)\n"
                    "  • [cyan]/files[/cyan] - List active files in workspace\n"
                    "  • [cyan]/exit[/cyan] - End the mentoring session\n"
                )
                continue

            with console.status("[bold cyan]Senior Staff Engineer is thinking & inspecting workspace...[/bold cyan]"):
                response_text = run_agent_turn(session_id, user_input)

            console.print("\n[bold magenta]🤖 Mentor > [/bold magenta]")
            console.print(Markdown(response_text))

        except KeyboardInterrupt:
            console.print("\n[yellow]Session interrupted. Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]❌ Error: {e}[/bold red]")


if __name__ == "__main__":
    app()
