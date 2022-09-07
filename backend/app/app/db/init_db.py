from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.core.config import settings
from app.db import base, session  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    base.Base.metadata.create_all(bind=session.engine)

    first_depot = crud.depot.get_first()
    if not first_depot:
        first_depot = crud.depot.create(schemas.DepotCreate(coords = "0;0", time_interval_start = 1, time_interval_end = 23))
