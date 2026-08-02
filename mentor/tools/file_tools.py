from pathlib import Path

def write_workspace_file(project_name: str, relative_path: str, content: str) -> str:
    """Writes a file safely inside workspace/{project_name}/."""
    base_dir = (Path.cwd() / "workspace" / project_name).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)

    target_path = (base_dir / relative_path).resolve()

    # Sandboxing check
    if not target_path.is_relative_to(base_dir):
        raise ValueError(f"Security Alert: Path '{relative_path}' escapes workspace sandbox.")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    return f"Successfully wrote file '{relative_path}' in project '{project_name}'."