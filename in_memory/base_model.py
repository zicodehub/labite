from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from configs import Settings

from schemas.config import PK_MNT_METHOD

ModelType = TypeVar("ModelType", bound= "Base")

class Base(Generic[ModelType]):
    _ID: int = 1
    DATA_DICT: Dict[Any,object] = {}
    SCHEMA: BaseModel

    def __init__(self, datum: Dict[str, Any]):
        """
        Base class inherited by all models
        """
        self._create(datum)
        
    def _create(self, datum: Dict[str, Any]):
        self.raw_datum = datum
        self.datum = self._serialize()  
        self._merge_attributes()      
        self._register_relations()
        self._commit()

    def _serialize(self):
        return self.SCHEMA(**self.raw_datum)
    
    def _merge_attributes(self):
        for field in self.SCHEMA.__fields__:
            value = getattr(self.datum, field)
            setattr(self, field, value)
    
    def _register_relations(self):
        pass

    def _commit(self):
        if Settings.PK_MANAGER == PK_MNT_METHOD.SERIAL:
            pk = self._get_next_pk()
        elif Settings.PK_MANAGER == PK_MNT_METHOD.MANUAL:
            pk = self.raw_datum.get('id')
            if not pk:
                raise Exception(f"Manual Primary Key not set")
        else: 
            raise Exception("Settings.PK_MANAGER not coherent")
    
        # Ensure no one already holds this pk
        if self.DATA_DICT.get(pk, None) is not None:
            raise Exception(f"PK key {pk} already set")
        
        self.DATA_DICT[pk] = self
        self._set_pk(pk)
        self._increase_pk()

    def _set_pk(self, pk: Any):
        self.id =  pk

    def _get_next_pk(self):
        return self._ID
    
    @classmethod
    def _increase_pk(cls):
        cls._ID += 1
    
    def __str__(self) -> str:
        return self.datum.json()
    
    @classmethod
    def create(cls, datum: Dict[str, Any]) -> ModelType:
        return cls(datum)
    
    @classmethod
    def create_many(cls, data: List[Dict[str, Any]]) -> List[ModelType]:
        return [cls.create(datum) for datum in data]
    
    @classmethod
    def get(cls, pk) -> ModelType:
        return cls.DATA_DICT[pk]
    
    @classmethod
    def list_all(cls) -> List[ModelType]:
        return [cls.DATA_DICT[key] for key in cls.DATA_DICT]
    
    @classmethod
    def delete(cls, pk) -> ModelType:
        obj = cls.DATA_DICT.get(pk, None)
        if obj is None:
            raise Exception("PK does not exists")
        
        del cls.DATA_DICT[pk]
        return obj