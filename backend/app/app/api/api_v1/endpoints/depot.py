from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Depot])
def read_items(
    # db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100) -> Any:
    """
    Retrieve items.
    """
    items = crud.depot.get_multi(skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Depot)
def create_item(
    *,
    # db: Session = Depends(deps.get_db),
    item_in: schemas.DepotCreate,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = crud.depot.create(obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Depot)
def read_item(
    *,
    # db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.depot.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=schemas.Depot)
def delete_item(
    *,
    # db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.depot.get(id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.depot.remove(id=id)
    return item
