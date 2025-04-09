from typing import List, Optional
from repositories.mision_repository import MisionRepository
from dto.mision_dto import MisionCreate, MisionUpdate, MisionResponse, EstadoMision
from models.Mision import Mision
from RPGqueue.misionFIFO import MisionQueue

class MisionService:
    def __init__(self, repository: MisionRepository, queue: MisionQueue):
        self.repository = repository
        self.queue = queue
    
    def get_all_misiones(self, skip: int = 0, limit: int = 100) -> List[MisionResponse]:
        misiones = self.repository.get_all(skip, limit)
        return [MisionResponse.model_validate(mision) for mision in misiones]
    
    def get_mision_by_id(self, mision_id: int) -> Optional[MisionResponse]:
        mision = self.repository.get_by_id(mision_id)
        if mision:
            return MisionResponse.model_validate(mision)
        return None
    
    def create_mision(self, mision: MisionCreate) -> MisionResponse:
        db_mision = self.repository.create(mision)
        # Al crear una misión, la añadimos a la cola de misiones pendientes
        self.queue.enqueue(db_mision)
        return MisionResponse.model_validate(db_mision)
    
    def update_mision(self, mision_id: int, mision_update: MisionUpdate) -> Optional[MisionResponse]:
        # Convertimos el modelo Pydantic a diccionario
        update_data = mision_update.model_dump(exclude_unset=True)
        
        updated_mision = self.repository.update(mision_id, update_data)
        if updated_mision:
            # Si el estado cambia a completado, manejamos la experiencia
            if update_data.get('estado') == EstadoMision.COMPLETADA:
                self._handle_completed_mission(updated_mision)
            return MisionResponse.model_validate(updated_mision)
        return None
    
    def delete_mision(self, mision_id: int) -> bool:
        return self.repository.delete(mision_id)
    
    def assign_personaje_to_mision(self, mision_id: int, personaje_id: int) -> bool:
        result = self.repository.asignar_personaje(mision_id, personaje_id)
        return result is not None
    
    def get_next_pending_mission(self) -> Optional[MisionResponse]:
        if not self.queue.is_empty():
            next_mission = self.queue.dequeue()
            return MisionResponse.model_validate(next_mission)
        return None
    
    def _handle_completed_mission(self, mission: Mision):
        """Maneja la lógica cuando una misión se completa (dar experiencia a personajes)"""
        # Esta implementación dependería de otros servicios como PersonajeService
        # Por ahora es un método placeholder
        pass
