from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base

ClientModelType = TypeVar("ClientModelType", bound= "ClientModel")

class ClientSchema(BaseModel):
    x: float
    y: float

class ClientModel(Base[ClientModelType, ClientSchema]):
    SCHEMA = ClientSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}