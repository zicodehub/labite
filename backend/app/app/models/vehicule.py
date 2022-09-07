from sqlalchemy import Column, ForeignKey, Integer, String, Float, JSON, Table
from sqlalchemy.orm import relationship


from app.db.base_class import Base

class HoldedOrder(Base):
    commande_id = Column(Integer, ForeignKey('commande.id'), primary_key=True)
    compartiment_id = Column(Integer, ForeignKey('compartiment.id'), primary_key=True)
    qty_holded = Column(Integer)

    commande = relationship("Commande", back_populates = "holdings")
    compartiment = relationship("Compartiment", back_populates = "holded_orders")

class Compartiment(Base):
    id = Column(Integer, primary_key=True, index=True)
    vehicule_id = Column(Integer, ForeignKey("vehicule.id"), nullable=False)
    holded_orders = relationship("HoldedOrder", back_populates= "compartiment")
    vehicule = relationship("Vehicule", back_populates= "compartiments")


class Vehicule(Base):
    """
    It represent a answer to a data point for each level_id ( Mas or Country)
    """
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    velocity = Column(Float)
    code = Column(String)
    nb_compartment = Column(Integer)
    size_compartment = Column(Integer)
    cout = Column(Integer)

    depot_id = Column(Integer, ForeignKey("depot.id"))
    depot = relationship("Depot", back_populates = "vehicules")
    
    trajet = Column(JSON, default= [])
    compartiments = relationship("Compartiment")
    # compartiments = relationship("Compartiment", back_populates = "vehicule")