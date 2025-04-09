# Patrones de Diseño Implementados

Este proyecto implementa varios patrones de diseño para garantizar una arquitectura limpia, mantenible y escalable.

## 1. Patrón Repositorio

El patrón Repositorio se utiliza para separar la lógica que recupera los datos y los mapea al modelo de entidad de la lógica de negocio que actúa sobre el modelo.

### Implementación

- `MisionRepository`: Encapsula el acceso a datos para las misiones.
- `PersonajeRepository`: Encapsula el acceso a datos para los personajes.

### Beneficios

- **Desacoplamiento**: La lógica de negocio depende de abstracciones y no de implementaciones concretas de acceso a datos.
- **Testabilidad**: Facilita el uso de mocks para pruebas unitarias.
- **Coherencia**: Proporciona un punto único de acceso a datos para cada entidad.

### Ejemplo de uso

```python
class MisionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, mision_id: int) -> Optional[Mision]:
        return self.db.query(Mision).filter(Mision.id == mision_id).first()
        
    # Otros métodos de acceso a datos
```

## 2. Patrón Servicio

El patrón Servicio proporciona una capa de abstracción para la lógica de negocio de la aplicación.

### Implementación

- `MisionService`: Encapsula la lógica de negocio relacionada con las misiones.
- `PersonajeService`: Encapsula la lógica de negocio relacionada con los personajes.

### Beneficios

- **Separación de responsabilidades**: Separa la lógica de negocio de los controladores y repositorios.
- **Reutilización de código**: Permite reutilizar la lógica de negocio en diferentes partes de la aplicación.
- **Mantenibilidad**: Facilita el mantenimiento al centralizar la lógica en componentes especializados.

### Ejemplo de uso

```python
class MisionService:
    def __init__(self, repository: MisionRepository, queue: MisionQueue):
        self.repository = repository
        self.queue = queue
    
    def create_mision(self, mision: MisionCreate) -> MisionResponse:
        db_mision = self.repository.create(mision)
        self.queue.enqueue(db_mision)
        return MisionResponse.from_orm(db_mision)
```

## 3. Patrón Singleton

El patrón Singleton garantiza que una clase tenga solo una instancia y proporciona un punto de acceso global a ella.

### Implementación

- `PersonajeMisionQueue`: Implementa Singleton para mantener una única instancia de la cola de misiones.
- `MisionQueue`: Implementa Singleton para la cola general de misiones.

### Beneficios

- **Estado compartido**: Permite compartir estado entre diferentes partes de la aplicación.
- **Eficiencia**: Evita la creación innecesaria de múltiples instancias.

### Ejemplo de uso

```python
class PersonajeMisionQueue:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonajeMisionQueue, cls).__new__(cls)
            cls._instance.queues = {}
        return cls._instance
```

## 4. Patrón DTO (Data Transfer Object)

El patrón DTO se utiliza para transferir datos entre subsistemas de una aplicación.

### Implementación

- `personaje_dto.py`: Define DTOs para operaciones con personajes.
- `mision_dto.py`: Define DTOs para operaciones con misiones.

### Beneficios

- **Encapsulación**: Encapsula los detalles de la representación de datos.
- **Validación**: Permite validar los datos de entrada antes de procesarlos.
- **Transformación**: Facilita la transformación de datos entre diferentes formatos.

### Ejemplo de uso

```python
class MisionCreate(MisionBase):
    nombre: str = Field(..., min_length=3, max_length=50)
    descripcion: str = Field(..., min_length=10, max_length=200)
    experiencia: int = Field(..., gt=0)
```

## 5. Patrón Inyección de Dependencias

La inyección de dependencias invierte el control de las dependencias.

### Implementación

- FastAPI proporciona un sistema de inyección de dependencias utilizado en los routers para obtener instancias de servicios y repositorios.

### Beneficios

- **Desacoplamiento**: Reduce el acoplamiento entre componentes.
- **Testabilidad**: Facilita la sustitución de dependencias por mocks en pruebas.
- **Flexibilidad**: Permite cambiar implementaciones sin modificar el código cliente.

### Ejemplo de uso

```python
def get_mision_service(db: Session = Depends(get_db), queue: MisionQueue = Depends(get_mission_queue)):
    repository = MisionRepository(db)
    return MisionService(repository, queue)

@router.post("/", response_model=MisionResponse)
def create_mision(mision: MisionCreate, service: MisionService = Depends(get_mision_service)):
    return service.create_mision(mision)
```

## 6. Patrón FIFO (First In, First Out)

El patrón FIFO implementa una cola donde el primer elemento añadido es el primero en ser procesado.

### Implementación

- `personaje_mision_queue.py`: Implementa colas FIFO para las misiones asignadas a cada personaje.

### Beneficios

- **Orden garantizado**: Garantiza que las misiones se procesan en el orden en que fueron asignadas.
- **Gestión justa**: Proporciona una gestión justa de las misiones para cada personaje.

### Ejemplo de uso

```python
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
```
