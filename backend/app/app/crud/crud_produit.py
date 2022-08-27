from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.produit import Produit
from app.schemas.produit import ProduitCreate, ProduitUpdate


class CRUDItem(CRUDBase[Produit, ProduitCreate, ProduitUpdate]):
    def are_produits_similar(self, produit_1: Produit, produit_2: Produit) -> bool:
        return produit_1.id == produit_2.id

produit = CRUDItem(Produit)
