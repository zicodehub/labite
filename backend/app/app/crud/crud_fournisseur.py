from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.fournisseur import Fournisseur
from app.schemas.fournisseur import FournisseurCreate, FournisseurUpdate


class CRUDItem(CRUDBase[Fournisseur, FournisseurCreate, FournisseurUpdate]):
    pass

fournisseur = CRUDItem(Fournisseur)
