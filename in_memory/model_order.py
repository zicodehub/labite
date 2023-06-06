from typing import TypeVar, Dict, Any
from pydantic import BaseModel
from base_model import Base

OrderModelType = TypeVar("OrderModelType", bound= "OrderModel")

class OrderSchema(BaseModel):
    supplier_id: int
    client_id: int
    article_id: int
    qty: int
    
class OrderModel(Base[OrderModelType, OrderSchema]):
    SCHEMA = OrderSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}

    def __init__(self, datum: Dict[str, Any]):
        from model_article import ArticleModel
        from model_client import ClientModel
        from model_supplier import SupplierModel

        self.article: ArticleModel
        self.client: ClientModel
        self.supplier: SupplierModel

        super().__init__(datum)
        self.qty_flex: int = self.datum.qty

    def _register_relations(self):
        from model_article import ArticleModel
        from model_client import ClientModel
        from model_supplier import SupplierModel

        _article = ArticleModel.get(self.datum.article_id)
        _client = ClientModel.get(self.datum.client_id)
        _supplier = SupplierModel.get(self.datum.supplier_id)
        
        self.article = _article
        self.article.register_order(self)

        self.client = _client
        self.client.register_order(self)

        self.supplier = _supplier
        self.client.register_order(self)