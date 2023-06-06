from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base

TypeArticleModelType = TypeVar("TypeArticleModelType", bound= "TypeArticleModel")

class TypeArticleSchema(BaseModel):
    name: str

class TypeArticleModel(Base[TypeArticleModelType, TypeArticleSchema]):
    
    SCHEMA = TypeArticleSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}

    def __init__(self, datum: Dict[str, Any]):
        from model_article import ArticleModel
        self.articles: list[ArticleModel] = []

        super().__init__(datum)
    def register_article(self, article: TypeArticleModelType):
        self.articles.append(article)
    