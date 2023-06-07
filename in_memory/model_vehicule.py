from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base

VehiculeModelType = TypeVar("VehiculeModelType", bound= "VehiculeModel")

class VehiculeSchema(BaseModel):
    warehouse_id: int
    speed: float = 60 # Km/s
    nb_compartments: int
    size_compartments: int
    cost: int

class VehiculeModel(Base[VehiculeModelType, VehiculeSchema]):
    SCHEMA = VehiculeSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}

    def __init__(self, datum: Dict[str, Any]):
        from  model_warehouse import WarehoudeModel
        from model_compartment import CompartmentModel

        self.warehouse: WarehoudeModel
        self.compartments: list[CompartmentModel] = []
        super().__init__(datum)


    def _register_relations(self):
        from  model_warehouse import WarehoudeModel
        from model_compartment import CompartmentModel

        _warehouse = WarehoudeModel.get(self.datum.warehouse_id)
        self.warehouse = _warehouse
        self.warehouse.register_vehicule(self)
        
        for i in range(self.datum.nb_compartments):
            _comp = CompartmentModel({
                'vehicule_id': self.id,
                'size': self.datum.size_compartments
            })

    def register_compartment(self, compartment):
        self.compartments.append(compartment)
        
    @property
    def name(self) -> str:
        return f"V{self.id}"