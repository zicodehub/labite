from typing import Tuple
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.tests.utils.utils import random_email, random_lower_string

from app.core.security import verify_password
from app import models, schemas, crud
from app.tests.utils.utils import random_email, random_lower_string

def test_country_affectation(db: Session) -> None:
    ctx = schemas.CountryCreate(name= "A little country", is_active= True)
    country =  crud.country.create(db, obj_in= ctx) 

    users = []
    for _ in range(3) :
        user_in = models.UserCreate(email=random_email(), password= random_lower_string())
        users.append(crud.user.create(db, obj_in= user_in))

    ma_ = schemas.MaCreate(name= "Some MA", country_id = country.id, is_active = True)
    ma = crud.ma.create_with_admins(db, obj_in= ma_, admins= users)

    related_mas = crud.ma.get_related_to_me(db, id_user= users[2].id)
    
    for m in related_mas:
        for u in users :
            assert crud.ma.is_affected(db, m.id, id_user= u.id)

def test_country_activation(db: Session) -> None:
    ma_ = schemas.MaCreate(name= "Another MA", is_active= True)
    ma = crud.ma.create(db, obj_in= ma_)
    assert ma.is_active == True

    ma = crud.ma.deactivate(db, id= ma.id)
    assert ma.name == ma_.name
    assert ma.is_active == False

    ma = crud.ma.activate(db, id= ma.id)
    assert ma.name == ma_.name
    assert ma.is_active == True
