from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.fournisseur import Fournisseur
from app.schemas.fournisseur import FournisseurCreate, FournisseurUpdate
from app.db.session import SessionLocal

class CRUDItem(CRUDBase[Fournisseur, FournisseurCreate, FournisseurUpdate]):
    def create(self, obj_in: FournisseurCreate, db: Session = SessionLocal()) -> Fournisseur:
        fourn = super().create(obj_in= obj_in, db= db)
        fourn.name = f'F{fourn.id}'
        db.add(fourn)
        db.commit()
        db.refresh(fourn)
        return fourn

fournisseur = CRUDItem(Fournisseur)
