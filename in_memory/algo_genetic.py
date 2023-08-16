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

class Genetic:
    MAX_GEN_POP_LENGTH = 7
    # NB_GEN = 10
    # MAX_SELECTION_IN_GEN = 70
    SAMPLE_SOLUTIONS = 3

    def __init__(self, list_commandes: List[Union[WarehoudeModel, SupplierModel, ClientModel]], params: GeneticParams):
        #print"RECUIT")
        self.start_at = DateTime.now()
        self.params: GeneticParams = params
        self.initial_solution: Solution = self.generate_initial_solution(list_commandes)
        # #printf"Initial solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({self.initial_solution.is_precedence_ok()}) ")

    def __del__(self):
        pass

    def start(self) -> List:
        dataset = {}

        init_precedence = Solution.is_precedence_ok(self.initial_solution.chemin)
        curent_gen = [self.initial_solution]
        current_solution =  curent_gen[0]
        depot = WarehoudeModel.get_first()

        print(f"\n\n\n!! Start solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({init_precedence}) ")
        if not init_precedence :
            # print("Précedence initiale non respectée ", self.initial_solution.chemin)
            raise Exception(f"Précedence initiale non respectée -{init_precedence}- {[i.name for i in self.initial_solution.chemin]} ")
        else:
            for g in range(self.params.nb_generations):
                print(f"\n\nGeneration  n°{g}/{self.params.nb_generations}. Pop = ", len(curent_gen))
                any_sols = self.generation_next(curent_gen)
                print("\t Population après croisements ", len(any_sols))
                curent_gen = self.selection(any_sols)
                current_solution = curent_gen[0]
                print("\t Best ", current_solution.cout, " --> ", [i.name for i in current_solution.chemin])
        
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

    def generation_next(self, population: List[Solution]):
        new_generation: List[Solution] = []
        for p in population :
            muted_sols = p.muter()
            # print(len(muted_sols))
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
        # random.shuffle(generation)
        # best = [generation[0]]

        # for sol in generation:
        #     if random.random() > 0.5 :# sol.cout < best.cout :
        #         best.append(sol)
        # return best
        
        return random.sample(generation, min(self.params.gen_max_selection, len(generation)))