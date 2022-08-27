from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


from app.db.base_class import Base

association_fournisseur_produit = Table('association_fournisseur_produit', Base.metadata,
    Column('produit_id', ForeignKey('produit.id'), primary_key=True),
    Column('fournisseur_id', ForeignKey('fournisseur.id'), primary_key=True),
    Column('qty', Integer)
)

class Fournisseur(Base):
    """
    It represent a answer to a data point for each level_id ( Mas or Country)
    """
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    name = Column(String)
    coords = Column(String)
    time_service = Column(Integer)
    time_interval_start = Column(Integer)
    time_interval_end = Column(Integer)

    commandes = relationship("Commande")
    produits = relationship("Produit", secondary = association_fournisseur_produit)


