import shutil
import pytest
from pathlib import Path

@pytest.fixture
def temp_workspace(tmp_path, monkeypatch):
    """
    Creates a clean, isolated temporary workspace directory for testing.
    Monkeypatches Path.cwd() to return tmp_path so unit tests never touch real files.
    """
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir(parents=True, exist_ok=True)

    # Temporary override Path.cwd() to point to tmp_path
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)

    yield workspace_dir

    # Cleanup after test finishes
    if workspace_dir.exists():
        shutil.rmtree(workspace_dir)