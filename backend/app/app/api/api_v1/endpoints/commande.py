from typing import Any, List
from app.utils import Genetic

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/genetic")
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100) -> Any:
    """
    Retrieve items.
    """
    f = crud.commande.get_fournisseurs(db = db)
    c = crud.commande.get_clients(db = db)
    d = crud.depot.get_first(db = db)
    print(f"Il y a {len(f)} fourn et {len(c)} clients ")
    
    random.shuffle(f)
    random.shuffle(c)
    
    # list_initial = [d] + f + c + [d]
    list_initial = f + c 
    genetic = Genetic(list_initial)
    return genetic.start()
    return "OK"

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
    # db: Session = Depends(deps.get_db),
    item_in: schemas.CommandeCreate,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = crud.commande.create(obj_in=item_in)
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
    item = crud.commande.remove(id=id)
    return item
