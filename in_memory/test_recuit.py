import base_model
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from typing import TypeVar
from schemas.config import ModelFilterSchema, FilterAgregationRuleSchema
from model_warehouse import *
from model_vehicule import *
from model_compartment import *
from model_client import ClientModel
from model_supplier import SupplierModel
from model_article import ArticleModel
from model_type_article import TypeArticleModel
from model_order import OrderModel, OrderSchema

from utils import reset_all
import random
from recuit import RecuitSimule

reset_all()

#### Garage #########################################
w1 = WarehoudeModel({
    'x': 0,
    'y': 0
})
assert w1.name == "D1"
assert w1.id == 1

v1 = VehiculeModel({
    "warehouse_id": w1.id,
    "nb_compartments": 12,
    "size_compartment": 24,
    "cost": 390
})

v2 = VehiculeModel({
    "warehouse_id": w1.id,
    "nb_compartments": 13,
    "size_compartment": 35,
    "cost": 390
})

#### Clients #########################################
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


client4 = ClientModel({
    'x': 146,
    'y': 73
})

client5 = ClientModel({
    'x': 618,
    'y': 7892
})


client6 = ClientModel({
    'x': 2618,
    'y': 4892
})

client7 = ClientModel({
    'x': 12618,
    'y': 782
})
#### Suppliers #########################################
supplier1 = SupplierModel({
    'x': 1,
    'y': 28
})

supplier2 = SupplierModel({
    'x': 32,
    'y': 98
})

supplier3 = SupplierModel({
    'x': 321,
    'y': 938
})

#### Store #############################################
t1 = TypeArticleModel({"name": "Riz"})

art1 = ArticleModel({
    'name': 'Rizière',
    'type_article_id': t1.id
})


#### Orders #############################################
order1 = OrderModel({
    'client_id': client1.id,
    'supplier_id': supplier1.id,
    'article_id': art1.id,
    'qty_fixed': 20
})

order2 = OrderModel({
    'client_id': client2.id,
    'supplier_id': supplier1.id,
    'article_id': art1.id,
    'qty_fixed': 14
})

order3 = OrderModel({
    'client_id': client3.id,
    'supplier_id': supplier1.id,
    'article_id': art1.id,
    'qty_fixed': 35
})

order4 = OrderModel({
    'client_id': client4.id,
    'supplier_id': supplier2.id,
    'article_id': art1.id,
    'qty_fixed': 39
})

order5 = OrderModel({
    'client_id': client5.id,
    'supplier_id': supplier2.id,
    'article_id': art1.id,
    'qty_fixed': 56
})

order6 = OrderModel({
    'client_id': client6.id,
    'supplier_id': supplier2.id,
    'article_id': art1.id,
    'qty_fixed': 96
})

order7 = OrderModel({
    'client_id': client7.id,
    'supplier_id': supplier3.id,
    'article_id': art1.id,
    'qty_fixed': 96
})



f = OrderModel.get_fournisseurs()
c = OrderModel.get_clients()
d = WarehoudeModel.get(1)
print(f"Il y a {len(f)} fourn et {len(c)} clients ")

random.shuffle(f)
random.shuffle(c)

# list_initial = [d] + f + c + [d]
list_initial = f + c 
recuit = RecuitSimule(list_initial)
res = recuit.start()

vehicules = {}
for v in VehiculeModel.list_all():
    vehicules[v.name] = {}
    vehicules[v.name].update({
        field: getattr(v, field) for field in VehiculeSchema.__fields__
    })
    vehicules[v.name]['compartments'] = {}

    v_qty_holded = 0
    for comp in v.compartments:
        vehicules[v.name]['compartments'][comp.id] = {}
        vehicules[v.name]['compartments'][comp.id].update({
            field: getattr(comp, field) for field in CompartmentSchema.__fields__
        })
        vehicules[v.name]['compartments'][comp.id]['total_batches'] = len(comp.batches)
        vehicules[v.name]['compartments'][comp.id]['filled_batches'] = len([ c for c in comp.batches if c.is_active is True])
        vehicules[v.name]['compartments'][comp.id]['holded'] = sum([ c.qty_holded for c in comp.batches])

        for h in comp.batches:
            v_qty_holded += h.qty_holded

    vehicules[v.name]['holded'] = v_qty_holded

res['vehicules'] = vehicules
res['orders'] = {}
OrderSchema.__fields__.update({'qty': 91})
for order in OrderModel.list_all():
    res['orders'][order.id] = {
        field: getattr(order, field) for field in OrderSchema.__fields__
    }
import json
with open("res.json", 'w') as  file:
    json.dump(res, file)
# print(jsonable_encoder(res))

