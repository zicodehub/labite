from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship


from app.db.base_class import Base


class TypeProduit(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Produit(Base):
    """
    It represent a answer to a data point for each level_id ( Mas or Country)
    """
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(Integer, ForeignKey('typeproduit.id'))

    commandes = relationship("Commande", back_populates = "produit")


