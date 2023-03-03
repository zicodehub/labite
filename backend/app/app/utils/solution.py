from math import sqrt
from random import randrange, randint
from time import time
from app.models.client import Client
from app.models.fournisseur import Fournisseur
from app.core.config import settings
from app import crud, models, schemas
from app.db.session import SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import List, Union

db = get_db().send(None)

def get_node_type(node: Union[models.Depot, models.Fournisseur, models.Client]) -> schemas.NodeType:
    if isinstance(node, models.Depot):
        return schemas.NodeType.depot
    if isinstance(node, models.Fournisseur):
        return schemas.NodeType.fournisseur
    if isinstance(node, models.Client):
        return schemas.NodeType.client
    else:
        raise Exception("Node type not recognized: Supported are Depot, Fournisseur, Client ")


class Solution:
    def __init__(self, chemin) -> None:
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
    
    def is_precedence_ok(self) -> bool:
        return self._is_precedence_ok(self.chemin)
    
    @classmethod
    def _is_precedence_ok(cls, chemin, db= db) -> bool:
        # for index, pt in enumerate(chemin):
        #     is_ok = False
        #     if isinstance(pt, models.Client):
        #         fournisseurs_associes = set([i.id for i in crud.commande.get_fournisseurs_for_client(client= pt)])
        #         for f in chemin[:index] :
        #             if isinstance(f, models.Fournisseur):
        #                 is_ok = crud.commande.must_deliver_client(db, f = f, client = pt)
        #                 if is_ok: 
        #                     fournisseurs_associes.remove(f.id)
                
        #         if not is_ok and len(fournisseurs_associes) != 0:
        #             return False

        for index, pt in enumerate(chemin):
            reject = False
            if isinstance(pt, models.Client):
                mes_fournisseurs_ids = [four.fournisseur_id for four in pt.commandes ]
                fournisseurs_associes = set(mes_fournisseurs_ids)
                for f in chemin[index:] :
                    if isinstance(f, models.Fournisseur):
                        reject = f.id in fournisseurs_associes
                        if reject: 
                            # fournisseurs_associes.remove(f.id)
                            return False
                
                # if not is_ok and len(fournisseurs_associes) != 0:
                #     return False
        return True

    @classmethod
    def distance(cls, i, j):
        xi, yi = [int(_) for _ in i.coords.split(";")]
        xj, yj = [int(_) for _ in j.coords.split(";")]

        return sqrt(
                (xi - xj)**2 + (yi - yj)**2 
            )
        
    @classmethod
    def duree_trajet(cls, i, j):
        return cls.distance(i, j) / settings.VITESSE_VEHICULE



    def is_fenetre_ok(self):
        return self._is_fenetre_ok(self.chemin)

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
    def _muter(cls, sol, k: int, db = db):
        chemin = sol.chemin
        mutations: List[cls] = []
        size = len(chemin) -1
        clone = chemin.copy()
        for i in range(1, size-1):
            # cls._permute(clone, randrange(1, size), randrange(1, size))
            cls._permute(clone, i, i+1)
            
            if cls._is_precedence_ok(clone, db= db): # and cls._is_fenetre_ok(clone) :
                mutations.append(cls(clone.copy()))
            # mutations.append(cls(clone))
        if len(mutations) == 0:
            pass
            #print"Aucune mutation trouvée ne respecte les contraintes ")
            # raise Exception("Aucune mutation trouvée ne respecte les contraintes ")
        print(f"Found {len(mutations)} mutations ")
        return mutations

    def test_solution_by_vehicules(self, db: Session = SessionLocal()) -> List[models.Vehicule]:
        solution = self
        vehicules_queue = crud.vehicule.get_all()
        trajet_final = {}

        #print"Test de la solution ", [i.name for i in solution.chemin])

        for vehicule in vehicules_queue:
            #print"\n")
            # if vehicule.name not in trajet_final:
                # trajet_final[vehicule.name] = []
            trajet_final[vehicule.name] = [ schemas.Node(
                name = vehicule.depot.name, coords = vehicule.depot.coords, 
                code = vehicule.depot.code, type = get_node_type(vehicule.depot)
            ) ]
            for node in solution.chemin :
                print(vehicule.name , " on ", node.name)
                if isinstance(node, models.Fournisseur):
                    #printf"FOURNISSEUR {node.name} ")
                    commandes = crud.commande.get_by_fournisseur(f = node)
                    # print(f"1* Fournoisseurs got {len(commandes)} orders")
                    for order in commandes:
                        order = crud.commande.get(order.id)
                        # print("2* Gonna hold ")
                        qty_packed = crud.vehicule.hold(vehicule, order)
                        # print("3* Holded order ", qty_packed)
                        #printf"V{vehicule.id}, Order {order.id}, Packed {qty_packed}/{order.qty_fixed} in V{vehicule.id} à {node.name} ")
                        qty_remaining = order.qty_fixed - qty_packed
                        if qty_remaining < 0 :
                            # #printf" {order.qty} / {qty_packed} ")
                            raise Exception(f"Trop de produits ont été chagés dans le véhicule {vehicule.id}. Commande {order.id}, Restant {qty_packed}/{order.qty_fixed} ")
                        if qty_packed > 0 :
                            node_schema = schemas.Node(
                                name = node.name, coords = node.coords, 
                                code = node.code, type = get_node_type(node),
                                mvt = qty_packed 
                            )
                            print(vehicule.name , len(order.holdings), " -- ", node_schema.json(), end='\n')
                            if node_schema.name not in [ i.name for i in trajet_final[vehicule.name] ]:
                                trajet_final[vehicule.name].append(node_schema)
                            crud.vehicule.add_node_to_route(vehicule, node_schema, db= db)
                            # S'il y a encore des produits dans la commande, on passe au véhicule suivant 
                
                elif isinstance(node, models.Client):
                    client_holded_orders = crud.vehicule.get_client_holded_orders_in_vehicule(vehicule, node)
                    qty_delivered = 0
                    #printf"CLIENT C{node.name} reçu {len(client_holded_orders)} commandes du véhicule V{vehicule.id} ")
                    for h in client_holded_orders:
                        qty_delivered += h.qty_holded
                        # #printh.qty_holded)
                        crud.vehicule.deactivate_holded_order(h)
                    if qty_delivered != 0:
                        node_schema = schemas.Node(
                                    name = node.name, coords = node.coords, 
                                    code = node.code, type = get_node_type(node),
                                    mvt = -qty_delivered 
                                )
                        if node_schema.name not in [ i.name for i in trajet_final[vehicule.name] ]:
                            trajet_final[vehicule.name].append(node_schema)
                        crud.vehicule.add_node_to_route(vehicule, node_schema)
                        print(vehicule.name , len(order.holdings), " -- ", node_schema.json(), end='\n')
                            
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
                trajet_final[vehicule.name].append(schemas.Node(
                    name = vehicule.depot.name, coords = vehicule.depot.coords, 
                    code = vehicule.depot.code, type = get_node_type(vehicule.depot)
                ))
                #printf"  Le VEHICULE {vehicule.name} est au dépot {len(trajet_final[vehicule.name])} !!!! ")
            #printf"Le VEHICULE {vehicule.name} a fait {len(trajet_final[vehicule.name])} nodes ")
        #printtrajet_final)
        return trajet_final


    def test_solution_by_orders(self, db: Session = SessionLocal()) -> List[models.Vehicule]:
        solution = self
        vehicules_queue = crud.vehicule.get_all()
        trajet_final = {}

        #print"Test de la solution par commandes ", [i.name for i in solution.chemin])
        
        clients_in_solution = [ node for node in solution.chemin if isinstance(node, models.Client) ]
        for client in clients_in_solution:
            list_commandes = crud.commande.get_by_client(client= client)
            are_client_orders_satisfied = False
            last_vehicule = None
            total_picked_qty = 0
            for vehicule in vehicules_queue:
                if are_client_orders_satisfied:
                    break
                total_ordered_qty = 0
                vehicule_available_space = 0
                

                ### Revoir cette technque.
                # EN fait, on doit charger le véhicule avec autant de produits restant dans les commande du client. 
                # Si toutes les commandes sont parcourues et livrées (commande.qty == 0), c'est bien
                # SInon, décharger complétemlent le vehicule puis passer au suivant
                for commande in list_commandes:
                    total_ordered_qty += commande.qty_fixed
                vehicule_available_space += crud.vehicule.get_available_space_in_free_compartments(vehicule= vehicule)
                
                if vehicule_available_space < total_ordered_qty: 
                    # Si le véhicule ne peut pas prendre toutes le commandes de ce client, on passe au vehicule suivant
                    print(f"Le V{vehicule.id} ne peut pas récup toutes les commandes du {client.name}: {vehicule_available_space}/{total_ordered_qty} ")

                    continue
                else:
                    print(f"\n  Avant chargement, Le {vehicule.name} va charger {total_ordered_qty} / {vehicule_available_space}. Dispo in vehicule {crud.vehicule.get_available_space_in_free_compartments(vehicule)} ")
                    if trajet_final.get(vehicule.name, None) == None:
                        #printf"Création du TRAJET pour {vehicule.name} ")
                        trajet_final[vehicule.name] = []
                    #printf" TREJT actuel du {vehicule.name} : ", trajet_final.get(vehicule.name, None))
                    for commande in list_commandes:
                        fournisseur = crud.fournisseur.get(id = commande.fournisseur_id)
                        qty_packed = crud.vehicule.hold(vehicule, commande)
                        print(f"\n Après chargement,  Le {vehicule.name} va charger {total_ordered_qty} / {vehicule_available_space}. Dispo in vehicule {crud.vehicule.get_available_space_in_free_compartments(vehicule)} ")
                    
                        print(f"V{vehicule.id}, Order {commande.id}, Packed {qty_packed}/{commande.qty_fixed} in V{vehicule.id} à {fournisseur.name} ")
                        qty_remaining = commande.qty_fixed - qty_packed
                        if qty_remaining < 0 :
                            # #printf" {order.qty} / {qty_packed} ")
                            raise Exception(f"Le véhicule {vehicule.id}. n'a quasiment pas chargé toutes les commandes du client {client.name}")
                        if qty_packed > 0 :
                            total_picked_qty += qty_packed
                            print(f" {client.name} total_picked_qty = {total_picked_qty} ")
                            node_schema = schemas.Node(
                                name = fournisseur.name, coords = fournisseur.coords, 
                                code = fournisseur.code, type = get_node_type(fournisseur),
                                mvt = qty_packed 
                            )
                            # if node_schema.name not in [ i.name for i in trajet_final[vehicule.name] ]:
                            trajet_final[vehicule.name].append(node_schema)
                            crud.vehicule.add_node_to_route(vehicule, node_schema, db= db) 
                    are_client_orders_satisfied = True
                    last_vehicule = vehicule
                    

            if are_client_orders_satisfied:
                print(f"Client {client.name} is satisfied ", total_picked_qty)
                node_schema = schemas.Node(
                    name = client.name, coords = client.coords, 
                    code = client.code, type = get_node_type(client),
                    mvt = -total_picked_qty 
                )
                if last_vehicule:
                    trajet_final[last_vehicule.name].append(node_schema)
                  
            else:
                # raise Exception(f"Error: Client {client.name} NON SATISFATIT")
                pass
        for key in trajet_final:
            v_id = key.split('V')[1]
            v = crud.vehicule.get(id= v_id)

            depot_schemas = schemas.Node(
                    name = v.depot.name, coords = v.depot.coords, 
                    code = v.depot.code, type = get_node_type(v.depot),
                    mvt = 0
                )

            vehicule_route = [depot_schemas]
            for index, node in enumerate(trajet_final[key]):
                founds = set()
                vehicule_route.append(node)
                for next_node in vehicule_route:
                    if node.name == next_node.name  :
                        if next_node.name not in founds :
                            node.mvt += next_node.mvt
                            founds.add(next_node.name)
                        else:
                            trajet_final[key] = trajet_final[key][:index] + trajet_final[key][index+1:]

            
            trajet_final[key].append(depot_schemas)
            trajet_final[key].insert(0, depot_schemas)
        #print"Trajet finale ", trajet_final)
        return trajet_final

