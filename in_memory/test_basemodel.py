import base_model
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import TypeVar, Dict, Any
from schemas.config import ModelFilterSchema, FilterAgregationRuleSchema
from utils import reset_all

reset_all()

class TestSchema(BaseModel):
    x: int
    y: int

TestModelType = TypeVar("TestModelType", bound= "TestModel")

class TestModel(base_model.Base[TestModelType, TestSchema]):
    SCHEMA = TestSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}
    

# v= {"x": 67, "y": 718}
# TestSchema(**jsonable_encoder(v))
t1 = TestModel({"x": 45, "y": 90})
t2 = TestModel.create({"x": 21, "y": 718})
many = TestModel.create_many([
    {"x": 67, "y": 718},
    {"x": 86, "y": 13}
])

assert len(TestModel.list_all()) == 4

for t in TestModel.list_all():
    assert isinstance(t.x, int)

del1 = TestModel.delete(1)
assert del1 == t1

try:
    TestModel.get(1)
except:
    pass
else:
    raise("ID 1 deleted")

# x value of deleted
filter1 = TestModel.filter([
    ModelFilterSchema(field= 'x', value=45)
])
for res in filter1:
    assert res.x == 45
assert len(filter1) == 0

# No existant x value
filter2 = TestModel.filter([
    ModelFilterSchema(field= 'x', value=82913)
])
for res in filter2:
    assert res.x == 67

# Actual value
filter3 = TestModel.filter([
    ModelFilterSchema(field= 'x', value=67)
])
for res in filter3:
    assert res.x == 67


# Test OR rule
filter4 = TestModel.filter([
    ModelFilterSchema(field= 'x', value=91029082),
    ModelFilterSchema(field= 'x', value=67)
], rule= FilterAgregationRuleSchema.OR)
for res in filter4:
    assert res.x == 67 or res.x == 91029082
    
assert len(filter4) == 1


# Test AND rule
# Aucune attente
filter5 = TestModel.filter([
    ModelFilterSchema(field= 'y', value=90),
    ModelFilterSchema(field= 'x', value=67)
], rule= FilterAgregationRuleSchema.AND)
for res in filter5:
    print(res)
    assert res.x == 67 and res.y == 90
    
assert len(filter5) == 0

# Test AND rule
# Avec un valeur existante
filter6 = TestModel.filter([
    ModelFilterSchema(field= 'y', value=718),
    ModelFilterSchema(field= 'x', value=67)
], rule= FilterAgregationRuleSchema.AND)
for res in filter6:
    print(res)
    assert res.x == 67 and res.y == 718
    
assert len(filter6) == 1