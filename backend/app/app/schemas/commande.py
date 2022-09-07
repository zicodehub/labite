import enum
from optparse import Option
from typing import Dict, Optional,List, Any, Union
# from datetime import datetime,date


from pydantic import BaseModel, Json

# Shared properties
class CommandeBase(BaseModel):  
    qty: Optional[int] = 0
    is_delivered: Optional[bool] = True
    is_active: Optional[bool] = True

class CommandeCreate(CommandeBase):
    client_id: int
    fournisseur_id: int
    produit_id: int
    qty: int

class CommandeUpdate(CommandeBase):
    pass


# Properties shared by models stored in DB
class CommandeInDB(CommandeBase):
    id: int
    produit_id: Optional[int]
    client_id: Optional[int]
    fournisseur_id: Optional[int]
    
    class Config:
        orm_mode = True


# Properties to return to client
class Commande(CommandeInDB):
    pass
