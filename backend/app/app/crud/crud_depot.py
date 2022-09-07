from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.depot import Depot
from app.schemas.depot import DepotCreate, DepotUpdate
from app.db.session import SessionLocal

class CRUDItem(CRUDBase[Depot, DepotCreate, DepotUpdate]):
    def create(self, obj_in: DepotCreate, db: Session = SessionLocal()) -> Depot:
        depot = super().create(obj_in= obj_in, db= db)
        depot.name = f'D{depot.id}'
        db.add(depot)
        db.commit()
        db.refresh(depot)
        return depot

depot = CRUDItem(Depot)
