from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.produit import TypeProduit
from app.schemas.type_produit import TypeCreate, TypeUpdate


class CRUDItem(CRUDBase[TypeProduit, TypeCreate, TypeUpdate]):
    pass

type_produit = CRUDItem(TypeProduit)
