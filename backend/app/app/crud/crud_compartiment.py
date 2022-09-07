from typing import List, Tuple
from app.db.session import SessionLocal

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.vehicule import Compartiment
from app.schemas.vehicule import CompartimentCreate, CompartimentUpdate
from app import models, crud, schemas

from app.db.session import get_db
db = get_db().send(None)

class CRUDItem(CRUDBase[Compartiment, CompartimentCreate, CompartimentUpdate]):
    pass
  
compartiment = CRUDItem(Compartiment)
