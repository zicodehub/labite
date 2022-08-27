import enum
from optparse import Option
from typing import Dict, Optional,List, Any, Union
from app.schemas.commande import Commande
from app.schemas.produit import Produit
# from datetime import datetime,date


from pydantic import BaseModel, Json

# Shared properties
class FournisseurBase(BaseModel):    
    name: Optional[str]
    coords: Optional[str]
    time_service: Optional[int]
    time_interval_start: Optional[int]
    time_interval_end: Optional[int]
    is_active: Optional[bool] = True

class FournisseurCreate(FournisseurBase):
    coords: str
    time_service: int
    time_interval_start: int
    time_interval_end: int

class FournisseurUpdate(FournisseurBase):
    pass


# Properties shared by models stored in DB
class FournisseurInDB(FournisseurBase):
    id: int
    commandes: List[Commande]
    produits: List[Produit]

    class Config:
        orm_mode = True


# Properties to return to client
class Fournisseur(FournisseurInDB):
    pass
