from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class CRUDItem(CRUDBase[Client, ClientCreate, ClientUpdate]):
    pass

client = CRUDItem(Client)
