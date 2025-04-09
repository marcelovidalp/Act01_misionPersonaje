from pydantic import BaseModel, Field
from typing import Optional, List

class PersonajeBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    clase: str = Field(..., min_length=2, max_length=50)

class PersonajeCreate(PersonajeBase):
    pass

class PersonajeUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    clase: Optional[str] = Field(None, min_length=2, max_length=50)
    nivel: Optional[int] = None
    experiencia: Optional[int] = None

class PersonajeResponse(PersonajeBase):
    id: int
    nivel: int
    experiencia: int
    
    class Config:
        from_attributes = True
