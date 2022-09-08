
import enum
from typing import Dict, Optional, List, Union
from app.schemas.fournisseur import Fournisseur
from app.core.config import settings
# from datetime import datetime,date
from app import models, schemas

from pydantic import BaseModel, Json

class NodeType(enum.Enum):
    fournisseur = "Fournisseur"
    client = "Client"
    depot = "Depot"

class Node(BaseModel):
    name: Optional[str]
    code: Optional[str]
    coords: str
    type: NodeType
    mvt: Optional[int]

class HoldedOrder(BaseModel):
    commande_id: int
    compartiment_id: int
    qty_holded: int 
    is_active: bool

    class Config:
        orm_mode = True

class CompartimentBase(BaseModel):
    vehicule_id: Optional[int]

class CompartimentCreate(CompartimentBase):
    vehicule_id: int

class CompartimentUpdate(CompartimentBase):
    pass

class Compartiment(CompartimentBase):
    id: int
    vehicule_id: int
    holded_orders: List[HoldedOrder]

    class Config:
        orm_mode = True

# Shared properties
class VehiculeBase(BaseModel):    
    name: Optional[str]
    code: Optional[str]
    velocity: Optional[int] = settings.VITESSE_VEHICULE
    nb_compartment: Optional[int]
    size_compartment: Optional[int]
    cout: Optional[int]
    depot_id: Optional[int]
    is_active: Optional[bool] = True

class VehiculeCreate(VehiculeBase):
    nb_compartment: int
    size_compartment: int
    cout: int
    depot_id: int
    
class VehiculeUpdate(VehiculeBase):
    pass


# Properties shared by models stored in DB
class VehiculeInDB(VehiculeBase):
    id: int
    compartiments: List[Compartiment]
    trajet: List

    depot: schemas.Depot

    class Config:
        orm_mode = True


# Properties to return to client
class Vehicule(VehiculeInDB):
    pass
