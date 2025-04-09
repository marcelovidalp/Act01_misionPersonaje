from sqlalchemy.orm import Session
from typing import List, Optional
from models.Mision import Mision
from models.MisionPersonaje import MisionPersonaje
from dto.mision_dto import MisionCreate, MisionUpdate, EstadoMision

class MisionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Mision]:
        return self.db.query(Mision).offset(skip).limit(limit).all()
    
    def get_by_id(self, mision_id: int) -> Optional[Mision]:
        return self.db.query(Mision).filter(Mision.id == mision_id).first()
    
    def get_by_estado(self, estado: EstadoMision) -> List[Mision]:
        return self.db.query(Mision).filter(Mision.estado == estado).all()
    
    def create(self, mision: MisionCreate) -> Mision:
        db_mision = Mision(**mision.model_dump(), estado="pendiente")
        self.db.add(db_mision)
        self.db.commit()
        self.db.refresh(db_mision)
        return db_mision
    
    def update(self, mision_id: int, mision_data: dict) -> Optional[Mision]:
        db_mision = self.get_by_id(mision_id)
        if db_mision is None:
            return None
        
        for key, value in mision_data.items():
            setattr(db_mision, key, value)
        
        self.db.commit()
        self.db.refresh(db_mision)
        return db_mision
    
    def delete(self, mision_id: int) -> bool:
        db_mision = self.get_by_id(mision_id)
        if db_mision is None:
            return False
        
        self.db.delete(db_mision)
        self.db.commit()
        return True
    
    def asignar_personaje(self, mision_id: int, personaje_id: int) -> Optional[MisionPersonaje]:
        # Verificar si ya existe la asignación
        existing = self.db.query(MisionPersonaje).filter(
            MisionPersonaje.mision_id == mision_id,
            MisionPersonaje.personaje_id == personaje_id
        ).first()
        
        if existing:
            return existing
        
        # Crear nueva asignación
        asignacion = MisionPersonaje(mision_id=mision_id, personaje_id=personaje_id)
        self.db.add(asignacion)
        self.db.commit()
        self.db.refresh(asignacion)
        return asignacion
