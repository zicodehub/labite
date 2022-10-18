from typing import List
from app.db.session import SessionLocal

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.commande import Commande
from app.schemas.commande import CommandeCreate, CommandeUpdate
from app import models, crud
from app.db.session import SessionLocal, get_db

db: Session = get_db().send(None)

class CRUDItem(CRUDBase[Commande, CommandeCreate, CommandeUpdate]):
    def create(self, obj_in: CommandeCreate, db: db) -> Commande:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, qty_fixed = obj_in_data['qty'])  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def decrease_qty(self, db: Session, order: Commande, value: int = 1) -> Commande:
        order.qty -= value
        local_object = db.merge(order)
        db.add(local_object)
        db.commit()
        db.refresh(local_object)
        return local_object

    def must_deliver_client(self, db: Session, f: models.Fournisseur, client: models.Client) -> bool:
        return db.query(self.model).filter(
                self.model.fournisseur_id == f.id, self.model.client_id == client.id)\
            .count() > 0
    
    def get_fournisseurs(self, db: Session = db) -> List[models.Fournisseur]:
        return db.query(models.Fournisseur).join(models.Commande).distinct().all()

    def get_clients(self, db: Session = db) -> List[models.Fournisseur]:
        return db.query(models.Client).join(models.Commande).distinct().all()
    
    
    def get_by_fournisseur(self, f: models.Fournisseur, db: Session = db) -> List[models.Commande]:
        return db.query(self.model).filter(
                self.model.fournisseur_id == f.id).all()

    def get_by_client(self, client: models.Client, db: Session = db) -> List[models.Commande]:
        return db.query(self.model).filter(
                self.model.client_id == client.id).all()
    
    def get_fournisseurs_for_client(self, client: models.Client, db: Session = db) -> List[models.Fournisseur]:
        return db.query(models.Fournisseur).join(models.Commande).filter(self.model.client_id == client.id).distinct().all()

    def get_clients_for_fournisseur(self, f: models.Fournisseur, db: Session = db) -> List[models.Client]:
        return db.query(models.Client).join(models.Commande).filter(self.model.fournisseur_id == f.id).distinct().all()


commande = CRUDItem(Commande)
