from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.db.session import SessionLocal, get_db

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

db = get_db().send(None)
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
    def get(self, id: Any, db: Session = db) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_first(self, db: Session = db) -> Optional[ModelType]:
        return db.query(self.model).first()

    def get_multi(
        self, *, skip: int = 0, limit: int = 100, db: Session = db
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_all(
        self, db: Session = db
    ) -> List[ModelType]:
        return db.query(self.model).all()

    def create(self, obj_in: CreateSchemaType, db: Session = db) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        # if isinstance(obj_in, dict):
        #     obj_in_data = obj_in
        # else:
        #     obj_in_data = obj_in.dict(exclude_unset=True)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        db: Session = db
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, id: int, db: Session = db) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def deactivate(
        self, id: int, db: Session = db
    ) -> ModelType :
        obj = db.query(self.model).get(id)
        obj.is_active = False
        db.commit()
        return obj

    def activate(
        self, id: int, db: Session = db
    ) -> ModelType :
        obj = db.query(self.model).get(id)
        obj.is_active = True
        db.commit()
        return obj