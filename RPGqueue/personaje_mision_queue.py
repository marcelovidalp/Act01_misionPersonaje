from collections import deque
from typing import Dict, List, Optional
from models.Mision import Mision

class PersonajeMisionQueue:
    """
    Implementa el patrón Singleton para gestionar colas FIFO de misiones por personaje
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonajeMisionQueue, cls).__new__(cls)
            cls._instance.queues = {}  # Dict[int, deque]
        return cls._instance
    
    def get_queue(self, personaje_id: int) -> deque:
        """Obtiene la cola de misiones para un personaje específico"""
        if personaje_id not in self.queues:
            self.queues[personaje_id] = deque()
        return self.queues[personaje_id]
    
    def enqueue(self, personaje_id: int, mision: Mision) -> None:
        """Añade una misión a la cola de un personaje"""
        queue = self.get_queue(personaje_id)
        queue.append(mision)
    
    def dequeue(self, personaje_id: int) -> Optional[Mision]:
        """Obtiene la siguiente misión pendiente para un personaje"""
        queue = self.get_queue(personaje_id)
        if len(queue) == 0:
            return None
        return queue.popleft()
    
    def peek(self, personaje_id: int) -> Optional[Mision]:
        """Ver la siguiente misión sin sacarla de la cola"""
        queue = self.get_queue(personaje_id)
        if len(queue) == 0:
            return None
        return queue[0]
    
    def get_all(self, personaje_id: int) -> List[Mision]:
        """Obtiene todas las misiones en la cola de un personaje"""
        return list(self.get_queue(personaje_id))
    
    def is_empty(self, personaje_id: int) -> bool:
        """Verifica si la cola de un personaje está vacía"""
        return len(self.get_queue(personaje_id)) == 0
    
    def size(self, personaje_id: int) -> int:
        """Devuelve el tamaño de la cola de un personaje"""
        return len(self.get_queue(personaje_id))
    
    def clear(self, personaje_id: int) -> None:
        """Vacía la cola de un personaje"""
        self.queues[personaje_id] = deque()
