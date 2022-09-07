import enum
from optparse import Option
from typing import Dict, Optional,List, Any, Union
# from datetime import datetime,date


from pydantic import BaseModel, Json
# from .vehicule import Vehicule
# from app import schemas

# Shared properties
class DepotBase(BaseModel):    
    name: Optional[str]
    coords: Optional[str]
    time_interval_start: Optional[int]
    time_interval_end: Optional[int]
    is_active: Optional[bool] = True

class DepotCreate(DepotBase):
    coords: str
    time_interval_start: int
    time_interval_end: int

class DepotUpdate(DepotBase):
    pass


# Properties shared by models stored in DB
class DepotBaseInDB(DepotBase):
    id: int
    # vehicules: List[Vehicule]
    class Config:
        orm_mode = True


# Properties to return to client
class Depot(DepotBaseInDB):
    pass
