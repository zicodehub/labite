import enum
from optparse import Option
from typing import Dict, Optional,List, Any, Union
# from datetime import datetime,date


from pydantic import BaseModel, Json

# Shared properties
class TypeBase(BaseModel):    
    name: Optional[str]
    is_active: Optional[bool] = True

class TypeCreate(TypeBase):
    name: str


class TypeUpdate(TypeBase):
    pass


# Properties shared by models stored in DB
class TypeInDB(TypeBase):
    id: int
    
    class Config:
        orm_mode = True


# Properties to return to client
class TypeProduit(TypeInDB):
    pass
