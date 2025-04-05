from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from .Base import Base

class Personaje(Base):
    __tablename__ = 'personajes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    nivel = Column(Integer, default=1)
    clase = Column(String(50), nullable=False)
    experiencia = Column(Integer, default=0)
    
    mision_personaje = relationship("MisionPersonaje", back_populates="personaje")

