import json
from pathlib import Path


class ProgressTracker:
    def __init__(
        self,
        project_name: str,
        milestones: list[str],
        file_path: str = "progress.json",
    ):
        self.project_name = project_name
        self.file_path = Path(file_path)
        self.milestones = milestones

        self._state = self._load()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def completed(self) -> list[str]:
        return self._state["completed_milestones"]

    @property
    def current(self) -> str | None:
        return self._state["current_milestone"]

    @property
    def total(self) -> int:
        return len(self.milestones)

    @property
    def progress(self) -> float:
        if self.total == 0:
            return 100.0
        return len(self.completed) / self.total * 100

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> dict:
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if self.project_name in data:
                    return data[self.project_name]

            except (json.JSONDecodeError, OSError):
                pass

        return {
            "completed_milestones": [],
            "current_milestone": self.milestones[0] if self.milestones else None,
        }

    def save(self):
        data = {}

        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass

        data[self.project_name] = self._state

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # ------------------------------------------------------------------
    # Progress
    # ------------------------------------------------------------------

    def complete_current_milestone(self):
        if self.current is None:
            return False

        if self.current not in self.completed:
            self.completed.append(self.current)

        current_index = self.milestones.index(self.current)

        if current_index + 1 < len(self.milestones):
            self._state["current_milestone"] = self.milestones[current_index + 1]
        else:
            self._state["current_milestone"] = None

        self.save()
        return True

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def get_summary(self) -> str:
        bar_length = 20

        filled = int((self.progress / 100) * bar_length)

        bar = "█" * filled + "░" * (bar_length - filled)

        remaining = [
            m
            for m in self.milestones
            if m not in self.completed and m != self.current
        ]

        lines = [
            f"📊 Project: {self.project_name}",
            "",
            f"Progress: [{bar}] {self.progress:.0f}% ({len(self.completed)}/{self.total})",
            "",
            "✅ Completed:",
        ]

        if self.completed:
            lines.extend(f"   ✓ {m}" for m in self.completed)
        else:
            lines.append("   None")

        lines.append("")

        if self.current:
            lines.append(f"🚀 Current:\n   → {self.current}")
        else:
            lines.append("🎉 All milestones completed!")

        if remaining:
            lines.append("")
            lines.append("📌 Remaining:")
            lines.extend(f"   • {m}" for m in remaining)

        return "\n".join(lines)