from .engine import engine
from .models import Base

def init_db(force: bool = False):

    if force:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)