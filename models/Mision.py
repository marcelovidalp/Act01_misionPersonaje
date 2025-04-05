from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from .Base import Base
from sqlalchemy.orm import relationship


class Mision(Base):
    __tablename__ = 'misiones'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(200), nullable=False)
    experiencia = Column(Integer, nullable=False)
    estado = Column(Enum('pendiente', 'en_progreso', 'completada', name='estado_mision'), nullable=False)
    fecha_inicio = Column(DateTime.now, default=func.now(), nullable=False)
    
    mision_personaje = relationship("MisionPersonaje", back_populates="mision")



