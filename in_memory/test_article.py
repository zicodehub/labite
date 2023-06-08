import base_model
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import TypeVar
from schemas.config import ModelFilterSchema, FilterAgregationRuleSchema
from model_type_article import *
from model_article import *

from utils import reset_all

reset_all()

t1 = TypeArticleModel({"name": "Riz"})
print(t1)

assert len(t1.articles) == 0

art1 = ArticleModel({
    'name': 'Rizière',
    'type_article_id': t1.id
})

art2 = ArticleModel({
    'name': 'Rizière',
    'type_article_id': t1.id
})

assert len(t1.articles) == 2
assert t1.articles[0] is art1
assert t1.articles[1] is art2

assert art1.type_article is t1