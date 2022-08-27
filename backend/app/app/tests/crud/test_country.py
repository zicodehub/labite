from typing import Tuple
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.tests.utils.utils import random_email, random_lower_string

from app.core.security import verify_password
from app import models, schemas, crud
from app.tests.utils.utils import random_email, random_lower_string

def test_country_affectation(db: Session) -> None:
    countries = []
    country_names = ["Lune", "Soleil", "Mercure"]
    for name in country_names :
        ctx = schemas.CountryCreate(name= name, is_active= True)
        countries.append( crud.country.create(db, obj_in= ctx) )

    users = []
    for _ in range(3) :
        user_in = models.UserCreate(email=random_email(), password= random_lower_string())
        users.append(crud.user.create(db, obj_in= user_in))

    crud.country.create_with_admins(db, countries= countries, admins= users )

    related_countries = crud.country.get_related_to_me(db, id_user= users[0].id)
    
    for ctx in related_countries:
        for u in users :
            assert crud.country.is_affected(db, id_country= ctx.id, id_user= u.id)

def test_country_activation(db: Session) -> None:
    ctx = schemas.CountryCreate(name= "Some city", is_active= True)
    country = crud.country.create(db, obj_in= ctx)
    assert country.is_active == True

    country = crud.country.deactivate(db, id= country.id)
    assert country.name == ctx.name
    assert country.is_active == False

    country = crud.country.activate(db, id= country.id)
    assert country.name == ctx.name
    assert country.is_active == True
