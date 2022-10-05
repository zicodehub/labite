import queue
from typing import List, Union
from app.utils.solution import Solution
from app import crud, models, schemas
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

def get_node_type(node: Union[models.Depot, models.Fournisseur, models.Client]) -> schemas.NodeType:
    if isinstance(node, models.Depot):
        return schemas.NodeType.depot
    if isinstance(node, models.Fournisseur):
        return schemas.NodeType.fournisseur
    if isinstance(node, models.Client):
        return schemas.NodeType.client
    else:
        raise Exception("Node type not recognized: Supported are Depot, Fournisseur, Client ")


class Genetic:
    MAX_GEN_POP_LENGTH = 3
    NB_GEN = 2
    MAX_SELECTION_IN_GEN = 5
    SAMPLE_SOLUTIONS = 3
    def __init__(self, list_commandes: List[Union[models.Depot, models.Fournisseur, models.Client]], db: Session = SessionLocal()) -> None:
        print("ZOAMDI")
        self.initial_solution: Solution = self.generate_initial_solution(list_commandes)
        self.db = db
        # print(f"Initial solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({self.initial_solution.is_precedence_ok()}) ")

    def __del__(self):
        self.db.close()

    def start(self) -> List:
        dataset = {}

        init_precedence = self.initial_solution.is_precedence_ok()
        curent_gen = [self.initial_solution]
        depot = crud.depot.get_first()
        print(f"\n\n\n!! Start solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({init_precedence}) ")
        if not init_precedence :
            # print("Précedence initiale non respectée ", self.initial_solution.chemin)
            raise Exception(f"Précedence initiale non respectée -{init_precedence}- {[i.name for i in self.initial_solution.chemin]} ")
        else:
            for g in range(self.NB_GEN):
                print(f"Going to create a generation  n°{g}")
                any_sols = self.generation_next(curent_gen)
                print(f"Generation n°{g} created : {len(any_sols)}")
                curent_gen = self.selection(any_sols)
                print(f"Meilleurs cout de la generation n°{g} : {[i.cout for i in curent_gen]} ")
                dataset.update({
                    "short": [depot.name] + [i.name for i in curent_gen[0].chemin] + [depot.name],
                    # "routes": self.test_solution(curent_gen[0]),
                    # "long": curent_gen[0],
                })
                # print(f"Meilleurs cout de la generation n°{g} : {[i for i in curent_gen]} ")
        # trajet_dict = self.test_solution(curent_gen[0])
        # print(f"Finale : {curent_gen[0].cout} -> {curent_gen[0].is_precedence_ok()} ")
        # trajet_dict = curent_gen[0].test_solution_by_vehicules(db= self.db)
        trajet_dict = curent_gen[0].test_solution_by_orders(db= self.db)
        dataset["trajet"] = trajet_dict
        cout_tous_vehicules = 0 
        distance_tous_trajet = 0
        dataset["details"] = []
        for v_key in trajet_dict :
            distance_trajet_vehicule = 0 
            trajet_vehicule = trajet_dict[v_key]
            if len(trajet_vehicule) > 1:
                prec_node = trajet_vehicule[0]
                for node in trajet_vehicule[1:]:
                    distance_trajet_vehicule += Solution.distance(prec_node, node)
                    prec_node = node
                cout = crud.vehicule.get_by_name(v_key).cout
                cout_vehicule = distance_trajet_vehicule * cout
                cout_tous_vehicules += cout_vehicule
                distance_tous_trajet += distance_trajet_vehicule
                dataset["details"].append({
                    'distance_trajet_vehicule': distance_trajet_vehicule,
                    'cout_vehicule': cout
                })
                

        dataset["distance"] = distance_tous_trajet
        dataset["cout"] = cout_tous_vehicules
        return dataset

    @staticmethod
    def generate_initial_solution(list_commandes: List) -> Solution:
        # return [Solution([ f for f in Fournisseur.get_all_active() ] + [ c for c in Client.get_all_active() ] )]
        return Solution(list_commandes)

    def generation_next(self, population: List[Solution]):
        new_generation: List[Solution] = []
        for p in population :
            for i in range(self.MAX_GEN_POP_LENGTH):
                muted_sols = p.muter()
                print(len(muted_sols))
                new_generation.extend(muted_sols)

        return new_generation if len(new_generation) else [self.initial_solution]

    def selection(self, generation: List[Solution]):
        """
        Sélection des X meilleures solutions
        """
        # selection = generation[5]
        # for solution in generation[5:]:
        #     for s in selection:
        #         if solution.cout < s.cout :
        #             selection.append(solution)
        #             break
        #     if len(selection)
        best = generation[0]

        for sol in generation:
            if sol.cout <= best.cout :
                best = sol
        return [best]
        # sorted(generation, lambda sol:  sol.cout)

    # def test_solution(self, solution: Solution) -> List[models.Vehicule]:
    #     vehicules_queue = crud.vehicule.get_all()
    #     trajet_final = {}

    #     print("Test de la solution ", [i.name for i in solution.chemin])

    #     for vehicule in vehicules_queue:
    #         print("\n")
    #         # if vehicule.name not in trajet_final:
    #             # trajet_final[vehicule.name] = []
    #         trajet_final[vehicule.name] = [ schemas.Node(
    #             name = vehicule.depot.name, coords = vehicule.depot.coords, 
    #             code = vehicule.depot.code, type = get_node_type(vehicule.depot)
    #         ) ]

    #         for node in solution.chemin :
    #             if isinstance(node, models.Fournisseur):
    #                 print(f"FOURNISSEUR {node.name} ")
    #                 commandes = crud.commande.get_by_fournisseur(f = node)
    #                 for order in commandes:
    #                     qty_packed = crud.vehicule.hold(vehicule, order)
    #                     print(f"V{vehicule.id}, Order {order.id}, Packed {qty_packed}/{order.qty_fixed} in V{vehicule.id} à {node.name} ")
    #                     qty_remaining = order.qty_fixed - qty_packed
    #                     if qty_remaining < 0 :
    #                         # print(f" {order.qty} / {qty_packed} ")
    #                         raise Exception(f"Trop de produits ont été chagés dans le véhicule {vehicule.id}. Commande {order.id}, Restant {qty_packed}/{order.qty_fixed} ")
    #                     if qty_packed > 0 :
    #                         node_schema = schemas.Node(
    #                             name = node.name, coords = node.coords, 
    #                             code = node.code, type = get_node_type(node),
    #                             mvt = qty_packed 
    #                         )
    #                         if node_schema.name not in [ i.name for i in trajet_final[vehicule.name] ]:
    #                             trajet_final[vehicule.name].append(node_schema)
    #                         crud.vehicule.add_node_to_route(vehicule, node_schema, db= self.db)
    #                         # S'il y a encore des produits dans la commande, on passe au véhicule suivant 
                
    #             elif isinstance(node, models.Client):
    #                 client_holded_orders = crud.vehicule.get_client_holded_orders_in_vehicule(vehicule, node)
    #                 qty_delivered = 0
    #                 print(f"CLIENT C{node.name} reçu {len(client_holded_orders)} commandes du véhicule V{vehicule.id} ")
    #                 for h in client_holded_orders:
    #                     qty_delivered += h.qty_holded
    #                     # print(h.qty_holded)
    #                     crud.vehicule.deactivate_holded_order(h)
    #                 if qty_delivered != 0:
    #                     node_schema = schemas.Node(
    #                                 name = node.name, coords = node.coords, 
    #                                 code = node.code, type = get_node_type(node),
    #                                 mvt = -qty_delivered 
    #                             )
    #                     if node_schema.name not in [ i.name for i in trajet_final[vehicule.name] ]:
    #                         trajet_final[vehicule.name].append(node_schema)
    #                     crud.vehicule.add_node_to_route(vehicule, node_schema, db = self.db)
    #                     print([ f"Commande {h.commande.id}, Qté {h.qty_holded}/{h.commande.qty_fixed} \n" for h in client_holded_orders ])

    #         print(f"  Le VEHICULE {vehicule.name} avant test {len(trajet_final[vehicule.name])} %%%%%%%%")
    #         if len(trajet_final[vehicule.name]) == 1:
    #             print(" test == 1")
    #             trajet_final[vehicule.name] = []
    #             print(f"  Le VEHICULE {vehicule.name} n'a rien  foutu {len(trajet_final[vehicule.name])} £££££££")
    #         elif len(trajet_final[vehicule.name]) > 1 : 
    #             print(" test > 1")
    #             trajet_final[vehicule.name].append(schemas.Node(
    #                 name = vehicule.depot.name, coords = vehicule.depot.coords, 
    #                 code = vehicule.depot.code, type = get_node_type(vehicule.depot)
    #             ))
    #             print(f"  Le VEHICULE {vehicule.name} est au dépot {len(trajet_final[vehicule.name])} !!!! ")
    #         print(f"Le VEHICULE {vehicule.name} a fait {len(trajet_final[vehicule.name])} nodes ")
    #     print(trajet_final)
    #     return trajet_final


