

from sqlalchemy import INTEGER, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
