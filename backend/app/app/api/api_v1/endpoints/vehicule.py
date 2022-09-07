from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Vehicule])
def read_items(
    # db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100) -> Any:
    """
    Retrieve items.
    """
    items = crud.vehicule.get_multi(skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Vehicule)
def create_item(
    *,
    # db: Session = Depends(deps.get_db),
    item_in: schemas.VehiculeCreate,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = crud.vehicule.create(obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Vehicule)
def read_item(
    *,
    # db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.vehicule.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=schemas.Vehicule)
def delete_item(
    *,
    # db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.vehicule.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.vehicule.remove(id=id)
    return item
