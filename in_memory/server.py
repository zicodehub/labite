import random, json
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
from schemas.config import *
from recuit import RecuitSimule
from algo_genetic import Genetic

app = FastAPI()

@app.get("/")
async def ping():
    return {'msg': 'OK'}

@app.post("/recuit")
async def recuit(obj: APIRecuitInput):
    reset_all()

    Base.Config.PK_MANAGER = PK_MNT_METHOD.MANUAL

    ClientModel.create_many(obj.clients)
        
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
    recuit = RecuitSimule(list_initial, obj.algo_params)
    res = recuit.start()
    
    with open("res.json", "w") as file:
        json.dump(res, file)
        
    return res


@app.post("/genetic")
async def recuit(obj: APIGeneticInput):
    reset_all()

    Base.Config.PK_MANAGER = PK_MNT_METHOD.MANUAL

    ClientModel.create_many(obj.clients)
        
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
    gentic = Genetic(list_initial, obj.algo_params)
    res = gentic.start()
    with open("res.json", "w") as file:
        json.dump(res, file)

    return res