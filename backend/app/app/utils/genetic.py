import queue
from datetime import datetime as DateTime
from typing import Any, List, Union
from app.utils.solution import Solution
from app import crud, models, schemas
from sqlalchemy.orm import Session
import random
from app.db.session import SessionLocal
from fastapi import APIRouter, Depends, HTTPException

class Genetic:
    MAX_GEN_POP_LENGTH = 10
    NB_GEN = 10
    MAX_SELECTION_IN_GEN = 1
    SAMPLE_SOLUTIONS = 1
    def __init__(self, list_commandes: List[Union[models.Depot, models.Fournisseur, models.Client]], db: Session = SessionLocal(), **kw) -> None:
        #print"ZOAMDI")
        for key in kw:
            setattr(self, key, kw[key])
        self.start_at = DateTime.now()
        self.initial_solution: Solution = self.generate_initial_solution(list_commandes)
        self.db = db
        # #printf"Initial solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({self.initial_solution.is_precedence_ok()}) ")

    def __del__(self):
        self.db.close()

    @classmethod
    def run_multi(cls, db, params: Any) -> List:
        solutions_finales = []
        for i in range(cls.SAMPLE_SOLUTIONS):
            f = crud.commande.get_fournisseurs(db = db)
            c = crud.commande.get_clients(db = db)
            d = crud.depot.get_first(db = db)
            #printf"Il y a {len(f)} fourn et {len(c)} clients ")
            
            random.shuffle(f)
            random.shuffle(c)
            
            # list_initial = [d] + f + c + [d]
            list_initial = f + c 
            genetic = cls(list_initial, db= db)
            res = genetic.start()
            db.close_all()
            solutions_finales.append(res)
            
        return solutions_finales    

    def start(self) -> List:
        dataset = {}

        init_precedence = self.initial_solution.is_precedence_ok()
        curent_gen = [self.initial_solution]
        depot = crud.depot.get_first()
        #printf"\n\n\n!! Start solution {[i.name for i in self.initial_solution.chemin]} -- Cout {self.initial_solution.cout} -- HMM ({init_precedence}) ")
        if not init_precedence :
            # #print"Précedence initiale non respectée ", self.initial_solution.chemin)
            raise Exception(f"Précedence initiale non respectée -{init_precedence}- {[i.name for i in self.initial_solution.chemin]} ")
        else:
            for g in range(self.NB_GEN):
                #printf"Going to create a generation  n°{g}")
                any_sols = self.generation_next(curent_gen)
                #printf"Generation n°{g} created : {len(any_sols)}")
                curent_gen = self.selection(any_sols)
                #printf"Meilleurs cout de la generation n°{g} : {[i.cout for i in curent_gen]} ")
                dataset.update({
                    "short": [depot.name] + [i.name for i in curent_gen[0].chemin] + [depot.name],
                    # "routes": self.test_solution(curent_gen[0]),
                    # "long": curent_gen[0],
                })
                # #printf"Meilleurs cout de la generation n°{g} : {[i for i in curent_gen]} ")
        # trajet_dict = self.test_solution(curent_gen[0])
        # #printf"Finale : {curent_gen[0].cout} -> {curent_gen[0].is_precedence_ok()} ")
        # trajet_dict = curent_gen[0].test_solution_by_vehicules(db= self.db)
        trajet_dict = curent_gen[0].test_solution_by_vehicules(db= self.db)
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
        dataset["duration"] = str(DateTime.now() - self.start_at)
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
                #printlen(muted_sols))
                new_generation.extend(muted_sols)

        return new_generation if len(new_generation) else [self.initial_solution]

    def selection(self, generation: List[Solution]):
        """
        Sélection des X meilleures solutions
        """
        # best = generation[0]

        # for sol in generation:
        #     if sol.cout <= best.cout :
        #         best = sol
        # return [best]

        generation.sort(key= lambda x: x.cout)
        print(f"Selected {self.MAX_SELECTION_IN_GEN}/{len(generation)} people")
        return generation[:self.MAX_SELECTION_IN_GEN]
  