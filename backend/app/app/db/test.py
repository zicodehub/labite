from calendar import c
from app.db.session import SessionLocal
from app import models, crud

db = SessionLocal()


for v in crud.vehicule.get_all():
    print(f"Véhicule {v.id}, Nb compartiment usés: {len(v.compartiments)} ")
    for order in crud.commande.get_all():
        # print(order, prod, vehicule)
        prod = crud.produit.get(order.produit_id)
        can_hold = crud.vehicule.can_hold(v, prod, order.qty)
        print(f"Can hold ({can_hold}/{v.nb_compartment * v.size_compartment}) for order {order.id} -> {order.qty}  ")
        qty_holded = crud.vehicule.hold(v, order)
        print(f"Quantité chargée : {qty_holded} / {order.qty} ")

# order = db.query(models.Commande).get(13)
# prod = crud.produit.get(order.produit_id)
# vehicule = db.query(models.Vehicule).get(1)
# print(f"Nb compartiment : {len(vehicule.compartiments)} ")
# # print(order, prod, vehicule)
# can_hold = crud.vehicule.can_hold(vehicule, prod, order.qty)
# print(f"Can hold ({can_hold}/{vehicule.nb_compartment*vehicule.size_compartment}) for order {order.qty}  ")
# qty_holded = crud.vehicule.hold(vehicule, order)
# print(f"Quantité chargée : {qty_holded} / {order.qty} ")

# db.add(hold)
# db.commit()