from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base
from _types import *

class BatchSchema(BaseModel):
    compartment_id: int
    order_id: int
    qty_holded: int
    is_active: bool = True
    
class BatchModel(Base[BatchModelType, BatchSchema]):
    SCHEMA = BatchSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}

    def __init__(self, datum: Dict[str, Any]):
        from  model_compartment import CompartmentModel

        self.compartment: CompartmentModel
        self.order: OrderModelType
        
        super().__init__(datum)


    def _register_relations(self):
        from model_compartment import CompartmentModel
        from model_order import OrderModel
        
        _compartment = CompartmentModel.get(self.datum.compartment_id)
        self.compartment = _compartment
        self.compartment.register_batch(self)
        
        _order = OrderModel.get(self.datum.order_id)
        self.order = _order
        self.order.register_batch(self)
      