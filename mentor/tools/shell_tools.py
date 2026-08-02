import subprocess
from pathlib import Path

ALLOWED_EXECUTABLES = {"pytest", "python", "uv", "ruff", "mypy"}
FORBIDDEN_KEYWORDS = {"rm", "del", "rmdir", "-c", "--command", "shutil"}

def execute_workspace_command(project_name: str, command: str) -> str:
    """Executes a whitelisted development command inside workspace/{project_name}/."""
    tokens = command.strip().split()
    if not tokens:
        raise ValueError("Empty command string provided.")

    executable = tokens[0]

    # 1. Whitelist check
    if executable not in ALLOWED_EXECUTABLES:
        raise PermissionError(f"Command '{executable}' is not in the approved executable whitelist: {ALLOWED_EXECUTABLES}")

    # 2. Forbidden keyword / flag check
    for token in tokens:
        if token.lower() in FORBIDDEN_KEYWORDS:
            raise PermissionError(f"Command contains forbidden token/flag: '{token}'")

    cwd = (Path.cwd() / "workspace" / project_name).resolve()
    cwd.mkdir(parents=True, exist_ok=True)

    # 3. Safe execution
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30
    )

    output = result.stdout if result.returncode == 0 else result.stderr
    return f"Command exit code: {result.returncode}\nOutput:\n{output}"