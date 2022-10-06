from math import sqrt
from app.models.client import Client
from app.models.fournisseur import Fournisseur
from app.core.config import settings
from app import crud, models, schemas
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from typing import List, Union

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
        print(chemin)
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
    def _is_precedence_ok(cls, chemin) -> bool:
        for index, pt in enumerate(chemin):
            is_ok = False
            if isinstance(pt, models.Client):
                # print(f"Client {pt.name} à index #{index}/{len(chemin[1:-1])} ")
                fournisseurs_associes = set([i.id for i in crud.commande.get_fournisseurs_for_client(client= pt)])
                for f in chemin[:index] :
                    if isinstance(f, models.Fournisseur):
                        is_ok = crud.commande.must_deliver_client(db = SessionLocal(), f = f, client = pt)
                        # print(f"\n\nTest {pt.name} -> {f.name}/{fournisseurs_associes} ({is_ok}) ")
                        if is_ok: 
                            # print(f"--- YES {pt.name} est fourni par {f.name}, reste ({fournisseurs_associes})")
                            # break
                            fournisseurs_associes.remove(f.id)
                    # else:
                    #     print(f"Fournisseur {f.name} of type {type(f)} no instance of {models.Fournisseur} ")

                if not is_ok and len(fournisseurs_associes) != 0:
                    # print(f"------- DANGER client {pt.name} NON fourni ({fournisseurs_associes}). Parcouru {len(chemin[:index])} ({[i.name for i in chemin[:index]]}) index {index} ---------")
                    return False
                # print(f"Client {pt.name} est fourni par {f.name} ")
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
        k = len(self.chemin)
        mutations: List[self] = self._muter(self.chemin, len(self.chemin)-1)
        return mutations

    @classmethod
    def _muter(cls, chemin: list, k: int):
        mutations: List[cls] = []
        clone = chemin.copy()
        for i in range(1, min(k, len(chemin))):
            cls._permute(clone, i, i+1)
            print(f"\n\n Try to mutate {[i.name for i in clone]} ")
            # if cls._is_precedence_ok(clone) : #and cls._is_fenetre_ok(chemin) :
            if cls._is_precedence_ok(clone): # and cls._is_fenetre_ok(clone) :
                mutations.append(cls(clone.copy()))
            # mutations.append(cls(clone))
        if len(mutations) == 0:
            print("Aucune mutation trouvée ne respecte les contraintes ")
            # raise Exception("Aucune mutation trouvée ne respecte les contraintes ")
        return mutations

    def test_solution_by_vehicules(self, db: Session = SessionLocal()) -> List[models.Vehicule]:
        solution = self
        vehicules_queue = crud.vehicule.get_all()
        trajet_final = {}

        print("Test de la solution ", [i.name for i in solution.chemin])

        for vehicule in vehicules_queue:
            print("\n")
            # if vehicule.name not in trajet_final:
                # trajet_final[vehicule.name] = []
            trajet_final[vehicule.name] = [ schemas.Node(
                name = vehicule.depot.name, coords = vehicule.depot.coords, 
                code = vehicule.depot.code, type = get_node_type(vehicule.depot)
            ) ]

            for node in solution.chemin :
                if isinstance(node, models.Fournisseur):
                    print(f"FOURNISSEUR {node.name} ")
                    commandes = crud.commande.get_by_fournisseur(f = node)
                    for order in commandes:
                        qty_packed = crud.vehicule.hold(vehicule, order)
                        print(f"V{vehicule.id}, Order {order.id}, Packed {qty_packed}/{order.qty_fixed} in V{vehicule.id} à {node.name} ")
                        qty_remaining = order.qty_fixed - qty_packed
                        if qty_remaining < 0 :
                            # print(f" {order.qty} / {qty_packed} ")
                            raise Exception(f"Trop de produits ont été chagés dans le véhicule {vehicule.id}. Commande {order.id}, Restant {qty_packed}/{order.qty_fixed} ")
                        if qty_packed > 0 :
                            node_schema = schemas.Node(
                                name = node.name, coords = node.coords, 
                                code = node.code, type = get_node_type(node),
                                mvt = qty_packed 
                            )
                            if node_schema.name not in [ i.name for i in trajet_final[vehicule.name] ]:
                                trajet_final[vehicule.name].append(node_schema)
                            crud.vehicule.add_node_to_route(vehicule, node_schema, db= db)
                            # S'il y a encore des produits dans la commande, on passe au véhicule suivant 
                
                elif isinstance(node, models.Client):
                    client_holded_orders = crud.vehicule.get_client_holded_orders_in_vehicule(vehicule, node)
                    qty_delivered = 0
                    print(f"CLIENT C{node.name} reçu {len(client_holded_orders)} commandes du véhicule V{vehicule.id} ")
                    for h in client_holded_orders:
                        qty_delivered += h.qty_holded
                        # print(h.qty_holded)
                        crud.vehicule.deactivate_holded_order(h)
                    if qty_delivered != 0:
                        node_schema = schemas.Node(
                                    name = node.name, coords = node.coords, 
                                    code = node.code, type = get_node_type(node),
                                    mvt = -qty_delivered 
                                )
                        if node_schema.name not in [ i.name for i in trajet_final[vehicule.name] ]:
                            trajet_final[vehicule.name].append(node_schema)
                        crud.vehicule.add_node_to_route(vehicule, node_schema, db = self.db)
                        print([ f"Commande {h.commande.id}, Qté {h.qty_holded}/{h.commande.qty_fixed} \n" for h in client_holded_orders ])

            print(f"  Le VEHICULE {vehicule.name} avant test {len(trajet_final[vehicule.name])} %%%%%%%%")
            if len(trajet_final[vehicule.name]) == 1:
                print(" test == 1")
                trajet_final[vehicule.name] = []
                print(f"  Le VEHICULE {vehicule.name} n'a rien  foutu {len(trajet_final[vehicule.name])} £££££££")
            elif len(trajet_final[vehicule.name]) > 1 : 
                print(" test > 1")
                trajet_final[vehicule.name].append(schemas.Node(
                    name = vehicule.depot.name, coords = vehicule.depot.coords, 
                    code = vehicule.depot.code, type = get_node_type(vehicule.depot)
                ))
                print(f"  Le VEHICULE {vehicule.name} est au dépot {len(trajet_final[vehicule.name])} !!!! ")
            print(f"Le VEHICULE {vehicule.name} a fait {len(trajet_final[vehicule.name])} nodes ")
        print(trajet_final)
        return trajet_final


    def test_solution_by_orders(self, db: Session = SessionLocal()) -> List[models.Vehicule]:
        solution = self
        vehicules_queue = crud.vehicule.get_all()
        trajet_final = {}

        print("Test de la solution par commandes ", [i.name for i in solution.chemin])
        
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
                
                for commande in list_commandes:
                    total_ordered_qty += commande.qty_fixed
                    vehicule_available_space += crud.vehicule.get_available_space_in_free_compartments(vehicule= vehicule)
                
                if vehicule_available_space < total_ordered_qty:
                    print(f"Le V{vehicule.id} ne peut pas récup toutes les commandes du {client.name}: {vehicule_available_space}/{total_ordered_qty} ")

                    continue
                else:
                    if trajet_final.get(vehicule.name, None) == None:
                        print(f"Création du TRAJET pour {vehicule.name} ")
                        trajet_final[vehicule.name] = []
                    print(f" TREJT actuel du {vehicule.name} : ", trajet_final.get(vehicule.name, None))
                    for commande in list_commandes:
                        fournisseur = crud.fournisseur.get(id = commande.fournisseur_id)
                        qty_packed = crud.vehicule.hold(vehicule, commande)
                        print(f"V{vehicule.id}, Order {commande.id}, Packed {qty_packed}/{commande.qty_fixed} in V{vehicule.id} à {fournisseur.name} ")
                        qty_remaining = commande.qty_fixed - qty_packed
                        if qty_remaining < 0 :
                            # print(f" {order.qty} / {qty_packed} ")
                            raise Exception(f"Le véhicule {vehicule.id}. n'a quasiment pas chargé toutes les commandes du client {client.name}")
                        if qty_packed > 0 :
                            total_picked_qty += qty_packed
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

            # for node in trajet_final[key]:


            depot_schemas = schemas.Node(
                    name = v.depot.name, coords = v.depot.coords, 
                    code = v.depot.code, type = get_node_type(v.depot),
                    mvt = 0
                )
            trajet_final[key].append(depot_schemas)
            trajet_final[key].insert(0, depot_schemas)
        print("Trajet finale ", trajet_final)
        return trajet_final

