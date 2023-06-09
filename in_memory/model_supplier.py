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

    def __init__(self, datum: Dict[str, Any]):
        from model_order import OrderModel
        
        self.orders: list[OrderModel] = []
        super().__init__(datum)

    def register_order(self, order):
        self.orders.append(order)
    
    @staticmethod
    def prefix():
        return 'F'
    
    @property
    def name(self) -> str:
        return f"{self.prefix()}{self.id}"