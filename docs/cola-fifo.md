# Sistema de Cola FIFO para Misiones

El sistema implementa un patrón de cola FIFO (First In, First Out) para gestionar las misiones de los personajes. Esto permite que las misiones se completen en el orden en que fueron asignadas, simulando una lista de tareas para cada personaje.

## Implementaciones de Cola FIFO

El sistema cuenta con dos implementaciones de cola FIFO:

1. **Cola General de Misiones** (`misionFIFO.py`): Gestiona todas las misiones pendientes en el sistema.
2. **Cola de Misiones por Personaje** (`personaje_mision_queue.py`): Gestiona las misiones asignadas a cada personaje específico.

## Cola General de Misiones

```python
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
```

## Cola de Misiones por Personaje

```python
class PersonajeMisionQueue:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonajeMisionQueue, cls).__new__(cls)
            cls._instance.queues = {}
        return cls._instance
    
    def get_queue(self, personaje_id: int) -> deque:
        """Obtiene la cola de misiones para un personaje específico"""
        if personaje_id not in self.queues:
            self.queues[personaje_id] = deque()
        return self.queues[personaje_id]
```

## Flujo de trabajo de las Misiones

### 1. Creación de Misión

Cuando se crea una misión, esta se establece inicialmente con estado "pendiente" y se añade a la cola general de misiones.

```python
def create_mision(self, mision: MisionCreate) -> MisionResponse:
    db_mision = self.repository.create(mision)
    # Al crear una misión, la añadimos a la cola de misiones pendientes
    self.queue.enqueue(db_mision)
    return MisionResponse.from_orm(db_mision)
```

### 2. Asignación de Misión a Personaje

Cuando un personaje acepta una misión:

1. La misión se extrae de la cola general.
2. El estado de la misión cambia a "en_progreso".
3. La misión se añade a la cola específica del personaje.

```python
def accept_mission(self, personaje_id: int, mision_id: int) -> bool:
    # Verificar que el personaje y la misión existen
    personaje = self.personaje_repository.get_by_id(personaje_id)
    mision = self.mision_repository.get_by_id(mision_id)
    
    if not personaje or not mision:
        return False
    
    # Verificar que la misión está pendiente
    if mision.estado != EstadoMision.PENDIENTE:
        return False
    
    # Asignar la misión al personaje
    self.mision_repository.asignar_personaje(mision_id, personaje_id)
    
    # Cambiar estado de la misión
    self.mision_repository.update(mision_id, {"estado": EstadoMision.EN_PROGRESO})
    
    # Agregar a la cola del personaje
    self.mision_queue.enqueue(personaje_id, mision)
    
    return True
```

### 3. Completar Misión

Cuando un personaje completa una misión:

1. La misión se extrae de la cola del personaje (siempre la primera que entró).
2. El estado de la misión cambia a "completada".
3. El personaje recibe la experiencia asociada a la misión.

```python
def complete_mission(self, personaje_id: int) -> Optional[MisionResponse]:
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
```

## Ventajas del Sistema de Cola FIFO

1. **Orden garantizado**: Las misiones se procesan en el mismo orden en que fueron asignadas.
2. **Sistema justo**: Asegura que todas las misiones se completen eventualmente.
3. **Simplicidad**: Es fácil de entender y de implementar.
4. **Eficiencia**: Las operaciones de enqueue y dequeue son O(1).

## Limitaciones

1. **No hay priorización**: Todas las misiones tienen la misma prioridad, independientemente de su dificultad o recompensa.
2. **Estado global**: El estado de la cola se mantiene en memoria, lo que podría ser un problema en caso de reinicio del sistema.

## Casos de Uso

- **Listar misiones pendientes**: Permite al jugador ver qué misiones tiene pendientes por completar.
- **Aceptar nueva misión**: Añade una misión a la cola del personaje.
- **Completar misión actual**: Completa la misión más antigua en la cola y concede la experiencia al personaje.
