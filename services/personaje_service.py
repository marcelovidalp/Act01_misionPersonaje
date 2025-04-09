from typing import List, Optional
from repositories.personaje_repository import PersonajeRepository
from repositories.mision_repository import MisionRepository
from dto.personaje_dto import PersonajeCreate, PersonajeUpdate, PersonajeResponse
from dto.mision_dto import MisionResponse, EstadoMision
from RPGqueue.personaje_mision_queue import PersonajeMisionQueue

class PersonajeService:
    def __init__(self, 
                personaje_repository: PersonajeRepository, 
                mision_repository: MisionRepository,
                mision_queue: PersonajeMisionQueue):
        self.personaje_repository = personaje_repository
        self.mision_repository = mision_repository
        self.mision_queue = mision_queue
    
    def get_all_personajes(self, skip: int = 0, limit: int = 100) -> List[PersonajeResponse]:
        personajes = self.personaje_repository.get_all(skip, limit)
        return [PersonajeResponse.model_validate(personaje) for personaje in personajes]
    
    def get_personaje_by_id(self, personaje_id: int) -> Optional[PersonajeResponse]:
        personaje = self.personaje_repository.get_by_id(personaje_id)
        if personaje:
            return PersonajeResponse.model_validate(personaje)
        return None
    
    def create_personaje(self, personaje: PersonajeCreate) -> PersonajeResponse:
        db_personaje = self.personaje_repository.create(personaje)
        return PersonajeResponse.model_validate(db_personaje)
    
    def update_personaje(self, personaje_id: int, personaje: PersonajeUpdate) -> Optional[PersonajeResponse]:
        updated_personaje = self.personaje_repository.update(personaje_id, personaje)
        if updated_personaje:
            return PersonajeResponse.model_validate(updated_personaje)
        return None
    
    def delete_personaje(self, personaje_id: int) -> bool:
        return self.personaje_repository.delete(personaje_id)
    
    def accept_mission(self, personaje_id: int, mision_id: int) -> bool:
        """Acepta una misión y la agrega a la cola FIFO del personaje"""
        # Verificar que el personaje y la misión existen
        personaje = self.personaje_repository.get_by_id(personaje_id)
        mision = self.mision_repository.get_by_id(mision_id)
        
        if not personaje or not mision:
            return False
        
        # Verificar que la misión está pendiente
        if mision.estado != "pendiente":
            return False
        
        # Asignar la misión al personaje
        asignacion = self.mision_repository.asignar_personaje(mision_id, personaje_id)
        
        if not asignacion:
            return False
        
        # Cambiar estado de la misión
        self.mision_repository.update(mision_id, {"estado": EstadoMision.EN_PROGRESO})
        
        # Agregar a la cola del personaje
        self.mision_queue.enqueue(personaje_id, mision)
        
        return True
    
    def complete_mission(self, personaje_id: int) -> Optional[MisionResponse]:
        """Completa la siguiente misión en la cola FIFO del personaje"""
        # Verificar que el personaje existe
        personaje = self.personaje_repository.get_by_id(personaje_id)
        if not personaje:
            return None
        
        # Obtener la siguiente misión en la cola
        mision = self.mision_queue.dequeue(personaje_id)
        if not mision:
            return None
        
        # Actualizar estado de la misión
        self.mision_repository.update(mision.id, {"estado": EstadoMision.COMPLETADA})
        
        # Añadir experiencia al personaje
        self.personaje_repository.add_experience(personaje_id, mision.experiencia)
        
        # Devolver la misión completada
        return MisionResponse.from_orm(mision)
    
    def get_personaje_misiones(self, personaje_id: int) -> List[MisionResponse]:
        """Obtiene todas las misiones en la cola FIFO del personaje"""
        # Verificar que el personaje existe
        personaje = self.personaje_repository.get_by_id(personaje_id)
        if not personaje:
            return []
        
        # Obtener todas las misiones en la cola
        misiones = self.mision_queue.get_all(personaje_id)
        
        return [MisionResponse.from_orm(mision) for mision in misiones]
