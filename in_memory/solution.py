from math import sqrt
from random import randrange, randint
from time import time
from model_client import ClientModel
from model_supplier import SupplierModel
from model_vehicule import VehiculeModel
from model_warehouse import WarehoudeModel
from model_order import OrderModel
from schemas.config import *

from typing import List, Union

def get_node_type(node: Union[WarehoudeModel, SupplierModel, ClientModel]) -> NodeType:
    if isinstance(node, WarehoudeModel):
        return NodeType.depot
    if isinstance(node, SupplierModel):
        return NodeType.fournisseur
    if isinstance(node, ClientModel):
        return NodeType.client
    else:
        raise Exception("Node type not recognized: Supported are Depot, Fournisseur, Client ")


class Solution:
    def __init__(self, chemin: List[SupplierModel | ClientModel]) -> None:
        self.chemin = chemin
        #printchemin)
        self.cout = self.compute_cout()
    
    def compute_cout(self):
        cout = 0
        if len(self.chemin) <= 1:
            return 0
            
        i = self.chemin[0]
        for j in self.chemin[1:] :
            cout += self.distance(i, j)
            i = j

        return cout
    
    def permute(self, i, j):
        self._permuter(self.chemin, i, j)
    
    @classmethod
    def _permute(cls, array, i, j):
        array[i], array[j] = array[j], array[i]
    REFUSED = 0
    ACCEPTED = 0
    @classmethod
    def is_precedence_ok(cls, chemin) -> bool:
        res = cls._is_precedence_ok(chemin)
        # form = [i.name for i in chemin]
        # # print("Call precedndec")
        # if res is False:
        #     cls.REFUSED += 1
        #     print("\n NONO precedence ", cls.REFUSED,  form)
        # else:
        #     cls.ACCEPTED += 1
        #     print("\n YES precedence ----------- ", cls.ACCEPTED, form)
        return res
    
    @classmethod
    def _is_precedence_ok(cls, chemin) -> bool:
        for index, pt in enumerate(chemin):
            is_ok = False
            if isinstance(pt, ClientModel):
                fournisseurs_associes = set([i.id for i in OrderModel.get_fournisseurs_for_client(client= pt)])
                for f in chemin[:index] :
                    if isinstance(f, SupplierModel):
                        is_ok = OrderModel.must_deliver_client(f = f, client = pt)
                        if is_ok: 
                            fournisseurs_associes.remove(f.id)
                
                if not is_ok and len(fournisseurs_associes) != 0:
                    return False

        for index, pt in enumerate(chemin):
            reject = False
            if isinstance(pt, ClientModel):
                mes_fournisseurs_ids = [four.supplier.id for four in pt.orders ]
                fournisseurs_associes = set(mes_fournisseurs_ids)
                for f in chemin[index:] :
                    if isinstance(f, SupplierModel):
                        reject = f.id in fournisseurs_associes
                        if reject: 
                            # fournisseurs_associes.remove(f.id)
                            return False
                
                # if not is_ok and len(fournisseurs_associes) != 0:
                #     return False
        return True

    @classmethod
    def distance(cls, i, j):
        xi, yi = i.x, i.y
        xj, yj = j.x, j.y

        return sqrt(
                (xi - xj)**2 + (yi - yj)**2 
            )
        
    @classmethod
    def duree_trajet(cls, i, j):
        return cls.distance(i, j) / 60



    def is_fenetre_ok(self):
        return self.is_fenetre_ok(self.chemin)

    @classmethod
    def _is_fenetre_ok(self, chemin):
        t_depart = 0
        i = chemin[0]
        for j in chemin[1:]:
            if t_depart + self.duree_trajet(i, j) > (j.time_interval_end - j.time_service) :
                return False

        return True

    def muter(self):
        # print("Gonna mutate")
        size = len(self.chemin) -1
        mutations: List[self] = self._muter(self,  size)
        # print("Yes my loard")
        return mutations
        # return self.chemin

    @classmethod
    def _muter(cls, sol, k: int):
        chemin = sol.chemin
        mutations: List[cls] = []
        size = len(chemin) -1
        clone = chemin.copy()
        # print("Muter size=", size)
        for i in range(randrange(1, size//2), randrange(size//2, size-1)):
            # cls._permute(clone, randrange(1, size), randrange(1, size))
            cls._permute(clone, i, i+1)
            
            if cls._is_precedence_ok(clone): # and cls._is_fenetre_ok(clone) :
                mutations.append(cls(clone.copy()))
            # mutations.append(cls(clone))
        if len(mutations) == 0:
            pass
            #print"Aucune mutation trouvée ne respecte les contraintes ")
            # raise Exception("Aucune mutation trouvée ne respecte les contraintes ")
        # print(f"Found {len(mutations)} mutations ")
        return mutations

    def test_solution_by_vehicules(self) -> List[VehiculeModel]:
        solution = self
        vehicules_queue = VehiculeModel.list_all()
        trajet_final = {}

        #print"Test de la solution ", [i.name for i in solution.chemin])

        for vehicule in vehicules_queue:
            #print"\n")
            # if vehicule.name not in trajet_final:
                # trajet_final[vehicule.name] = []
            trajet_final[vehicule.name] = [ Node(
                name = vehicule.warehouse.name, x = vehicule.warehouse.x, y = vehicule.warehouse.y, 
                code = vehicule.warehouse.name, type = get_node_type(vehicule.warehouse)
            ) ]
            for node in solution.chemin :
                print("\n\n ", vehicule.name , " on ", node.name)
                if isinstance(node, SupplierModel):
                    #printf"FOURNISSEUR {node.name} ")
                    commandes: List[OrderModel] = OrderModel.get_by_fournisseur(f = node)
                    print(f"{node.name} has {len(commandes)} orders")
                    for order in commandes:
                        order: OrderModel = OrderModel.get(order.id)
                        # print("2* Gonna hold ")
                        qty_packed = VehiculeModel.hold(vehicule, order)
                        # print("3* Holded order ", qty_packed)
                        print(f"V{vehicule.id} ({node.name} -> {order.client.name}) , Order {order.id}, Packed {qty_packed}/{order.qty_fixed} in V{vehicule.id} à {node.name} ")
                        qty_remaining = order.qty_fixed - qty_packed
                        if qty_remaining < 0 :
                            # #printf" {order.qty} / {qty_packed} ")
                            raise Exception(f"Trop de produits ont été chagés dans le véhicule {vehicule.id}. Commande {order.id}, Restant {qty_packed}/{order.qty_fixed} ")
                        if qty_packed > 0 :
                            node_schema = Node(
                                name = node.name, 
                                x = node.x,
                                y = node.y, 
                                code = node.name, type = get_node_type(node),
                                mvt = qty_packed 
                            )
                            print(vehicule.name , len(order.batches), " -- ", node_schema.json(), end='\n')
                            if node_schema.name not in [ i.name for i in trajet_final[vehicule.name] ]:
                                trajet_final[vehicule.name].append(node_schema)
                            VehiculeModel.add_node_to_route(vehicule, node_schema)
                            # S'il y a encore des produits dans la commande, on passe au véhicule suivant 
                
                elif isinstance(node, ClientModel):
                    client_holded_orders = VehiculeModel.get_client_holded_orders_in_vehicule(vehicule, node)
                    qty_delivered = 0
                    print(f"CLIENT C{node.name} reçu {len(client_holded_orders)} commandes du véhicule V{vehicule.id} ")
                    for h in client_holded_orders:
                        qty_delivered += h.qty_holded
                        # #printh.qty_holded)
                        VehiculeModel.deactivate_holded_order(h)
                    if qty_delivered != 0:
                        node_schema = Node(
                                    name = node.name,
                                    code = node.name, 
                                    type = get_node_type(node),
                                    mvt = -qty_delivered,
                                    x = node.x,
                                    y = node.y, 
                                )
                        if node_schema.name not in [ i.name for i in trajet_final[vehicule.name] ]:
                            trajet_final[vehicule.name].append(node_schema)
                        VehiculeModel.add_node_to_route(vehicule, node_schema)
                        print(vehicule.name , len(order.batches), " -- ", node_schema.json(), end='\n')
                            
                        #print[ f"Commande {h.commande.id}, Qté {h.qty_holded}/{h.commande.qty_fixed} \n" for h in client_holded_orders ])
                    else:
                        print("No for client ", len(client_holded_orders))
            #printf"  Le VEHICULE {vehicule.name} avant test {len(trajet_final[vehicule.name])} %%%%%%%%")
            if len(trajet_final[vehicule.name]) == 1:
                #print" test == 1")
                trajet_final[vehicule.name] = []
                #printf"  Le VEHICULE {vehicule.name} n'a rien  foutu {len(trajet_final[vehicule.name])} £££££££")
            elif len(trajet_final[vehicule.name]) > 1 : 
                #print" test > 1")
                trajet_final[vehicule.name].append(Node(
                    name = vehicule.warehouse.name, 
                    x = vehicule.warehouse.x,
                    y = vehicule.warehouse.y,
                    code = vehicule.warehouse.name, type = get_node_type(vehicule.warehouse)
                ))
                #printf"  Le VEHICULE {vehicule.name} est au dépot {len(trajet_final[vehicule.name])} !!!! ")
            #printf"Le VEHICULE {vehicule.name} a fait {len(trajet_final[vehicule.name])} nodes ")
        #printtrajet_final)
        return trajet_final