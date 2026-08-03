from sqlalchemy.orm import Session
from mentor.database import Sessions, engine
from sqlalchemy import select



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