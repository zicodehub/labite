from math import exp
import queue, random
from time import time
from datetime import time as Time, datetime as DateTime
from typing import List, Union
from solution import Solution
from model_client import ClientModel, ClientSchema
from model_supplier import SupplierModel, SupplierSchema
from model_vehicule import VehiculeModel, VehiculeSchema
from model_warehouse import WarehoudeModel, WarehouseSchema
from model_order import OrderModel, OrderSchema
from model_compartment import CompartmentModel, CompartmentSchema
from model_batch import BatchModel, BatchSchema
from schemas.config import *

class TabuSearch:
    MAX_ITERATION: int = 10
    MAX_TABU_LIST_SIZE: int = 50
    NB_TABU_ITEMS_OUT_AT_TIME: int = 1
 
    TABU_LIST: set[Solution] = set()

    def __init__(self, list_commandes: List[Union[WarehoudeModel, SupplierModel, ClientModel]], params: TabuParams):
        #print"RECUIT")
        self.start_at = DateTime.now()
        self.init_params(params)
        self.initial_solution: Solution = self.generate_initial_solution(list_commandes)
        # #printf"Initial solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({self.initial_solution.is_precedence_ok()}) ")

    def __del__(self):
        pass

    def init_params(self, params: TabuParams):
        self.MAX_ITERATION = params.max_iter
        self.MAX_TABU_LIST_SIZE = params.max_tabu_list_size
        self.NB_TABU_ITEMS_OUT_AT_TIME = params.nb_out_at_time

    def start(self) -> List:
        dataset = {}

        init_precedence = Solution.is_precedence_ok(self.initial_solution.chemin)
        current_solution =  self.initial_solution
        depot = WarehoudeModel.get(1)

        print(f"\n\n\n!! Start solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({init_precedence}) ")
        if not init_precedence :
            # print("Précedence initiale non respectée ", self.initial_solution.chemin)
            raise Exception(f"Précedence initiale non respectée -{init_precedence}- {[i.name for i in self.initial_solution.chemin]}")
        else:
            for i in range(self.MAX_ITERATION):
                print(f"\n\Tabou  n°{i}/{self.MAX_ITERATION}")

                random_solutions = self.generate_neighborhood(current_solution)
                valid_solutions = self.pick_valid_neighbours(random_solutions)  # those not in Tabu list
                if len(valid_solutions) == 0:
                    print(f"\n ERRR valid_solutions ({len(valid_solutions)}) while random_solutions ({len(random_solutions)}) ")
                else:
                    best = self.selection(valid_solutions) # those not in Tabu list

                self.update_tabu(i, current_solution, best)
                current_solution = best

                print("\t Best ", best.cout, " --> ", [i.name for i in best.chemin])
        
        if len(self.TABU_LIST) > 0:
            current_solution = self.selection(list(self.TABU_LIST))
        
        duration = DateTime.now() - self.start_at
        dataset.update({
            "short": [depot.name] + [i.name for i in current_solution.chemin] + [depot.name],
            "duration": str(duration),
            "duration_seconds": duration.seconds
        })
        
        trajet_dict = current_solution.test_solution_by_vehicules()

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
                cout = VehiculeModel.get_by_name(v_key).cost
                cout_vehicule = distance_trajet_vehicule * cout
                cout_tous_vehicules += cout_vehicule
                distance_tous_trajet += distance_trajet_vehicule
                dataset["details"].append({
                    'distance_trajet_vehicule': distance_trajet_vehicule,
                    'cout_vehicule': cout
                })
                

        dataset["distance"] = distance_tous_trajet
        dataset["cout"] = cout_tous_vehicules
        for key in dataset["trajet"]:
            dataset["trajet"][key] = [i.json() for i in dataset["trajet"][key]]

                
        vehicules = {}
        for v in VehiculeModel.list_all():
            vehicules[v.name] = {}
            vehicules[v.name].update({
                field: getattr(v, field) for field in VehiculeSchema.__fields__
            })
            vehicules[v.name]['compartments'] = {}

            v_qty_holded = 0
            for comp in v.compartments:
                vehicules[v.name]['compartments'][comp.id] = {}
                vehicules[v.name]['compartments'][comp.id].update({
                    field: getattr(comp, field) for field in CompartmentSchema.__fields__
                })
                vehicules[v.name]['compartments'][comp.id]['total_batches'] = len(comp.batches)
                vehicules[v.name]['compartments'][comp.id]['filled_batches'] = len([ c for c in comp.batches if c.is_active is True])
                vehicules[v.name]['compartments'][comp.id]['holded'] = sum([ c.qty_holded for c in comp.batches])

                for h in comp.batches:
                    v_qty_holded += h.qty_holded

            vehicules[v.name]['holded'] = v_qty_holded

        dataset['vehicules'] = vehicules
        dataset['orders'] = {}
        OrderFields = OrderSchema.__fields__.copy()
        OrderFields.update({'qty': 91})
        for order in OrderModel.list_all():
            dataset['orders'][order.id] = {
                field: getattr(order, field) for field in OrderFields
            }
        print("\n\n\t EXECUTION TERMINEE !")
        return dataset

    @staticmethod
    def generate_initial_solution(list_commandes: List) -> Solution:
        # return [Solution([ f for f in Fournisseur.get_all_active() ] + [ c for c in Client.get_all_active() ] )]
        return Solution(list_commandes)

    def generate_neighborhood(self, s: Solution) -> List[Solution]:
        hood = s.muter()
        if len(hood) == 0:
            hood = [s]
        return hood
    
    def pick_valid_neighbours(self, hood: List[Solution]) -> List[Solution]:
        new_neighbours = []
        for s in hood:
            if s not in self.TABU_LIST:
                new_neighbours.append(s)

        return new_neighbours

    def selection(self, neighbourhood: List[Solution]) -> Solution:
        """
        Sélection de la meilleure solution
        """
        best = neighbourhood[0]
        for s in neighbourhood:
            if s.cout < best.cout:
                best = s

        
        return best
    
    def update_tabu(self, iteration, current_solution, new_solution) -> None:
        self.TABU_LIST.add(new_solution)
        if self.MAX_TABU_LIST_SIZE == len(self.TABU_LIST):
            for _ in range(self.NB_TABU_ITEMS_OUT_AT_TIME):
                self.TABU_LIST.pop()