from mentor.workspace import is_safe_workspace_path

def write_workspace_file(relative_path: str, content: str, project_name: str = "workspace") -> str:
    """Writes a file inside the active workspace directory with path sandboxing."""
    is_safe, target_path = is_safe_workspace_path(relative_path)
    if not is_safe:
        raise ValueError(f"Security Alert: Path '{relative_path}' escapes workspace sandbox.")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    return f"Successfully wrote file '{relative_path}'."