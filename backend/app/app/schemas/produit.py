import enum
from optparse import Option
from typing import Dict, Optional,List, Any, Union
# from datetime import datetime,date


from pydantic import BaseModel, Json

# Shared properties
class ProduitBase(BaseModel):    
    name: Optional[str]
    is_active: Optional[bool] = True

class ProduitCreate(ProduitBase):
    type: int
    name: str


class ProduitUpdate(ProduitBase):
    pass


# Properties shared by models stored in DB
class ProduitInDB(ProduitBase):
    id: int
    type: int
    
    class Config:
        orm_mode = True


# Properties to return to client
class Produit(ProduitInDB):
    pass
