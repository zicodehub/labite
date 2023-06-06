import enum
from pydantic import BaseModel
from typing import Any

class PK_MNT_METHOD(enum.Enum):
    SERIAL = "SERIAL"
    MANUAL = "MANUAL"


class FilterAgregationRuleSchema(enum.Enum):
    AND = "AND"
    OR = "OR"

class ModelFilterSchema(BaseModel):
    field: str
    operator: str = '=='
    value: Any