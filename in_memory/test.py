import base_model
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import TypeVar

class TestSchema(BaseModel):
    x: int
    y: int

TestModelType = TypeVar("TestModelType", bound= "TestModel")

class TestModel(base_model.Base[TestModelType]):
    SCHEMA = TestSchema

# v= {"x": 67, "y": 718}
# TestSchema(**jsonable_encoder(v))
t1 = TestModel({"x": 45, "y": 90})
t2 = TestModel.create({"x": 67, "y": 718})
many = TestModel.create_many([
    {"x": 67, "y": 718},
    {"x": 86, "y": 13}
])

assert len(TestModel.list_all()) == 4
assert t1.id == 1
assert many[1].id == 4

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