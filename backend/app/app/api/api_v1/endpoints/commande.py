from typing import Any, List
from app.utils import Genetic, RecuitSimule

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/reset-db")
def reset_the_db(
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    from app.db import reset_db
    reset_db.clean()
    return True
    
@router.get("/recuit")
def read_recuit(
    db: Session = Depends(deps.get_db),
   ) -> Any:
    """
    Retrieve items.
    """
    print("Running Recuit Simulé")
    from app.db import reset_db
    solutions_finales = []
    reset_db.clean(db)
    
    f = crud.commande.get_fournisseurs(db = db)
    c = crud.commande.get_clients(db = db)
    d = crud.depot.get_first(db = db)
    #printf"Il y a {len(f)} fourn et {len(c)} clients ")
    
    random.shuffle(f)
    random.shuffle(c)
    
    # list_initial = [d] + f + c + [d]
    list_initial = f + c 
    try :
        recuit = RecuitSimule(list_initial, db= db)
        res = recuit.start()
        solutions_finales.append(res)
        db.close_all()
    except Exception as e:
        #print"Exception API::: ", e)
        db.close_all()
        raise e
        return HTTPException(status_code=500, detail= e)

    return solutions_finales



@router.get("/genetic")
def read_genetic(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100) -> Any:
    """
    Retrieve items.
    """
    print("Running Génétic")
    from app.db import reset_db
    solutions_finales = []
    for i in range(Genetic.SAMPLE_SOLUTIONS):
        reset_db.clean(db)
        f = crud.commande.get_fournisseurs(db = db)
        c = crud.commande.get_clients(db = db)
        d = crud.depot.get_first(db = db)
        #printf"Il y a {len(f)} fourn et {len(c)} clients ")
        
        random.shuffle(f)
        random.shuffle(c)
        
        # list_initial = [d] + f + c + [d]
        list_initial = f + c 
        try :
            genetic = Genetic(list_initial, db= db)
            res = genetic.start()
            db.close_all()
            solutions_finales.append(res)
        except Exception as e:
            #print"Exception API::: ", e)
            db.close_all()
            raise e
            return HTTPException(status_code=500, detail= e)

    return solutions_finales

@router.get("/", response_model=List[schemas.Commande])
def read_items(
    # db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100) -> Any:
    """
    Retrieve items.
    """
    items = crud.commande.get_multi()
    return items


@router.post("/", response_model=schemas.Commande)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.CommandeCreate,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = crud.commande.create(obj_in=item_in, db= db)
    return item


@router.get("/{id}", response_model=schemas.Commande)
def read_item(
    *,
    # db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.commande.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=schemas.Commande)
def delete_item(
    *,
    # db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.commande.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for h in item.holdings:
        crud.vehicule.remove_holded_order(h)
        
    item = crud.commande.remove(id=id)
    return item
