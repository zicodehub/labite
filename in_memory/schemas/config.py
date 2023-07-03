import enum
from pydantic import BaseModel
from typing import Any, Optional, List

DEBUG = True

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
    x: float
    y: float
    type: NodeType
    mvt: Optional[int]

class APIInput(BaseModel):
    clients: Any
    suppliers: List
    type_articles: List
    articles: List
    orders: List
    warehouses: List
    vehicules: List

class GeneticParams(BaseModel):
    nb_generations: int = 10
    gen_max_selection: int = 70,
    proba_mutation: float = 0.3

class RecuitParams(BaseModel):
    temp: int = 10
    reductor: float = 0.99,
    proba_admission: float = 0.3

class APIGeneticInput(APIInput):
    algo_params: GeneticParams

class APIRecuitInput(APIInput):
    algo_params: RecuitParams
