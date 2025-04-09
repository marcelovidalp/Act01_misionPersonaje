# Diagramas de Patrones de Diseño

## Patrón Repositorio

El patrón Repositorio actúa como una capa intermedia entre la lógica de negocio y la capa de acceso a datos.

```mermaid
classDiagram
    class Service {
        +operacionDeNegocio()
    }
    
    class Repository {
        -db: Session
        +create()
        +read()
        +update()
        +delete()
        +findBy()
    }
    
    class Database {
        +executeSQLQuery()
    }
    
    class Model {
        +attributes
    }
    
    Service --> Repository : usa
    Repository --> Database : usa
    Repository --> Model : opera sobre
```

## Patrón Singleton

El patrón Singleton garantiza que una clase tenga una única instancia y proporciona un punto de acceso global a ella.

```mermaid
classDiagram
    class PersonajeMisionQueue {
        -_instance: PersonajeMisionQueue
        -queues: Dict[int, deque]
        +__new__(cls)
        +get_queue(personaje_id)
        +enqueue(personaje_id, mision)
        +dequeue(personaje_id)
    }
    
    class Service1 {
        +usaQueue()
    }
    
    class Service2 {
        +usaQueue()
    }
    
    Service1 --> PersonajeMisionQueue : usa la misma instancia
    Service2 --> PersonajeMisionQueue : usa la misma instancia
```

## Patrón DTO (Data Transfer Object)

El patrón DTO separa los datos de transferencia de los modelos del dominio.

```mermaid
classDiagram
    class Controller {
        +createPersonaje(dto)
        +updatePersonaje(dto)
    }
    
    class PersonajeDTO {
        +nombre
        +clase
        +validate()
    }
    
    class PersonajeService {
        +create(dto)
        +update(id, dto)
    }
    
    class PersonajeModel {
        +id
        +nombre
        +nivel
        +clase
        +experiencia
        +save()
        +update()
    }
    
    Controller --> PersonajeDTO : usa
    Controller --> PersonajeService : llama
    PersonajeService --> PersonajeDTO : recibe/devuelve
    PersonajeService --> PersonajeModel : modifica
```

## Patrón Inyección de Dependencias

El patrón de Inyección de Dependencias invierte el control de creación de dependencias.

```mermaid
flowchart TD
    A[Controller] --> |depende de| B{DI Container}
    B --> |crea| C[Service]
    B --> |crea| D[Repository]
    B --> |crea| E[DB Session]
    C --> |depende de| D
    D --> |depende de| E
```

## Patrón FIFO (First In, First Out)

El patrón FIFO implementa una estructura de datos tipo cola donde el primer elemento en entrar es el primero en salir.

```mermaid
graph TD
    subgraph QueueSystem["Sistema de Cola FIFO"]
        A[Nuevo elemento] -->|enqueue| Queue
        Queue -->|dequeue| B[Elemento procesado]
    end
    
    subgraph Implementación
        enqueue[("enqueue(element)")] -->|"Añade al final"| deque[("cola: deque")]
        dequeue[("dequeue()")] -->|"Extrae del principio"| deque
    end
    
    subgraph GameSystem["Sistema de Juego"]
        CreateMission["Crear Misión"] -->|"enqueue"| MissionQueue["Cola de Misiones"]
        MissionQueue -->|"dequeue"| ProcessMission["Procesar Misión"]
    end
```

## Arquitectura por Capas

La arquitectura por capas separa las responsabilidades del sistema en niveles.

```mermaid
flowchart TB
    subgraph Presentation["Capa de Presentación"]
        API[API Controllers]
    end
    
    subgraph BusinessLogic["Capa de Lógica de Negocio"]
        Services[Servicios]
    end
    
    subgraph DataAccess["Capa de Acceso a Datos"]
        Repositories[Repositorios]
    end
    
    subgraph DatabaseLayer["Capa de Base de Datos"]
        ORM[ORM]
        DB[(Database)]
    end
    
    Presentation --> BusinessLogic
    BusinessLogic --> DataAccess
    DataAccess --> DatabaseLayer
```
