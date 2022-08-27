from calendar import c
from app.db.session import SessionLocal
from app import models, crud

db = SessionLocal()

# print(comp.holded_orders[0].commande)
comp = models.Compartiment(vehicule_id = 1)
db.add(comp)
db.commit()
db.refresh(comp)
comp = db.query(models.Compartiment).all()[-1]
print(comp.vehicule_id, comp.id)
# hold = models.HoldedOrder(commande_id= 19, compartiment_id= comp.id, qty_holded= 3)
# hold = db.query(models.HoldedOrder).first()

# print(comp.holded_orders[0].commande)
# comp.holded_orders.append()

# db.add(hold)
# db.commit()