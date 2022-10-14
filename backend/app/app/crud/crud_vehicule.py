from typing import List, Tuple
from app.db.session import SessionLocal

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.vehicule import Vehicule
from app.schemas.vehicule import VehiculeCreate, VehiculeUpdate
from app import models, crud, schemas

from app.db.session import get_db
db = get_db().send(None)

class CRUDItem(CRUDBase[Vehicule, VehiculeCreate, VehiculeUpdate]):
    # def get_all(self) -> List[Vehicule]:
    #     return super().get_all(db)

    def get_by_name(self, name: str, db: Session = db) -> Vehicule:
        return db.query(self.model).filter(self.model.name == name).first()

    def create(self, obj_in: VehiculeCreate, db: Session = db) -> Vehicule:
        v = super().create(obj_in= obj_in, db= db)
        v.name = f'V{v.id}'
        db.add(v)
        db.commit()
        db.refresh(v)
        return v

    def can_hold(self, vehicule: models.Vehicule, produit: models.Produit, qty: int) -> int:
        dispo1 = self.get_available_space_in_free_compartments(vehicule)
        dispo2 = self.get_available_space_for_produit(vehicule, produit)

        qty_holdable = dispo1 + dispo2 
        # #printf"Dispo ({dispo1} + {dispo2}) = {qty_holdable} ")
        return qty_holdable
        
    def hold(self, vehicule: models.Vehicule, order: models.Commande) -> int:
        """
            - On empack d'abord dans les compartiments contenant des produits similaires
            - Si la commande n'est totalement rentrée dans les précedents compartiments, 
            on en crée de nouveau autant de fois que le véhicule possède des compartiments en réserve

            On rétourne la quantité de commande qu'il reste à empacketer
        """
        holded = False 
        max_vehicule_qty = vehicule.nb_compartment * vehicule.size_compartment
        qty_holded_by_vehicule = self.get_used_space_in_busy_compartments(vehicule)
        qty_holded_for_order = 0
        for comp in vehicule.compartiments:
            # #print"Found compartments")
            if qty_holded_by_vehicule == order.qty :
                break
            
            elif qty_holded_by_vehicule > max_vehicule_qty :
                raise Exception("Le véhicule a accueillit plus de produits qu'il ne peut supporter")
            
            elif len(comp.holded_orders) != 0 :
                #printf" {comp.holded_orders[0].commande} à {comp.holded_orders[0].commande.id} ")
                size_free = self.get_free_space_in_compartment(comp, comp.holded_orders[0].commande.produit, order.produit)
                # #printf"Le Compart {comp.id} a {size_free} dispo ")
                qty_to_hold = min(size_free, order.qty )
                if qty_to_hold > 0:
                    self.add_order_to_compartment(comp, order, qty_to_hold)
                    qty_holded_for_order += qty_to_hold
                    qty_holded_by_vehicule += qty_to_hold
                    #printf"V{vehicule.id}, comp {comp.id} a pu retenir {qty_to_hold} supplémentaires pour la order {order.id} ")
        index = 0
        size_free = vehicule.size_compartment # Car on rempli désormais les compartiments vides. 
        # #printf"V{vehicule.id} Qté empaquetable : {qty_to_hold} ")
        qty_to_hold = min(size_free, order.qty )
        while qty_holded_for_order < order.qty and (qty_holded_by_vehicule + qty_to_hold) <= max_vehicule_qty and vehicule.nb_compartment > len(crud.vehicule.get_compartiments(vehicule.id)) :
            qty_to_hold = min(size_free, order.qty )
            if qty_to_hold > 0:
                comp = self.create_compartment(vehicule)                
                self.add_order_to_compartment(comp, order, qty_to_hold)
                qty_holded_for_order += qty_to_hold
                qty_holded_by_vehicule += qty_to_hold
                index += 1
            #printf"Itération {index} : v.nb_comp = {len(crud.vehicule.get_compartiments(vehicule.id))}/{vehicule.nb_compartment}, order_holded = {qty_holded_for_order}/{order.qty_fixed}, total_in_vehicule = {qty_holded_by_vehicule}/{max_vehicule_qty} with_step = {qty_to_hold}/{vehicule.size_compartment} ")
        # #printf"Résumé: iter={index}, qty_to_hold={qty_to_hold}, qty_holded_by_vehicule={qty_holded_by_vehicule}, qty_holded_for_order={qty_holded_for_order} ")
        return qty_holded_for_order

    def add_order_to_compartment(self, compartment: models.Compartiment, order: models.Commande, qty_to_hold: int):
        h = models.HoldedOrder(commande_id = order.id, compartiment_id = compartment.id, qty_holded = qty_to_hold)
        db.add(h)
        db.commit()
        crud.commande.decrease_qty(db, order, qty_to_hold)
       
    def add_node_to_route(self, vehicule: models.Vehicule, node: schemas.Node, db: Session = db ) -> bool:
        # TODO: This function is the problem

        #printf"AJOUT de {vehicule.name} au noeud {node.name} ")
        # vehicule = crud.vehicule.get(vehicule.id, db= db)
        # current_route = vehicule.trajet
        # compartiments = vehicule.compartiments.copy()
        # if node.json() not in current_route :
        #     # raise Exception(f"Le noeud véhicule {vehicule.id} est déjà passé par le noeud {node}")
        #     # #printf"\n Le noeud véhicule {vehicule.id} est déjà passé par le noeud {node}")
        # # else:
        #     current_route.append(node.json())
        #     vehicule.trajet = current_route
        #     local_object = db.merge(vehicule)
        #     local_object.compartiments = compartiments
        #     db.add(local_object)
        #     # db.add(vehicule)
        #     db.commit()
        #     #print"Ajout au trajet ", compartiments)
        #     for c in compartiments:
        #         # local_comp = db.merge(c)
        #         # local_comp.vehicule_id = vehicule.id
        #         # local_comp.vehicule = vehicule
        #         # db.add(local_comp)
        #         #printdb.execute(f"UPDATE compartiment SET vehicule_id={vehicule.id} WHERE compartiment.id = {c.id} "))
        #         db.commit()
        #     return True
        return False

    def get_compartiments(self, vehicule_id: int) -> int:
        return crud.vehicule.get(vehicule_id).compartiments
        
    def get_commandes(self, vehicule: models.Vehicule) -> List[models.Commande]:
        commandes = []
        for comp in vehicule.holded_orders :
            commandes.append(comp.commande)
        return commandes

    def get_commandes_in_compartiment(self, compartiment: models.Compartiment) -> List[models.Commande]:
        return db.query(models.HoldedOrder).filter(models.HoldedOrder.compartiment_id == compartiment.id).all()

    def get_free_space_in_compartment(self, compartiment: models.Compartiment, produit_1: models.Produit, produit_2: models.Produit) -> int:
        size_used = sum([ holded.qty_holded for holded in compartiment.holded_orders if holded.is_active == True ])
        if size_used != 0:
            if not crud.produit.are_produits_similar(produit_1, produit_2) :
                return 0
        return compartiment.vehicule.size_compartment - size_used

    def get_available_space_for_produit(self, vehicule: models.Vehicule, produit: models.Produit):
        """
        Espace disponible dans les compartiments où il y déjà un --MÊME-- popduit similaire TODO: même poduit ou du même type
        """
        # Method 1

        # qty_available = 0
        # for index, comp in enumerate(vehicule.compartiments):
        #     for holded_order in comp.holded_orders :
        #         if holded_order.commande.produit_id == produit.id :
        #             qty_available += vehicule.size_compartment - holded_order.qty_holded
        #             #printf"Compartiment {index}: {holded_order.qty_holded} / {vehicule.size_compartment} --- dispo = {qty_available} ")
        # return qty_available

        # Method 2
        return (len(vehicule.compartiments) * vehicule.size_compartment) - self.get_used_space_by_produit(vehicule, produit)

    def get_used_space_by_produit(self, vehicule: models.Vehicule, produit: models.Produit):
        """
        Espace disponible dans les compartiments où il y déjà un --MÊME-- popduit similaire TODO: même poduit ou du même type
        """
        qty_used = 0
        for index, comp in enumerate(vehicule.compartiments):
            for holded_order in comp.holded_orders :
                if holded_order.commande.produit_id == produit.id :
                    qty_used +=  holded_order.qty_holded
                    # #printf"Produit trouvé dans comp {index} : {holded_order.qty_holded} ")
        return qty_used
    
    def get_used_space_in_busy_compartments(self, vehicule: models.Vehicule):
        """
        Espace disponible dans les compartiments où il y déjà un --MÊME-- popduit similaire TODO: même poduit ou du même type
        """
        _v = crud.vehicule.get(id= vehicule.id)
        qty_used = 0
        for index, comp in enumerate(_v.compartiments):
            for holded_order in comp.holded_orders :
                if holded_order.is_active:
                    qty_used +=  holded_order.qty_holded
                # #printf"Compartiment {index} : {holded_order.qty_holded} ")
        return qty_used

    def get_available_space_in_free_compartments(self, vehicule: models.Vehicule) -> int:
        # Ne prend pas en compte les restangoglos dans les compartements à moitié plein
        _v = crud.vehicule.get(vehicule.id)
        nb_remaining_compartments = _v.nb_compartment - len(_v.compartiments)
        # #printf"Space in free comps : (holded_comp = {len(vehicule.compartiments)}, total_comp = {vehicule.nb_compartment} ) ")
        # #print[i for i in vehicule.compartiments])
        return nb_remaining_compartments * _v.size_compartment

    def create_compartment(self, vehicule: models.Vehicule) -> models.Compartiment:
        # c = models.Compartiment(vehicule_id = vehicule.id)
        # c.vehicule_id = vehicule.id

        # db2 = db
        # db2.add(c)
        # db2.commit()
        # db2.refresh(c)
        # pk = db.query(models.Compartiment).filter(models.Compartiment.id == c.id).first().vehicule_id
        obj_in = schemas.CompartimentCreate(vehicule_id = vehicule.id)
        c = crud.compartiment.create(obj_in= obj_in, db = db)

        
        # # #printc.vehicule)
        # try:
        #     c.vehicule = vehicule
        # except:
        #     c.vehicule = local_obj
        #     pass
        # # finally:

        ########""
        # local_comp = db.merge(c)
        # local_vehicule = db.merge(vehicule)
        # local_vehicule.compartiments.append(local_comp)
        # db.add(local_vehicule)
        # db.commit()
        # db.refresh(local_vehicule)
        ##########


        # c.vehicule = db.merge(vehicule)
        # c.vehicule_id = vehicule.id
        # db.add(c)
        # db.commit()
        # db.refresh(c)

        # db.execute(f"UPDATE compartiment SET vehicule_id={vehicule.id} WHERE compartiment.id = {c.id} ")
        
        # db.refresh(local_comp)
        # #printf"Create compartment {local_comp.id} for V{local_vehicule.id}, {local_comp.vehicule_id} of {local_comp.vehicule} ")
        return c
        return local_comp

    def get_client_holded_orders_in_compartiment(self, compartiment: models.Compartiment, client: models.Client) -> List[models.HoldedOrder]:
        # for h in compartiment.holded_orders :
        #     if h.commande.client_id == client.id :
        #         l.append(comm)

        # Si une holded_order est inactive c'est qu'elle est déjà déchargée chez un client
        return [ h for h in compartiment.holded_orders if h.commande.client_id == client.id and h.is_active == True ] 

    def get_client_holded_orders_in_vehicule(self, vehicule: models.Vehicule, client: models.Client) -> List[models.HoldedOrder]:
        orders = []
        # #printf"\nGetting comparments in {vehicule.name} ")
        # db.query(models.Compartiment).filter
        for comp in vehicule.compartiments :
        # for comp in crud.compartiment.get_all():
            # #printf"Compp {comp.id} ")
            # #printf"Compartment {comp.id} of {comp.vehicule_id}  ")
            orders.extend(self.get_client_holded_orders_in_compartiment(comp, client))
        return orders


    # def get_active_compartments(self, vehicule: models.Vehicule) -> List[models.Compartiment]:
    #     return [ comp for comp in vehicule.compartiments if comp.is_active == True ]

    def deactivate_holded_order(self, holded_order: models.HoldedOrder) -> models.HoldedOrder:
        holded_order.is_active = False
        local_obj = db.merge(holded_order)
        db.add(local_obj)
        db.commit()
        db.refresh(local_obj)
        return local_obj

    def remove_holded_order(self, holded_order: models.HoldedOrder, db: Session = db) -> models.HoldedOrder:
        db.delete(holded_order)
        db.commit()
        
        return holded_order

vehicule = CRUDItem(Vehicule)
