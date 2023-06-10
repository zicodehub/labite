import base_model
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import TypeVar
from schemas.config import ModelFilterSchema, FilterAgregationRuleSchema
from model_warehouse import *
from model_vehicule import *
from model_compartment import *
from utils import reset_all

reset_all()

w1 = WarehoudeModel({'x': 0.0, 'y': 0.0})
assert w1.name == "D1"
assert w1.id == 1

v1 = VehiculeModel({
    "warehouse_id": w1.id,
    "nb_compartments": 12,
    "size_compartment": 24,
    "cost": 390
})

assert v1.warehouse is w1
assert len(v1.compartments) == 12

