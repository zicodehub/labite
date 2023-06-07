from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base

WarehoudeModelType = TypeVar("WarehoudeModelType", bound= "WarehoudeModel")

class WarehouseSchema(BaseModel):
    name: str

class WarehoudeModel(Base[WarehoudeModelType, WarehouseSchema]):
    
    SCHEMA = WarehouseSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}

    def __init__(self, datum: Dict[str, Any]):
        from model_vehicule import VehiculeModel
        self.vehicules: list[VehiculeModel] = []

        super().__init__(datum)
    
    def register_vehicule(self, vehicule):
        self.vehicules.append(vehicule)
    