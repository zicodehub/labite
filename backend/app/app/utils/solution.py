from math import sqrt
from app.models.client import Client
from app.models.fournisseur import Fournisseur
from app.core.config import settings
from app import crud, models
from app.db.session import SessionLocal
from typing import List
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

