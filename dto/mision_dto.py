from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class EstadoMision(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"

class MisionBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    descripcion: str = Field(..., min_length=10, max_length=200)
    experiencia: int = Field(..., gt=0)

class MisionCreate(MisionBase):
    pass

class MisionUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50)
    descripcion: Optional[str] = Field(None, min_length=10, max_length=200)
    experiencia: Optional[int] = Field(None, gt=0)
    estado: Optional[EstadoMision] = None

class MisionResponse(MisionBase):
    id: int
    estado: EstadoMision
    fecha_inicio: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True
