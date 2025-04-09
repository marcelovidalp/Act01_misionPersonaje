from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class MisionPersonaje(Base):
    __tablename__ = 'mision_personaje'
    id = Column(Integer, primary_key=True)
    mision_id = Column(Integer, ForeignKey('misiones.id'), nullable=False)
    personaje_id = Column(Integer, ForeignKey('personajes.id'), nullable=False)

    mision = relationship("Mision", back_populates="mision_personaje")
    personaje = relationship("Personaje", back_populates="mision_personaje")