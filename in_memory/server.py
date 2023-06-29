import random
from fastapi import FastAPI, Body
from pydantic import BaseModel
from _types import *
from utils import reset_all
from model_warehouse import *
from model_vehicule import *
from model_compartment import *
from model_type_article import *
from model_article import *
from model_client import *
from model_supplier import *
from model_order import *
from base_model import Base
from schemas.config import PK_MNT_METHOD
from recuit import RecuitSimule
from algo_genetic import Genetic

class APIInput(BaseModel):
    clients: Any
    suppliers: List
    type_articles: List
    articles: List
    orders: List
    warehouses: List
    vehicules: List

app = FastAPI()

@app.post("/recuit")
async def recuit(obj: APIInput):
    print(obj)
    reset_all()

    Base.Config.PK_MANAGER = PK_MNT_METHOD.MANUAL

    ClientModel.create_many(obj.clients)
    print("\n\n CLIENTS ")
    for i in ClientModel.list_all():
        print(i)
        
    SupplierModel.create_many(obj.suppliers)
    TypeArticleModel.create_many(obj.type_articles)
    ArticleModel.create_many(obj.articles)
    OrderModel.create_many(obj.orders)
    WarehoudeModel.create_many(obj.warehouses)
    VehiculeModel.create_many(obj.vehicules)

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
    return res


@app.post("/genetic")
async def recuit(obj: APIInput):
    print(obj)
    reset_all()

    Base.Config.PK_MANAGER = PK_MNT_METHOD.MANUAL

    ClientModel.create_many(obj.clients)
    print("\n\n CLIENTS ")
    for i in ClientModel.list_all():
        print(i)
        
    SupplierModel.create_many(obj.suppliers)
    TypeArticleModel.create_many(obj.type_articles)
    ArticleModel.create_many(obj.articles)
    OrderModel.create_many(obj.orders)
    WarehoudeModel.create_many(obj.warehouses)
    VehiculeModel.create_many(obj.vehicules)

    f = OrderModel.get_fournisseurs()
    c = OrderModel.get_clients()
    d = WarehoudeModel.get(1)
    print(f"Il y a {len(f)} fourn et {len(c)} clients ")
    print("\t ALGO GENETIC ")

    random.shuffle(f)
    random.shuffle(c)

    # list_initial = [d] + f + c + [d]
    list_initial = f + c 
    gentic = Genetic(list_initial)
    res = gentic.start()
    return res
    return {}