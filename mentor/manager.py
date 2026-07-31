import json
from pathlib import Path
from mentor.prompt import SYSTEM_PROMPT

class ConversationManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.conversation = self.load()
    
    def load(self) -> list[dict]:
        """Load the conversation history from the JSON file."""
        if Path(self.file_path).exists():
            with open(self.file_path, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return [{"role": "system", "content": SYSTEM_PROMPT}]
        return [{"role": "system", "content": SYSTEM_PROMPT}]

    def save(self):
        """Save the conversation history to the JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(self.conversation, f, indent=4)

    def append(self, role: str, content: str):
        """Append a new message to the conversation."""
        self.conversation.append({"role": role, "content": content})
        self.save()

    def reset(self):
        """Reset the conversation history."""
        self.conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.save()
    
