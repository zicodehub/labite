from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base

ArticleModelType = TypeVar("ArticleModelType", bound= "ArticleModel")

class ArticleSchema(BaseModel):
    name: str
    type_article_id: int

class ArticleModel(Base[ArticleModelType, ArticleSchema]):
    SCHEMA = ArticleSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}

    def __init__(self, datum: Dict[str, Any]):
        from  model_type_article import TypeArticleModel
        from model_order import OrderModel

        self.type_article: TypeArticleModel
        self.orders: list[OrderModel] = []
        super().__init__(datum)


    def _register_relations(self):
        from  model_type_article import TypeArticleModel
        
        type_article = TypeArticleModel.get(self.datum.type_article_id)
        self.type_article = type_article
        type_article.register_article(self)

    def register_order(self, order):
        self.orders.append(order)