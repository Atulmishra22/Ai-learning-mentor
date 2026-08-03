import os
from pathlib import Path

def get_workspace_dir() -> Path:
    """
    Returns the absolute Path for the single active workspace/ directory.
    Creates the directory if it does not already exist.
    """
    workspace_dir = (Path.cwd() / "workspace").resolve()
    workspace_dir.mkdir(parents=True, exist_ok=True)
    return workspace_dir


def is_safe_workspace_path(relative_path: str) -> tuple[bool, Path]:
    """
    Validates if relative_path is safely contained within workspace/.
    Returns (is_safe, resolved_target_path).
    """
    base_dir = get_workspace_dir()
    target_path = (base_dir / relative_path).resolve()

    # Sandboxing check to prevent path traversal (../)
    try:
        is_safe = target_path.is_relative_to(base_dir)
        return is_safe, target_path
    except (ValueError, Exception):
        return False, target_path


def list_project_files() -> list[str]:
    """
    Returns a list of relative file paths for all non-ignored files
    inside workspace/. Safely handles OS permission errors and symlinks.
    """
    base_dir = get_workspace_dir()
    ignored_dirs = {".git", "__pycache__", ".venv", ".pytest_cache", "node_modules"}

    file_list = []
    try:
        for path in base_dir.rglob("*"):
            try:
                if any(part in ignored_dirs for part in path.parts):
                    continue
                if path.is_file():
                    rel_path = path.relative_to(base_dir)
                    file_list.append(str(rel_path))
            except (PermissionError, OSError):
                continue
    except (PermissionError, OSError):
        pass

    return sorted(file_list)