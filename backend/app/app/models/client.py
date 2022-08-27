from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship


from app.db.base_class import Base


class Client(Base):
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

    # ma_id = Column(Integer, ForeignKey('ma.id'))

