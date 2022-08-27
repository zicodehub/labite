from calendar import c
from app.db.session import SessionLocal
from app import models, crud

db = SessionLocal()

orders = crud.commande.get_all(db)
for o in orders:
    o.qty = o.qty_fixed
    db.add(o)
    db.commit()

for h in db.query(models.HoldedOrder).all():
    db.delete(h)
    db.commit()

for c in db.query(models.Compartiment).all():
    db.delete(c)
    db.commit()

for v in db.query(models.Vehicule).all():
    v.trajet = []
    db.add(v)
    db.commit()

# db.add(hold)
# db.commit()