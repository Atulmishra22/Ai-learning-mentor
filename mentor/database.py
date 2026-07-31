from sqlalchemy import create_engine, INTEGER, String,ForeignKey, Text, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

class Base(DeclarativeBase):
    pass

class Sessions(Base):
    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)

class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True,autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(255), ForeignKey("sessions.session_id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tool_calls: Mapped[str | None] = mapped_column(Text, nullable=True)

class Progresstable(Base):
    __tablename__ = "progress"

    project_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    milestone_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    milestone_order: Mapped[int] = mapped_column(INTEGER, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")

Base.metadata.create_all(engine)

# session and history Managers

def create_session_if_not_exists(session_id: str, project_name: str) -> None :
    """Create a new session only if it does not already exist."""
    with Session(engine) as session:

        existing_session = session.scalar(
            select(Sessions).where(Sessions.session_id == session_id)
        )

        if existing_session is not None:
            return

        session.add(
            Sessions(
                session_id=session_id,
                project_name=project_name,
            )
        )

        session.commit()

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

# curriculum and progress managers

def create_project_milestones(
    project_name: str,
    milestones: list[str],
) -> None:
    """Replace all milestones for a project."""

    with Session(engine) as session:

        session.execute(
            delete(Progresstable).where(
                Progresstable.project_name == project_name
            )
        )

        for order, milestone in enumerate(milestones, start=1):
            session.add(
                Progresstable(
                    project_name=project_name,
                    milestone_name=milestone,
                    milestone_order=order,
                    status="pending",
                )
            )

        session.commit()


    
def get_milestones(project_name: str) -> list[dict]:
    """Return all milestones for a project."""

    with Session(engine) as session:

        milestones = session.scalars(
            select(Progresstable)
            .where(Progresstable.project_name == project_name)
            .order_by(Progresstable.milestone_order)
        ).all()

        return [
            {
                "name": milestone.milestone_name,
                "order": milestone.milestone_order,
                "status": milestone.status,
            }
            for milestone in milestones
        ]

def mark_milestone_completed(
    project_name: str,
    milestone_name: str,
) -> bool:
    """Mark a milestone as completed."""

    with Session(engine) as session:

        milestone = session.scalar(
            select(Progresstable).where(
                Progresstable.project_name == project_name,
                Progresstable.milestone_name == milestone_name,
            )
        )

        if milestone is None:
            return False

        milestone.status = "completed"

        session.commit()

        return True