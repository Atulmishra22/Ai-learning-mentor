import pytest
from pathlib import Path

from mentor.workspace import get_workspace_dir, is_safe_workspace_path, list_project_files
from mentor.tools.file_tools import write_workspace_file
from mentor.tools.shell_tools import execute_workspace_command


# ==============================================================================
# TEST GROUP 1: WORKSPACE SANDBOXING & FILE LISTING
# ==============================================================================

def test_workspace_dir_creation(temp_workspace):
    """Test that get_workspace_dir creates workspace/ directory."""
    ws = get_workspace_dir()
    assert ws.exists()
    assert ws.name == "workspace"


def test_is_safe_workspace_path_valid(temp_workspace):
    """Test valid paths inside workspace."""
    is_safe, target = is_safe_workspace_path("main.py")
    assert is_safe is True
    assert target.name == "main.py"


def test_is_safe_workspace_path_traversal_blocked(temp_workspace):
    """Test that path traversal attempts (../../) are blocked."""
    is_safe, target = is_safe_workspace_path("../../etc/passwd")
    assert is_safe is False


def test_list_project_files_filtering(temp_workspace):
    """Test that list_project_files excludes ignored directories like __pycache__."""
    ws = get_workspace_dir()
    (ws / "main.py").write_text("print('hello')", encoding="utf-8")

    # Create ignored folder
    pycache = ws / "__pycache__"
    pycache.mkdir(parents=True, exist_ok=True)
    (pycache / "compiled.pyc").write_text("cache", encoding="utf-8")

    files = list_project_files()
    assert "main.py" in files
    assert "__pycache__/compiled.pyc" not in files


# ==============================================================================
# TEST GROUP 2: TOOL EXECUTION HANDLERS & SECURITY WHITELIST
# ==============================================================================

def test_write_workspace_file_success(temp_workspace):
    """Test writing a valid file inside workspace."""
    res = write_workspace_file("src/app.py", "print('app')")
    assert "Successfully wrote file" in res

    ws = get_workspace_dir()
    assert (ws / "src" / "app.py").read_text(encoding="utf-8") == "print('app')"


def test_write_workspace_file_traversal_exception(temp_workspace):
    """Test that writing outside workspace raises ValueError security alert."""
    with pytest.raises(ValueError, match="Security Alert"):
        write_workspace_file("../outside.txt", "evil")


def test_execute_workspace_command_whitelist_pass(temp_workspace):
    """Test running a whitelisted command like python --version."""
    res = execute_workspace_command("python --version")
    assert "Command exit code: 0" in res


def test_execute_workspace_command_unapproved_executable_blocked(temp_workspace):
    """Test that non-whitelisted executables like bash or npm are blocked."""
    with pytest.raises(PermissionError, match="not in the approved executable whitelist"):
        execute_workspace_command("bash -c ls")


def test_execute_workspace_command_forbidden_flag_blocked(temp_workspace):
    """Test that forbidden flags/keywords like rm are blocked."""
    with pytest.raises(PermissionError, match="contains forbidden token/flag"):
        execute_workspace_command("python -c rm")