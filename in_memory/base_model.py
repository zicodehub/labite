from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from configs import Settings

from schemas.config import PK_MNT_METHOD, ModelFilterSchema, FilterAgregationRuleSchema
import json

ModelType = TypeVar("ModelType", bound= "Base")
SchemaType = TypeVar("SchemaType", bound= "BaseModel")

class Base(Generic[ModelType, SchemaType]):
    '''
    Attributes to implement

        _ID: int = 1
        DATA_DICT: Dict[Any,object] = {}
    '''
    SCHEMA: BaseModel

    def __init__(self, datum: Dict[str, Any]):
        """
        Base class inherited by all models
        """
        self._create(datum)
        
    def _create(self, datum: Dict[str, Any]):
        self.raw_datum = datum
        self.datum: SchemaType = self._serialize()  
        self._merge_attributes()      
        self._commit()
        self._register_relations()

    def _serialize(self) -> SchemaType:
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
            raise Exception(f"PK key {pk} already set. DATASET = ", self.DATA_DICT)
        
        self.DATA_DICT[pk] = self
        self._set_pk(pk)
        self.__class__._increase_pk()

    def _set_pk(self, pk: Any):
        self.id =  pk

    def _get_next_pk(self):
        return self._ID
    
    @classmethod
    def _increase_pk(cls):
        cls._ID += 1
    
    def __str__(self) -> str:
        cp = self.datum.dict()
        cp['id'] = self.id
        return json.dumps(cp)
    
    @classmethod
    def create(cls, datum: Dict[str, Any]) -> ModelType:
        return cls(datum)
    
    @classmethod
    def create_many(cls, data: List[Dict[str, Any]]) -> List[ModelType]:
        return [cls.create(datum) for datum in data]
    
    @classmethod
    def get(cls, pk) -> ModelType:
        res = cls.DATA_DICT.get(pk, None)
        if res is None:
            raise AssertionError(f"{cls.__class__} cannot get element at pk = {pk} ")
        return res
    
    @classmethod
    def list_all(cls) -> List[ModelType]:
        return [cls.DATA_DICT[key] for key in cls.DATA_DICT]
    
    @classmethod
    def filter(cls, 
               filters: List[ModelFilterSchema], 
               rule: FilterAgregationRuleSchema = FilterAgregationRuleSchema.AND,
               bypass_type_checking = False) -> List[ModelType]:
        '''
        Filter among criterias with and

        *filters: [
            {
                'field': 'name',
                'operator': '==',
                'value': 3
            },
        ]
        '''
        results = []
        for pk in cls.DATA_DICT:
            datum = cls.DATA_DICT[pk]
            found: bool = False
           
            for index, criteria in enumerate(filters):
                datum_field = getattr(datum, criteria.field)
                if not bypass_type_checking:
                    if type(datum_field) != type(criteria.value):
                        raise AssertionError(f"type(datum_field) != type(criteria.value). Types are {type(datum_field)} != {type(criteria.value)}")
                    
                if criteria.format is not None:
                    if criteria.format == "count":
                        datum_field = len(datum_field)
                    else: 
                        raise Exception(f" 'criteria.format = {criteria.format}' non pris en compte  ")
                query = f"{datum_field}{criteria.operator}{criteria.value}"
                if eval(query) is True:
                    if rule == FilterAgregationRuleSchema.OR:
                        found = True
                        continue

                    # Pour la rule AND, on attend que le dernier critère soit satisfait avant de conclure
                    # Dès qu'un critère n'est du AND n'est pas respecté, la condition suivante n'estv même pas évalué   
                    elif rule == FilterAgregationRuleSchema.AND and index+1 == len(filters):
                        found = True
                else:
                    if rule == FilterAgregationRuleSchema.AND:
                        break

            if found:
                results.append(datum)

        return results
        

    @classmethod
    def delete(cls, pk) -> ModelType:
        obj = cls.DATA_DICT.get(pk, None)
        if obj is None:
            raise Exception("PK does not exists")
        
        del cls.DATA_DICT[pk]
        return obj
    
    @classmethod
    def reset_db(cls):
        cls._ID = 1
        cls.DATA_DICT = {}