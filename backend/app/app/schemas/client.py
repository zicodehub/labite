
from typing import Dict, Optional, List
from app.schemas.commande import Commande
# from datetime import datetime,date


from pydantic import BaseModel, Json

# Shared properties
class ClientBase(BaseModel):    
    name: Optional[str]
    coords: Optional[str]
    time_service: Optional[int]
    time_interval_start: Optional[int]
    time_interval_end: Optional[int]
    is_active: Optional[bool] = True

class ClientCreate(ClientBase):
    coords: str
    time_service: int
    time_interval_start: int
    time_interval_end: int

class ClientUpdate(ClientBase):
    pass


# Properties shared by models stored in DB
class ClientInDB(ClientBase):
    id: int
    commandes: List[Commande]
    class Config:
        orm_mode = True


# Properties to return to client
class Client(ClientInDB):
    pass
