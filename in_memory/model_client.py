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

    def __init__(self, datum: Dict[str, Any]):
        from model_order import OrderModel
        
        self.orders: list[OrderModel] = []
        super().__init__(datum)

    def register_order(self, order):
        self.orders.append(order)

    @property
    def name(self) -> str:
        return f"C{self.id}"