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
from algo_tabu import TabuSearch

app = FastAPI()

@app.get("/")
async def ping():
    return {'msg': 'OK'}

## RECUIT SIMULE ###############################################################################
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


@app.post("/multi/recuit")
async def multi_genetic(obj: MultiAPIRecuitInput):
    dataset = {}

    for id_area in obj.areas:
        reset_all()

        Base.Config.PK_MANAGER = PK_MNT_METHOD.MANUAL

        selected_clients = [ c for c in obj.clients if c['area_id'] == id_area]
        selected_clients_ids = [ c['id'] for c in selected_clients]
        # print("\n selected_clients_ids ", selected_clients_ids)
        ClientModel.create_many(selected_clients)
            
        selected_suppliers = [ c for c in obj.suppliers if c['area_id'] == id_area]
        selected_suppliers_ids = [c['id'] for c in selected_suppliers]
        # print("\n selected_suppliers_ids ", selected_suppliers_ids)
        SupplierModel.create_many(selected_suppliers)

        TypeArticleModel.create_many(obj.type_articles)
        ArticleModel.create_many(obj.articles)
        
        selected_orders = [o for o in obj.orders if o['client_id'] in selected_clients_ids and o['supplier_id'] in selected_suppliers_ids]
        OrderModel.create_many(selected_orders)

        selected_warehouses = [ c for c in obj.warehouses if c['area_id'] == id_area]
        selected_warehouses_ids = [ w['id'] for w in selected_warehouses]
        # print("\n selected_warehouses_ids ", selected_warehouses_ids)
        WarehoudeModel.create_many(selected_warehouses)

        selected_vehicules = [ v for v in obj.vehicules if v['warehouse_id'] in selected_warehouses_ids]
        # print("\n selected_vehicules ", selected_vehicules)
        VehiculeModel.create_many(selected_vehicules)

        f = OrderModel.get_fournisseurs()
        c = OrderModel.get_clients()
        d = WarehoudeModel.get_first()
        # print(f"Il y a {len(f)} fourn et {len(c)} clients ")
        # print("Dépot de base : D", d.id)
        random.shuffle(f)
        random.shuffle(c)

        # list_initial = [d] + f + c + [d]
        list_initial = f + c 
        recuit = RecuitSimule(list_initial, obj.algo_params)
        res = recuit.start()
        dataset[id_area] = res
        
    with open("res_multi.json", "w") as file:
        json.dump(dataset, file)
        
    return dataset



## GENETIQUE ###############################################################################
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

@app.post("/multi/genetic")
async def multi_genetic(obj: MultiAPIGeneticInput):
    dataset = {}

    for id_area in obj.areas:
        reset_all()

        Base.Config.PK_MANAGER = PK_MNT_METHOD.MANUAL

        selected_clients = [ c for c in obj.clients if c['area_id'] == id_area]
        selected_clients_ids = [ c['id'] for c in selected_clients]
        # print("\n selected_clients_ids ", selected_clients_ids)
        ClientModel.create_many(selected_clients)
            
        selected_suppliers = [ c for c in obj.suppliers if c['area_id'] == id_area]
        selected_suppliers_ids = [c['id'] for c in selected_suppliers]
        # print("\n selected_suppliers_ids ", selected_suppliers_ids)
        SupplierModel.create_many(selected_suppliers)

        TypeArticleModel.create_many(obj.type_articles)
        ArticleModel.create_many(obj.articles)
        
        selected_orders = [o for o in obj.orders if o['client_id'] in selected_clients_ids and o['supplier_id'] in selected_suppliers_ids]
        OrderModel.create_many(selected_orders)

        selected_warehouses = [ c for c in obj.warehouses if c['area_id'] == id_area]
        selected_warehouses_ids = [ w['id'] for w in selected_warehouses]
        # print("\n selected_warehouses_ids ", selected_warehouses_ids)
        WarehoudeModel.create_many(selected_warehouses)

        selected_vehicules = [ v for v in obj.vehicules if v['warehouse_id'] in selected_warehouses_ids]
        # print("\n selected_vehicules ", selected_vehicules)
        VehiculeModel.create_many(selected_vehicules)

        f = OrderModel.get_fournisseurs()
        c = OrderModel.get_clients()
        d = WarehoudeModel.get_first()
        # print(f"Il y a {len(f)} fourn et {len(c)} clients ")
        # print("Dépot de base : D", d.id)
        random.shuffle(f)
        random.shuffle(c)

        # list_initial = [d] + f + c + [d]
        list_initial = f + c 
        gentic = Genetic(list_initial, obj.algo_params)
        res = gentic.start()
        dataset[id_area] = res
        
    with open("res_multi.json", "w") as file:
        json.dump(dataset, file)
        
    return dataset



## TABOU ###############################################################################
@app.post("/tabu")
async def tabu(obj: APITabuInput):
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
    recuit = TabuSearch(list_initial, obj.algo_params)
    res = recuit.start()
    
    with open("res.json", "w") as file:
        json.dump(res, file)
        
    return res


@app.post("/multi/tabu")
async def multi_tabu(obj: MultiAPITabuInput):
    dataset = {}

    for id_area in obj.areas:
        reset_all()

        Base.Config.PK_MANAGER = PK_MNT_METHOD.MANUAL

        selected_clients = [ c for c in obj.clients if c['area_id'] == id_area]
        selected_clients_ids = [ c['id'] for c in selected_clients]
        # print("\n selected_clients_ids ", selected_clients_ids)
        ClientModel.create_many(selected_clients)
            
        selected_suppliers = [ c for c in obj.suppliers if c['area_id'] == id_area]
        selected_suppliers_ids = [c['id'] for c in selected_suppliers]
        # print("\n selected_suppliers_ids ", selected_suppliers_ids)
        SupplierModel.create_many(selected_suppliers)

        TypeArticleModel.create_many(obj.type_articles)
        ArticleModel.create_many(obj.articles)
        
        selected_orders = [o for o in obj.orders if o['client_id'] in selected_clients_ids and o['supplier_id'] in selected_suppliers_ids]
        OrderModel.create_many(selected_orders)

        selected_warehouses = [ c for c in obj.warehouses if c['area_id'] == id_area]
        selected_warehouses_ids = [ w['id'] for w in selected_warehouses]
        # print("\n selected_warehouses_ids ", selected_warehouses_ids)
        WarehoudeModel.create_many(selected_warehouses)

        selected_vehicules = [ v for v in obj.vehicules if v['warehouse_id'] in selected_warehouses_ids]
        # print("\n selected_vehicules ", selected_vehicules)
        VehiculeModel.create_many(selected_vehicules)

        f = OrderModel.get_fournisseurs()
        c = OrderModel.get_clients()
        d = WarehoudeModel.get_first()
        # print(f"Il y a {len(f)} fourn et {len(c)} clients ")
        # print("Dépot de base : D", d.id)
        random.shuffle(f)
        random.shuffle(c)

        # list_initial = [d] + f + c + [d]
        list_initial = f + c 
        tabu = TabuSearch(list_initial, obj.algo_params)
        res = tabu.start()
        dataset[id_area] = res
        
    with open("res_multi.json", "w") as file:
        json.dump(dataset, file)
        
    return dataset
