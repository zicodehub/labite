from typing import List, Tuple
from app.db.session import SessionLocal

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.vehicule import Vehicule
from app.schemas.vehicule import VehiculeCreate, VehiculeUpdate
from app import models, crud, schemas

db = SessionLocal()

class CRUDItem(CRUDBase[Vehicule, VehiculeCreate, VehiculeUpdate]):
    def get_all(self) -> List[Vehicule]:
        return super().get_all(db)
    def can_hold(self, vehicule: models.Vehicule, produit: models.Produit, qty: int) -> int:
        dispo1 = self.get_available_space_in_free_compartments(vehicule)
        dispo2 = self.get_available_space_for_produit(vehicule, produit)

        qty_holdable = dispo1 + dispo2 
        # print(f"Dispo ({dispo1} + {dispo2}) = {qty_holdable} ")
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
            if qty_holded_by_vehicule == order.qty :
                break
            
            elif qty_holded_by_vehicule > max_vehicule_qty :
                raise Exception("Le véhicule a accueillit plus de produits qu'il ne peut supporter")
            
            elif len(comp.holded_orders) != 0 and comp.holded_orders[0].commande.produit_id == order.produit_id :
                size_free = self.get_free_space_in_compartment(comp)
                # print(f"Le Compart {comp.id} a {size_free} dispo ")
                if size_free > 0:
                    qty_to_hold = min(size_free, order.qty )
                    self.add_order_to_compartment(comp, order, qty_to_hold)
                    qty_holded_for_order += qty_to_hold
                    qty_holded_by_vehicule += qty_to_hold
                    print(f"V{vehicule.id}, comp {comp.id} a pu retenir {qty_to_hold} supplémentaires pour la order {order.id} ")
        index = 0
        size_free = vehicule.size_compartment # Car on rempli désormais les compartiments vides. 
        # print(f"V{vehicule.id} Qté empaquetable : {qty_to_hold} ")
        qty_to_hold = min(size_free, order.qty )
        while qty_holded_for_order < order.qty and (qty_holded_by_vehicule + qty_to_hold) <= max_vehicule_qty and vehicule.nb_compartment > len(crud.vehicule.get_compartiments(vehicule.id)) :
            qty_to_hold = min(size_free, order.qty )
            comp = self.create_compartment(vehicule)                
            self.add_order_to_compartment(comp, order, qty_to_hold)
            qty_holded_for_order += qty_to_hold
            qty_holded_by_vehicule += qty_to_hold
            print(f"Itération {index} : v.nb_comp = {len(crud.vehicule.get_compartiments(vehicule.id))}/{vehicule.nb_compartment}, order_holded = {qty_holded_for_order}/{order.qty_fixed}, total_in_vehicule = {qty_holded_by_vehicule}/{max_vehicule_qty} with_step = {qty_to_hold}/{vehicule.size_compartment} ")
            index += 1

        return qty_holded_for_order

    def add_order_to_compartment(self, compartment: models.Compartiment, order: models.Commande, qty_to_hold: int):
        h = models.HoldedOrder(commande_id = order.id, compartiment_id = compartment.id, qty_holded = qty_to_hold)
        db.add(h)
        db.commit()
        crud.commande.decrease_qty(db, order, qty_to_hold)
        # db.refresh(vehicule)

    def add_node_to_route(self, vehicule: models.Vehicule, node: schemas.Node) -> bool:
        current_route = vehicule.trajet
        if node.json() in current_route :
            # raise Exception(f"Le noeud véhicule {vehicule.id} est déjà passé par le noeud {node}")
            print(f"\n Le noeud véhicule {vehicule.id} est déjà passé par le noeud {node}")
        else:
            print("Ajout au trajet")
            current_route.append(node.json())
            local_object = db.merge(vehicule)
            db.add(local_object)
            db.commit()

    def get_compartiments(self, vehicule_id: int) -> int:
        return crud.vehicule.get(vehicule_id).compartiments
        
    def get_commandes(self, vehicule: models.Vehicule) -> List[models.Commande]:
        commandes = []
        for comp in vehicule.holded_orders :
            commandes.append(comp.commande)
        return commandes

    def get_commandes_in_compartiment(self, compartiment: models.Compartiment) -> List[models.Commande]:
        return db.query(models.HoldedOrder).filter(models.HoldedOrder.compartiment_id == compartiment.id).all()

    def get_free_space_in_compartment(self, compartiment: models.Compartiment) -> int:
        size_used = sum([ holded.qty_holded for holded in compartiment.holded_orders ])
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
        #             print(f"Compartiment {index}: {holded_order.qty_holded} / {vehicule.size_compartment} --- dispo = {qty_available} ")
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
                    # print(f"Produit trouvé dans comp {index} : {holded_order.qty_holded} ")
        return qty_used
    
    def get_used_space_in_busy_compartments(self, vehicule: models.Vehicule):
        """
        Espace disponible dans les compartiments où il y déjà un --MÊME-- popduit similaire TODO: même poduit ou du même type
        """
        qty_used = 0
        for index, comp in enumerate(vehicule.compartiments):
            for holded_order in comp.holded_orders :
                qty_used +=  holded_order.qty_holded
                # print(f"Compartiment {index} : {holded_order.qty_holded} ")
        return qty_used

    def get_available_space_in_free_compartments(self, vehicule: models.Vehicule):
        nb_remaining_compartments = vehicule.nb_compartment - len(vehicule.compartiments)
        # print(f"Space in free comps : (holded_comp = {len(vehicule.compartiments)}, total_comp = {vehicule.nb_compartment} ) ")
        # print([i for i in vehicule.compartiments])
        return nb_remaining_compartments * vehicule.size_compartment

    def create_compartment(self, vehicule: models.Vehicule) -> models.Compartiment:
        c = models.Compartiment(vehicule_id = vehicule.id)
        c.vehicule_id = vehicule.id
        db.add(c)
        db.commit()
        db.refresh(c)
        db.refresh(vehicule)
        print(f"Create compartment {c.id} for V{vehicule.id} ")
        # db.refresh(vehicule)
        return c

vehicule = CRUDItem(Vehicule)
