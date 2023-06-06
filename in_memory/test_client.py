import base_model
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import TypeVar
from schemas.config import ModelFilterSchema, FilterAgregationRuleSchema
from model_client import *

t1 = ClientModel({"x": 45.0, "y": 90.0})
print(t1)
t2 = ClientModel.create({"x": 21.0, "y": 718.0})
many = ClientModel.create_many([
    {"x": 67.0, "y": 718.0},
    {"x": 86.0, "y": 13.0}
])

assert len(ClientModel.list_all()) == 4

for t in ClientModel.list_all():
    assert isinstance(t.x, float)

del1 = ClientModel.delete(1)
assert del1 == t1

try:
    ClientModel.get(1)
except:
    pass
else:
    raise("ID 1 deleted")

# x value of deleted
filter1 = ClientModel.filter([
    ModelFilterSchema(field= 'x', value=45.0)
])
for res in filter1:
    assert res.x == 45.0
assert len(filter1) == 0

# No existant x value
filter2 = ClientModel.filter([
    ModelFilterSchema(field= 'x', value=82913.0)
])
for res in filter2:
    assert res.x == 67

# Actual value
filter3 = ClientModel.filter([
    ModelFilterSchema(field= 'x', value=67.0)
])
for res in filter3:
    assert res.x == 67


# Test OR rule
filter4 = ClientModel.filter([
    ModelFilterSchema(field= 'x', value=91029082.0),
    ModelFilterSchema(field= 'x', value=67.0)
], rule= FilterAgregationRuleSchema.OR)
for res in filter4:
    assert res.x == 67 or res.x == 91029082
    
assert len(filter4) == 1


# Test AND rule
# Aucune attente
filter5 = ClientModel.filter([
    ModelFilterSchema(field= 'y', value=90.0),
    ModelFilterSchema(field= 'x', value=67.0)
], rule= FilterAgregationRuleSchema.AND)
for res in filter5:
    print(res)
    assert res.x == 67 and res.y == 90
    
assert len(filter5) == 0

# Test AND rule
# Avec un valeur existante
filter6 = ClientModel.filter([
    ModelFilterSchema(field= 'y', value=718.0),
    ModelFilterSchema(field= 'x', value=67.0)
], rule= FilterAgregationRuleSchema.AND)
for res in filter6:
    print(res)
    assert res.x == 67 and res.y == 718
    
assert len(filter6) == 1