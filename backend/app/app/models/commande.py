from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship


from app.db.base_class import Base

class Commande(Base):
    """
    It represent a answer to a data point for each level_id ( Mas or Country)
    """
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    fournisseur_id = Column(Integer, ForeignKey('fournisseur.id'))
    produit_id = Column(Integer, ForeignKey('produit.id'))
    qty = Column(Integer)
    qty_fixed = Column(Integer)
    is_delivered = Column(Boolean())

    produit = relationship("Produit", back_populates = "commandes")
    holdings = relationship("HoldedOrder", back_populates = "commande")


