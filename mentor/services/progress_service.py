
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from mentor.database import Progresstable, engine


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