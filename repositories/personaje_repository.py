from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from models.Personaje import Personaje
from models.MisionPersonaje import MisionPersonaje
from dto.personaje_dto import PersonajeCreate, PersonajeUpdate

class PersonajeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Personaje]:
        return self.db.query(Personaje).offset(skip).limit(limit).all()
    
    def get_by_id(self, personaje_id: int) -> Optional[Personaje]:
        return self.db.query(Personaje).filter(Personaje.id == personaje_id).first()
    
    def create(self, personaje: PersonajeCreate) -> Personaje:
        db_personaje = Personaje(**personaje.model_dump())
        self.db.add(db_personaje)
        self.db.commit()
        self.db.refresh(db_personaje)
        return db_personaje
    
    def update(self, personaje_id: int, personaje: PersonajeUpdate) -> Optional[Personaje]:
        db_personaje = self.get_by_id(personaje_id)
        if db_personaje is None:
            return None
        
        update_data = personaje.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_personaje, key, value)
        
        self.db.commit()
        self.db.refresh(db_personaje)
        return db_personaje
    
    def delete(self, personaje_id: int) -> bool:
        db_personaje = self.get_by_id(personaje_id)
        if db_personaje is None:
            return False
        
        self.db.delete(db_personaje)
        self.db.commit()
        return True
    
    def add_experience(self, personaje_id: int, experience: int) -> Optional[Personaje]:
        """Añade experiencia a un personaje y sube de nivel si corresponde"""
        db_personaje = self.get_by_id(personaje_id)
        if db_personaje is None:
            return None
        
        db_personaje.experiencia += experience
        
        # Implementar lógica de subida de nivel
        # Por cada 100 puntos de experiencia, el personaje sube un nivel
        new_level = db_personaje.experiencia // 100 + 1
        if new_level > db_personaje.nivel:
            db_personaje.nivel = new_level
        
        self.db.commit()
        self.db.refresh(db_personaje)
        return db_personaje
    
    def get_misiones(self, personaje_id: int) -> List[MisionPersonaje]:
        """Obtiene todas las misiones asignadas a un personaje"""
        return self.db.query(MisionPersonaje).filter(
            MisionPersonaje.personaje_id == personaje_id
        ).options(joinedload(MisionPersonaje.mision)).all()
