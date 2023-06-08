import enum
from pydantic import BaseModel
from typing import Any, Optional

class PK_MNT_METHOD(enum.Enum):
    SERIAL = "SERIAL"
    MANUAL = "MANUAL"


class FilterAgregationRuleSchema(enum.Enum):
    AND = "AND"
    OR = "OR"

class ModelFilterSchema(BaseModel):
    field: str
    format: Optional[str]
    operator: str = '=='
    value: Any

class NodeType(enum.Enum):
    fournisseur = "Fournisseur"
    client = "Client"
    depot = "Depot"

class Node(BaseModel):
    name: Optional[str]
    code: Optional[str]
    coords: str
    type: NodeType
    mvt: Optional[int]