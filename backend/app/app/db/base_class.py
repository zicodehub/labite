from typing import Any

from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.ext.declarative import as_declarative, declared_attr
# from sqlalchemy_searchable import make_searchable

@as_declarative()
class Base:
    is_active = Column(Boolean(), default=True)
    
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# make_searchable(Base.metadata)