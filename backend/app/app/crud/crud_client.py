from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate
from app.db.session import SessionLocal

class CRUDItem(CRUDBase[Client, ClientCreate, ClientUpdate]):
    def create(self, obj_in: ClientCreate, db: Session = SessionLocal()) -> Client:
        client = super().create(obj_in= obj_in, db= db)
        client.name = f'C{client.id}'
        db.add(client)
        db.commit()
        db.refresh(client)
        return client
client = CRUDItem(Client)
