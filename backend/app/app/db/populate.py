from calendar import c
from app.db.session import SessionLocal
from app import models, crud
from random import randint
db = SessionLocal()

# print(comp.holded_orders[0].commande)
# comp = models.Compartiment(vehicule_id = 1)
# db.add(comp)
# db.commit()
# db.refresh(comp)
# comp = db.query(models.Compartiment).all()[-1]
# print(comp.vehicule_id, comp.id)



for i in range(5):
    
    crud.client.create()