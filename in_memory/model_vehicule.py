from typing import TypeVar, Dict, Any, List
from pydantic import BaseModel
from base_model import Base
from _types import *
from model_compartment import CompartmentModel
from model_article import ArticleModel
from model_order import OrderModel
from model_batch import BatchModel
from schemas.config import *

class VehiculeSchema(BaseModel):
    warehouse_id: int
    speed: float = 60 # Km/s
    nb_compartments: int
    size_compartment: int
    cost: int

class VehiculeModel(Base[VehiculeModelType, VehiculeSchema]):
    SCHEMA = VehiculeSchema
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}

    def __init__(self, datum: Dict[str, Any]):
        from  model_warehouse import WarehoudeModel
        from model_compartment import CompartmentModel

        self.warehouse: WarehoudeModel
        self.compartments: list[CompartmentModel] = []
        super().__init__(datum)


    def _register_relations(self):
        from  model_warehouse import WarehoudeModel
        from model_compartment import CompartmentModel

        _warehouse = WarehoudeModel.get(self.datum.warehouse_id)
        self.warehouse = _warehouse
        self.warehouse.register_vehicule(self)
        
        for i in range(self.datum.nb_compartments):
            _comp = CompartmentModel({
                'vehicule_id': self.id,
                'size': self.datum.size_compartment
            })

    def register_compartment(self, compartment):
        self.compartments.append(compartment)
    @staticmethod
    def prefix():
        return 'V'
    
    @property
    def name(self) -> str:
        return f"{self.prefix()}{self.id}"
    
    @classmethod
    def get_by_name(cls, name: str) -> VehiculeModelType:
        pk = name.split(cls.prefix())[-1]
        try:
            pk = int(pk)
        except:
            raise AssertionError(f"VehiculeModel name = {name} is not splitable to get vehicle id")
        
        return VehiculeModel.get(pk)

    @classmethod
    def can_hold(cls, vehicule: VehiculeModelType, produit: ArticleModel, qty: int) -> int:
        dispo1 = cls.get_available_space_in_free_compartments(vehicule)
        dispo2 = cls.get_available_space_for_produit(vehicule, produit)

        qty_holdable = dispo1 + dispo2 
        # #printf"Dispo ({dispo1} + {dispo2}) = {qty_holdable} ")
        return qty_holdable
        
    @classmethod
    def hold(cls, vehicule: VehiculeModelType, order: OrderModel) -> int:
        """
            - On empack d'abord dans les compartments contenant des produits similaires
            - Si la commande n'est totalement rentrée dans les précedents compartments, 
            on en crée de nouveau autant de fois que le véhicule possède des compartments en réserve

            On rétourne la quantité de commande qu'il reste à empacketer
        """
        holded = False 
        max_vehicule_qty = vehicule.nb_compartments * vehicule.size_compartment
        qty_holded_by_vehicule = cls.get_used_space_in_busy_compartments(vehicule)
        qty_holded_for_order = 0
        for comp in vehicule.compartments:
            # #print"Found compartments")
            if qty_holded_by_vehicule == order.qty :
                print("ONE")
                break
            
            elif qty_holded_by_vehicule > max_vehicule_qty :
                raise Exception("Le véhicule a accueillit plus de produits qu'il ne peut supporter")
            
            # elif  db.query(HoldedOrder).count(HoldedOrder.compartiment_id == comp.id) != 0 : #len(comp.holded_orders) != 0 :
            elif len(BatchModel.filter([
                ModelFilterSchema(
                    field= 'compartment_id',
                    value= comp.id
                )
            ])) != 0:
                print("TWO")
                #printf" {comp.holded_orders[0].commande} à {comp.holded_orders[0].commande.id} ")
                size_free = cls.get_free_space_in_compartment(comp, comp.batches[0].order.article, order.article)
                # #printf"Le Compart {comp.id} a {size_free} dispo ")
                qty_to_hold = min(size_free, order.qty )
                if qty_to_hold > 0:
                    cls.add_order_to_compartment(comp, order, qty_to_hold)
                    qty_holded_for_order += qty_to_hold
                    qty_holded_by_vehicule += qty_to_hold
                    #printf"V{vehicule.id}, comp {comp.id} a pu retenir {qty_to_hold} supplémentaires pour la order {order.id} ")
        index = 0
        size_free = vehicule.size_compartment # Car on rempli désormais les compartments vides. 
        # #printf"V{vehicule.id} Qté empaquetable : {qty_to_hold} ")
        qty_to_hold = min(size_free, order.qty )
        print(f"\t qty_to_hold ", qty_to_hold)
        print(f"\t qty_holded_for_order({qty_holded_for_order}) < order.qty({order.qty}) <==>  {qty_holded_for_order < order.qty}")
        print(f"\t (qty_holded_by_vehicule({qty_holded_by_vehicule}) + qty_to_hold({qty_to_hold}))({qty_holded_by_vehicule + qty_to_hold}) <= max_vehicule_qty({max_vehicule_qty}) <==>  {(qty_holded_by_vehicule + qty_to_hold) <= max_vehicule_qty}")
        print(f"\t vehicule.nb_compartments({vehicule.nb_compartments}) >= len(vehicule.compartments)({len(vehicule.compartments)}) <==> {vehicule.nb_compartments >= len(vehicule.compartments)} ")
        while qty_holded_for_order < order.qty and (qty_holded_by_vehicule + qty_to_hold) <= max_vehicule_qty and vehicule.nb_compartments >= len(vehicule.compartments) :
            qty_to_hold = min(size_free, order.qty )
            if qty_to_hold > 0:
                comp = cls.create_compartment(vehicule)                
                cls.add_order_to_compartment(comp, order, qty_to_hold)
                qty_holded_for_order += qty_to_hold
                qty_holded_by_vehicule += qty_to_hold
                index += 1
            #printf"Itération {index} : v.nb_comp = {len(crud.vehicule.get_compartiments(vehicule.id))}/{vehicule.nb_compartments}, order_holded = {qty_holded_for_order}/{order.qty_fixed}, total_in_vehicule = {qty_holded_by_vehicule}/{max_vehicule_qty} with_step = {qty_to_hold}/{vehicule.size_compartment} ")
        # #printf"Résumé: iter={index}, qty_to_hold={qty_to_hold}, qty_holded_by_vehicule={qty_holded_by_vehicule}, qty_holded_for_order={qty_holded_for_order} ")
        return qty_holded_for_order

    @classmethod
    def add_order_to_compartment(cls, compartment: CompartmentModel, order: OrderModel, qty_to_hold: int):
        # h = models.HoldedOrder(commande_id = order.id, compartiment_id = compartment.id, qty_holded = qty_to_hold)
        BatchModel.create({
            'order_id': order.id,
            'compartment_id': compartment.id,
            'qty_holded': qty_to_hold
        })
        OrderModel.decrease_qty(order, qty_to_hold)
        
    @classmethod
    def add_node_to_route(cls, vehicule: VehiculeModelType, node: Node) -> bool:
        # TODO: This function is the problem

        return False

    def get_compartiments(self, vehicule_id: int) -> List[CompartmentModel]:
        # return crud.vehicule.get(vehicule_id).compartments
        return VehiculeModel.get(vehicule_id).compartments
    
    def get_commandes_in_compartiment(self, compartiment: CompartmentModel) -> List[BatchModel]:
        return BatchModel.filter([
            ModelFilterSchema(
                field= 'compartment_id',
                value=compartiment.id
            )
        ])
        # return db.query(models.HoldedOrder).filter(models.HoldedOrder.compartiment_id == compartiment.id).all()

    @classmethod
    def get_free_space_in_compartment(cls, compartiment: CompartmentModel, produit_1: ArticleModel, produit_2: ArticleModel) -> int:
        size_used = sum([ batch.qty_holded for batch in compartiment.batches if batch.is_active == True ])
        if size_used != 0:
            if not ArticleModel.are_produits_similar(produit_1, produit_2) :
                return 0
        return compartiment.vehicule.size_compartment - size_used

    @classmethod
    def get_available_space_for_produit(cls, vehicule: VehiculeModelType, produit: ArticleModel) -> int:
        """
        Espace disponible dans les compartments où il y déjà un --MÊME-- popduit similaire TODO: même poduit ou du même type
        """
        # Method 1

        # qty_available = 0
        # for index, comp in enumerate(vehicule.compartments):
        #     for holded_order in comp.holded_orders :
        #         if holded_order.commande.produit_id == article.id :
        #             qty_available += vehicule.size_compartment - holded_order.qty_holded
        #             #printf"Compartiment {index}: {holded_order.qty_holded} / {vehicule.size_compartment} --- dispo = {qty_available} ")
        # return qty_available

        # Method 2
        return (len(vehicule.compartments) * vehicule.size_compartment) - cls.get_used_space_by_produit(vehicule, produit)

    @classmethod
    def get_used_space_by_produit(cls, vehicule: VehiculeModelType, produit: ArticleModel) -> int:
        """
        Espace disponible dans les compartments où il y déjà un --MÊME-- popduit similaire TODO: même poduit ou du même type
        """
        qty_used = 0

        for index, comp in enumerate(vehicule.compartments):
            for batch in comp.batches :
                if batch.order.article_id == produit.id :
                    qty_used +=  batch.qty_holded
                    # #printf"Produit trouvé dans comp {index} : {holded_order.qty_holded} ")
        return qty_used
    
    @classmethod
    def get_used_space_in_busy_compartments(cls, vehicule: VehiculeModelType) -> int:
        """
        Espace disponible dans les compartments où il y déjà un --MÊME-- popduit similaire TODO: même poduit ou du même type
        """
        _v: VehiculeModel = VehiculeModel.get(vehicule.id)
        qty_used = 0

        for index, comp in enumerate(_v.compartments):
            for batch in comp.batches :
                if batch.is_active:
                    qty_used +=  batch.qty_holded
                # #printf"Compartiment {index} : {holded_order.qty_holded} ")
        return qty_used

    @classmethod
    def get_available_space_in_free_compartments(cls, vehicule: VehiculeModelType) -> int:
        # Ne prend pas en compte les restangoglos dans les compartements à moitié plein
        _v: VehiculeModel = VehiculeModel.get(vehicule.id)
        nb_remaining_compartments: int = _v.nb_compartments - len(_v.compartments)
        # #printf"Space in free comps : (holded_comp = {len(vehicule.compartments)}, total_comp = {vehicule.nb_compartments} ) ")
        # #print[i for i in vehicule.compartments])
        return nb_remaining_compartments * _v.size_compartment

    @classmethod
    def create_compartment(cls, vehicule: VehiculeModelType) -> CompartmentModel:
        # c = crud.compartiment.create(obj_in= obj_in, db = db)
        return CompartmentModel({
            'vehicule_id': vehicule.id
        })
    
    @classmethod
    def get_client_holded_orders_in_compartiment(cls, compartiment: CompartmentModel, client: ClientModelType) -> List[BatchModel]:
        
        results: List[BatchModel] = []
        for batch in BatchModel.list_all():
            if batch.is_active is True and batch.order.client.id == client.id:
                results.append(batch)

        return results
        # return db.query(models.HoldedOrder).filter(
        #     models.HoldedOrder.commande_id == client.id,
        #     models.HoldedOrder.is_active == True
        # ).all()
    
    @classmethod
    def get_client_holded_orders_in_vehicule(cls, vehicule: VehiculeModelType, client: ClientModelType) -> List[BatchModel]:
        orders = []
        # #printf"\nGetting comparments in {vehicule.name} ")
        # db.query(models.Compartiment).filter
        compos = CompartmentModel.filter([
            ModelFilterSchema(
                field = 'vehicule_id',
                value = vehicule.id
            )
        ])
        # compos = db.query(models.Compartiment).filter(models.Compartiment.vehicule_id == vehicule.id).all()
        # print(f"V{vehicule.id} -> Comps: {len(compos)} ")
        for comp in compos :
            cc = cls.get_client_holded_orders_in_compartiment(comp, client)
            orders.extend(cc)
        print(orders)
        return orders


    # def get_active_compartments(self, vehicule: models.Vehicule) -> List[models.Compartiment]:
    #     return [ comp for comp in vehicule.compartments if comp.is_active == True ]

    @classmethod
    def deactivate_holded_order(cls, batch: BatchModel) -> BatchModel:
        batch.is_active = False
        
        return batch

    @classmethod
    def remove_holded_order(self, batch: BatchModel) -> BatchModel:
        BatchModel.delete(batch.id)
        
        return batch
