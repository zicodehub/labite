from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base

SupplierModelType = TypeVar("SupplierModelType", bound= "SupplierModel")

class SupplierSchema(BaseModel):
    x: float
    y: float

class SupplierModel(Base[SupplierModelType, SupplierSchema]):
    SCHEMA = SupplierSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}