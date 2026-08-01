from sqlalchemy import select
from sqlalchemy.orm import Session

from mentor.database import Messages, engine


def load_messages(session_id: str) -> list[dict]:
    """ Load all messages for a session in chronological order."""
    with Session(engine) as session:
        messages = session.scalars(
            select(Messages).where(Messages.session_id == session_id).order_by(Messages.id)
        ).all()

        return [{
            "role": message.role,
            "content": message.content,
        } for message in messages ]

def save_message(session_id: str, role: str, content: str, tool_calls: str = None) -> None:
    """ insert new message into db """

    with Session(engine) as session:
        message = Messages(
            session_id = session_id,
            role = role,
            content = content,
            tool_calls = tool_calls
        )

        session.add(message)
        session.commit()
