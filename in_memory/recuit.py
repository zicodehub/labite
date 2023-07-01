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

class RecuitSimule:
    def __init__(self, list_commandes: List[Union[WarehoudeModel, SupplierModel, ClientModel]]):
        #print"RECUIT")
        self.start_at = DateTime.now()
        self.initial_solution: Solution = self.generate_initial_solution(list_commandes)
        # #printf"Initial solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({self.initial_solution.is_precedence_ok()}) ")

    def __del__(self):
        pass

    def start(self) -> List:
        dataset = {}

        init_precedence = self.initial_solution.is_precedence_ok(self.initial_solution.chemin)
        depot = WarehoudeModel.get(1)


        current_solution = self.initial_solution
        temp = 10
        reducteur = 0.99
        # reducteur = 0.9999
        #printf"\n\n\n!! Start solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({init_precedence}) ")
        if not init_precedence :
            # #print"Précedence initiale non respectée ", self.initial_solution.chemin)
            raise Exception(f"Précedence initiale non respectée -{init_precedence}- {[i.name for i in self.initial_solution.chemin]} ")
        else:
            while temp > 1:
                # print(temp)
                if DEBUG:
                    print(f"Temp=", temp)
                neighbor = self.generate_neighbord(current_solution)
                # return "yes"
                # #printf"Generation n°{g} created : {len(any_sols)}")
                if neighbor.cout > current_solution.cout:
                    current_solution = neighbor
                    if DEBUG:
                        print(f"\n Best {neighbor.cout} \n")
                else:
                    proba = exp(
                        -(abs(neighbor.cout - current_solution.cout)) / temp
                    )
                    # print("Proba ", proba)
                    if proba > 0.51:
                        current_solution = neighbor
                    temp *= reducteur
                # temp -= 1
                # #printf"Meilleurs cout de la generation n°{g} : {[i.cout for i in curent_gen]} ")
                
                #printf"Meilleurs cout de la generation n°{g} : {[i for i in curent_gen]} ")
        
        duration = DateTime.now() - self.start_at
        dataset.update({
            "short": [depot.name] + [i.name for i in current_solution.chemin] + [depot.name],
            "duration": str(duration),
            "duration_seconds": duration.seconds
            # "routes": self.test_solution(curent_gen[0]),
            # "long": curent_gen[0],
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
        vehicules_queue = VehiculeModel.list_all()
        
        for v in vehicules_queue:
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

    def generate_neighbord(self, s: Solution) -> Solution:
        muted_sol = s  
        # print("\n Neighborhood for ", [g.name for g in s.chemin])      
        for i in range(random.randint(2, 5)):
            temp = muted_sol.muter()
            try:
                if len(temp) > 1:
                    # min_mutant = temp[0]
                    # for m in temp:
                    #     if m.cout < min_mutant.cout:
                    #         min_mutant = m 
                    muted_sol = temp[random.randrange(0, len(temp)-1)]
                else:
                    muted_sol = temp[0]
            except IndexError as e:
                # raise e
                # print("Mutations no trouvées pour le chemin ", [k.name for k in s.chemin ])
                pass
            if random.random() > 0.45:
                ##printlen(muted_sols))
                return muted_sol

        return muted_sol