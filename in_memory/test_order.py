import base_model
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import TypeVar
from schemas.config import ModelFilterSchema, FilterAgregationRuleSchema
from model_type_article import *
from model_article import *
from model_client import *
from model_supplier import *
from model_order import *

ClientModel.reset_db()
SupplierModel.reset_db()
OrderModel.reset_db()
TypeArticleModel.reset_db()
ArticleModel.reset_db()

client1 = ClientModel({
    'x': 1,
    'y': 28
})


client2 = ClientModel({
    'x': 56,
    'y': 31
})

client3 = ClientModel({
    'x': 356,
    'y': 311
})

supplier1 = SupplierModel({
    'x': 1,
    'y': 28
})

supplier2 = SupplierModel({
    'x': 32,
    'y': 98
})

t1 = TypeArticleModel({"name": "Riz"})

art1 = ArticleModel({
    'name': 'Rizière',
    'type_article_id': t1.id
})

order1 = OrderModel({
    'client_id': client1.id,
    'supplier_id': supplier1.id,
    'article_id': art1.id,
    'qty': 20
})

order2 = OrderModel({
    'client_id': client2.id,
    'supplier_id': supplier1.id,
    'article_id': art1.id,
    'qty': 20
})

order3 = OrderModel({
    'client_id': client3.id,
    'supplier_id': supplier2.id,
    'article_id': art1.id,
    'qty': 20
})

assert OrderModel.must_deliver_client(f= supplier1, client= client1) == True
assert OrderModel.must_deliver_client(f= supplier1, client= client2) == True
assert OrderModel.must_deliver_client(f= supplier2, client= client3) == True

assert supplier1 in OrderModel.get_fournisseurs()
assert supplier2 in OrderModel.get_fournisseurs()

assert client1 in OrderModel.get_clients()
assert client3 in OrderModel.get_clients()

assert supplier1 in OrderModel.get_fournisseurs_for_client(client= client1)
assert supplier2 not in OrderModel.get_fournisseurs_for_client(client= client1)
assert supplier2 in OrderModel.get_fournisseurs_for_client(client= client3)
assert supplier1 not in OrderModel.get_fournisseurs_for_client(client= client3)

assert client1 in OrderModel.get_clients_for_fournisseur(f= supplier1)
assert client3 not in OrderModel.get_clients_for_fournisseur(f= supplier1)

assert order1.qty_flex is order1.datum.qty
assert order1.article is art1
assert order1.client is client1
assert order1.supplier is supplier1

try:
    OrderModel({
        'client_id': 902816982,
        'supplier_id': supplier1.id,
        'article_id': art1.id,
        'qty': 20
    })
except:
    pass
else:
    raise AssertionError("Client_id 902816982 must be inexistent")
