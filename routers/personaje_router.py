from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from repositories.personaje_repository import PersonajeRepository
from repositories.mision_repository import MisionRepository
from services.personaje_service import PersonajeService
from dto.personaje_dto import PersonajeCreate, PersonajeUpdate, PersonajeResponse
from dto.mision_dto import MisionResponse
from RPGqueue.personaje_mision_queue import PersonajeMisionQueue

router = APIRouter(
    prefix="/personajes",
    tags=["Personajes"]
)

# Dependencias
def get_personaje_service(db: Session = Depends(get_db)):
    personaje_repo = PersonajeRepository(db)
    mision_repo = MisionRepository(db)
    queue = PersonajeMisionQueue()
    return PersonajeService(personaje_repo, mision_repo, queue)

@router.get("/", response_model=List[PersonajeResponse])
def get_all_personajes(
    skip: int = 0, 
    limit: int = 100, 
    service: PersonajeService = Depends(get_personaje_service)
):
    """Obtener todos los personajes"""
    return service.get_all_personajes(skip, limit)

@router.get("/{personaje_id}", response_model=PersonajeResponse)
def get_personaje(
    personaje_id: int, 
    service: PersonajeService = Depends(get_personaje_service)
):
    """Obtener un personaje por su ID"""
    personaje = service.get_personaje_by_id(personaje_id)
    if personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return personaje

@router.post("/", response_model=PersonajeResponse, status_code=status.HTTP_201_CREATED)
async def create_personaje(
    personaje: PersonajeCreate,
    service: PersonajeService = Depends(get_personaje_service)
):
    """
    Crear nuevo personaje
    
    - **nombre**: Nombre del personaje (obligatorio)
    - **clase**: Clase del personaje (guerrero, mago, arquero, etc.) (obligatorio)
    """
    return service.create_personaje(personaje)

@router.put("/{personaje_id}", response_model=PersonajeResponse)
def update_personaje(
    personaje_id: int, 
    personaje: PersonajeUpdate, 
    service: PersonajeService = Depends(get_personaje_service)
):
    """Actualizar un personaje existente"""
    updated_personaje = service.update_personaje(personaje_id, personaje)
    if updated_personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return updated_personaje

@router.delete("/{personaje_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_personaje(
    personaje_id: int, 
    service: PersonajeService = Depends(get_personaje_service)
):
    """Eliminar un personaje"""
    success = service.delete_personaje(personaje_id)
    if not success:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return None

@router.post("/{personaje_id}/misiones/{mision_id}", status_code=status.HTTP_200_OK)
async def accept_mission(
    personaje_id: int,
    mision_id: int,
    service: PersonajeService = Depends(get_personaje_service)
):
    """
    Aceptar misión (encolar)
    
    Asigna una misión a un personaje y la añade a su cola FIFO
    """
    success = service.accept_mission(personaje_id, mision_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="No se pudo aceptar la misión. Verifica que el personaje y la misión existan y que la misión esté pendiente."
        )
    return {"message": "Misión aceptada exitosamente", "personaje_id": personaje_id, "mision_id": mision_id}

@router.post("/{personaje_id}/completar", response_model=MisionResponse)
async def complete_mission(
    personaje_id: int,
    service: PersonajeService = Depends(get_personaje_service)
):
    """
    Completar misión (desencolar + sumar XP)
    
    Completa la primera misión en la cola FIFO del personaje y le otorga experiencia
    """
    mission = service.complete_mission(personaje_id)
    if not mission:
        raise HTTPException(
            status_code=404, 
            detail="No hay misiones pendientes para completar o el personaje no existe."
        )
    return mission

@router.get("/{personaje_id}/misiones", response_model=List[MisionResponse])
async def get_personaje_missions(
    personaje_id: int,
    service: PersonajeService = Depends(get_personaje_service)
):
    """
    Listar misiones en orden FIFO
    
    Muestra todas las misiones asignadas al personaje en orden FIFO
    """
    personaje = service.get_personaje_by_id(personaje_id)
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
        
    return service.get_personaje_misiones(personaje_id)
