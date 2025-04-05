from collections import deque
from typing import List, Optional
from ..models.Mision import Mision
from ..dto.mision_dto import EstadoMision

class MisionQueue:
    def __init__(self):
        self.queue = deque()
        
    def enqueue(self, mision: Mision) -> None:
        """Añade una misión a la cola"""
        if mision.estado == "pendiente":
            self.queue.append(mision)
            
    def dequeue(self) -> Optional[Mision]:
        """Obtiene la siguiente misión pendiente"""
        if self.is_empty():
            return None
        return self.queue.popleft()
    
    def peek(self) -> Optional[Mision]:
        """Ver la siguiente misión sin sacarla de la cola"""
        if self.is_empty():
            return None
        return self.queue[0]
    
    def is_empty(self) -> bool:
        """Verifica si la cola está vacía"""
        return len(self.queue) == 0
    
    def size(self) -> int:
        """Devuelve el tamaño de la cola"""
        return len(self.queue)
    
    def clear(self) -> None:
        """Vacía la cola"""
        self.queue.clear()
        
    def load_pending_missions(self, missions: List[Mision]) -> None:
        """Carga todas las misiones pendientes en la cola"""
        for mission in missions:
            if mission.estado == "pendiente":
                self.enqueue(mission)
