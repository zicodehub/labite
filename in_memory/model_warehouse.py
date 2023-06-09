from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base

WarehoudeModelType = TypeVar("WarehoudeModelType", bound= "WarehoudeModel")

class WarehouseSchema(BaseModel):
    x: float
    y: float

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
    
    @staticmethod
    def prefix():
        return 'D'
    
    @property
    def name(self) -> str:
        return f"{self.prefix()}{self.id}"