from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from repositories.mision_repository import MisionRepository
from services.mision_service import MisionService
from dto.mision_dto import MisionCreate, MisionUpdate, MisionResponse
from RPGqueue.misionFIFO import MisionQueue

router = APIRouter(
    prefix="/misiones",
    tags=["Misiones"]
)

# Dependencias
def get_mission_queue():
    return MisionQueue()

def get_mision_service(db: Session = Depends(get_db), queue: MisionQueue = Depends(get_mission_queue)):
    repository = MisionRepository(db)
    return MisionService(repository, queue)

@router.get("/", response_model=List[MisionResponse])
def get_all_misiones(
    skip: int = 0, 
    limit: int = 100, 
    service: MisionService = Depends(get_mision_service)
):
    """Obtener todas las misiones"""
    return service.get_all_misiones(skip, limit)

@router.get("/{mision_id}", response_model=MisionResponse)
def get_mision(
    mision_id: int, 
    service: MisionService = Depends(get_mision_service)
):
    """Obtener una misión por su ID"""
    mision = service.get_mision_by_id(mision_id)
    if mision is None:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    return mision

@router.post("/", response_model=MisionResponse, status_code=status.HTTP_201_CREATED)
def create_mision(
    mision: MisionCreate, 
    service: MisionService = Depends(get_mision_service)
):
    """Crear una nueva misión"""
    return service.create_mision(mision)

@router.put("/{mision_id}", response_model=MisionResponse)
def update_mision(
    mision_id: int, 
    mision: MisionUpdate, 
    service: MisionService = Depends(get_mision_service)
):
    """Actualizar una misión existente"""
    updated_mision = service.update_mision(mision_id, mision)
    if updated_mision is None:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    return updated_mision

@router.delete("/{mision_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mision(
    mision_id: int, 
    service: MisionService = Depends(get_mision_service)
):
    """Eliminar una misión"""
    success = service.delete_mision(mision_id)
    if not success:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    return None

@router.post("/{mision_id}/asignar/{personaje_id}", status_code=status.HTTP_200_OK)
def asignar_personaje(
    mision_id: int, 
    personaje_id: int, 
    service: MisionService = Depends(get_mision_service)
):
    """Asignar un personaje a una misión"""
    success = service.assign_personaje_to_mision(mision_id, personaje_id)
    if not success:
        raise HTTPException(status_code=404, detail="No se pudo realizar la asignación")
    return {"message": "Personaje asignado correctamente a la misión"}

@router.get("/next-mission", response_model=MisionResponse)
def get_next_mission(
    service: MisionService = Depends(get_mision_service)
):
    """Obtener la siguiente misión pendiente de la cola"""
    mission = service.get_next_pending_mission()
    if mission is None:
        raise HTTPException(status_code=404, detail="No hay misiones pendientes en la cola")
    return mission
