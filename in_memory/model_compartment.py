from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base
from _types import *

class CompartmentSchema(BaseModel):
    vehicule_id: int
    # size: int
    
class CompartmentModel(Base[CompartmentModelType, CompartmentSchema]):
    SCHEMA = CompartmentSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}

    def __init__(self, datum: Dict[str, Any]):
        from  model_vehicule import VehiculeModel

        self.vehicule: VehiculeModel
        self.batches: list[BatchModelType] = []

        super().__init__(datum, auto_create_pk = True)


    def _register_relations(self):
        from  model_vehicule import VehiculeModel
        
        _vehicule = VehiculeModel.get(self.datum.vehicule_id)
        self.vehicule = _vehicule
        self.vehicule.register_compartment(self)
      
    def register_batch(self, batch: BatchModelType):
        self.batches.append(batch)