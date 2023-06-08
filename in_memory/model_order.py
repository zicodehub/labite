from typing import TypeVar, Dict, Any, List
from pydantic import BaseModel
from base_model import Base
from _types import *
from schemas.config import ModelFilterSchema, FilterAgregationRuleSchema

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
        self.supplier.register_order(self)

    def decrease_qty(self, order: OrderModelType, value: int = 1) -> OrderModelType:
        self.qty_flex -= value
        return self

    @classmethod
    def must_deliver_client(cls, f: ClientModelType, client: ClientModelType) -> bool:
        return len(cls.filter([
            ModelFilterSchema(
                field = 'supplier_id',
                value = f.id
            ),
            ModelFilterSchema(
                field = 'client_id',
                value = client.id
            )
        ])) > 0
            
    @classmethod
    def get_fournisseurs(cls) -> List[SupplierModelType]:
        from model_supplier import SupplierModel
        return SupplierModel.filter([
            ModelFilterSchema(
                format = 'count',
                field = 'orders',
                operator = '!=',
                value = 0
            )
        ], bypass_type_checking= True)

    @classmethod
    def get_clients(cls) -> List[SupplierModelType]:
        from model_client import ClientModel
        return ClientModel.filter([
            ModelFilterSchema(
                format = 'count',
                field = 'orders',
                operator = '!=',
                value = 0
            )
        ], bypass_type_checking= True)
    
    @classmethod
    def get_by_fournisseur(cls, f: SupplierModelType) -> List[OrderModelType]:
        return cls.filter([
            ModelFilterSchema(
                field = 'supplier_id',
                value = f.id
            )
        ])

    @classmethod
    def get_by_client(cls, client: ClientModelType) -> List[OrderModelType]:
        return cls.filter([
            ModelFilterSchema(
                field = 'client_id',
                value = client.id
            )
        ])
    
    @classmethod
    def get_fournisseurs_for_client(cls, client: ClientModelType) -> List[SupplierModelType]:
        from model_supplier import SupplierModel
        suppliers_witch_order = SupplierModel.filter([
            ModelFilterSchema(
                format = 'count',
                field = 'orders',
                operator = '!=',
                value = 0
            )
        ], bypass_type_checking= True)

        selected_suppliers: List[SupplierModelType] = []
        for supplier in suppliers_witch_order:
            for o in supplier.orders:
                if o.client.id == client.id:
                    if supplier not in selected_suppliers:
                        selected_suppliers.append(supplier)
                

        return selected_suppliers
    
    @classmethod
    def get_clients_for_fournisseur(cls, f: SupplierModelType) -> List[ClientModelType]:
        from model_client import ClientModel
        clients_with_orders = ClientModel.filter([
            ModelFilterSchema(
                format = 'count',
                field = 'orders',
                operator = '!=',
                value = 0
            )
        ], bypass_type_checking= True)
    
        selected_clients: List[ClientModelType] = []

        for client in clients_with_orders:
            for o in client.orders :
                if o.supplier.id == f.id:
                    if client not in selected_clients:
                        selected_clients.append(client)
                

        return selected_clients