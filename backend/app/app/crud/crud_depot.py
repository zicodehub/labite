from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.depot import Depot
from app.schemas.depot import DepotCreate, DepotUpdate


class CRUDItem(CRUDBase[Depot, DepotCreate, DepotUpdate]):
    pass

depot = CRUDItem(Depot)
