from model_warehouse import *
from model_vehicule import *
from model_compartment import *
from model_batch import *
from model_client import *
from model_supplier import *
from model_type_article import *
from model_article import *
from model_order import *

def reset_all():
    WarehoudeModel.reset_db()
    VehiculeModel.reset_db()
    CompartmentModel.reset_db()
    BatchModel.reset_db()
    TypeArticleModel.reset_db()
    ArticleModel.reset_db()
    ClientModel.reset_db()
    SupplierModel.reset_db()
    OrderModel.reset_db()