from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


# @router.get("/", response_model=List[schemas.Fournisseur])
@router.get("/", response_model=List[schemas.Fournisseur])
def read_items(
    # db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100) -> Any:
    """
    Retrieve items.
    """
    items = crud.fournisseur.get_multi(skip=skip, limit=limit)
    print(dir(items[0]))
    return items


@router.post("/", response_model=schemas.Fournisseur)
def create_item(
    *,
    # db: Session = Depends(deps.get_db),
    item_in: schemas.FournisseurCreate,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = crud.fournisseur.create(obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Fournisseur)
def read_item(
    *,
    # db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.fournisseur.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=schemas.Fournisseur)
def delete_item(
    *,
    # db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.fournisseur.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.fournisseur.remove(id=id)
    return item
