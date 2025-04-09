# Diagrama de Componentes

Este diagrama muestra los principales componentes del sistema y cómo interactúan entre sí.

```mermaid
flowchart TB
    subgraph API["API Layer"]
        fastapi[FastAPI Application]
        personajeRouter[Personaje Router]
        misionRouter[Misión Router]
    end
    
    subgraph Service["Service Layer"]
        personajeService[Personaje Service]
        misionService[Misión Service]
    end
    
    subgraph Repository["Repository Layer"]
        personajeRepo[Personaje Repository]
        misionRepo[Misión Repository]
    end
    
    subgraph Database["Database Layer"]
        sqlalchemy[SQLAlchemy ORM]
        sqlite[(SQLite Database)]
    end
    
    subgraph Queue["Queue System"]
        misionQueue[Misión Queue]
        personajeMisionQueue[Personaje Misión Queue]
    end
    
    subgraph Model["Domain Model"]
        personajeModel[Personaje Model]
        misionModel[Misión Model]
        misionPersonajeModel[MisiónPersonaje Model]
    end
    
    subgraph DTO["Data Transfer Objects"]
        personajeDTO[Personaje DTOs]
        misionDTO[Misión DTOs]
    end
    
    %% Conexiones
    fastapi --> personajeRouter
    fastapi --> misionRouter
    
    personajeRouter --> personajeService
    misionRouter --> misionService
    
    personajeService --> personajeRepo
    personajeService --> misionRepo
    personajeService --> personajeMisionQueue
    
    misionService --> misionRepo
    misionService --> misionQueue
    
    personajeRepo --> sqlalchemy
    misionRepo --> sqlalchemy
    
    sqlalchemy --> sqlite
    
    personajeService --> personajeDTO
    misionService --> misionDTO
    
    personajeRepo --> personajeModel
    misionRepo --> misionModel
    personajeRepo --> misionPersonajeModel
    misionRepo --> misionPersonajeModel
```

## Descripción del Diagrama de Componentes

El sistema está organizado en capas bien definidas siguiendo el principio de separación de responsabilidades:

### Capa de API (API Layer)
- **FastAPI Application**: Punto de entrada principal de la aplicación
- **Personaje Router**: Gestiona las solicitudes HTTP relacionadas con personajes
- **Misión Router**: Gestiona las solicitudes HTTP relacionadas con misiones

### Capa de Servicio (Service Layer)
- **Personaje Service**: Implementa la lógica de negocio para personajes
- **Misión Service**: Implementa la lógica de negocio para misiones

### Capa de Repositorio (Repository Layer)
- **Personaje Repository**: Proporciona acceso a datos para personajes
- **Misión Repository**: Proporciona acceso a datos para misiones

### Capa de Base de Datos (Database Layer)
- **SQLAlchemy ORM**: Mapeo objeto-relacional
- **SQLite Database**: Base de datos SQLite

### Sistema de Cola (Queue System)
- **Misión Queue**: Gestiona colas de misiones generales
- **Personaje Misión Queue**: Gestiona colas de misiones por personaje

### Modelo de Dominio (Domain Model)
- **Personaje Model**: Define la entidad Personaje
- **Misión Model**: Define la entidad Misión
- **MisiónPersonaje Model**: Define la relación entre personajes y misiones

### Objetos de Transferencia de Datos (DTOs)
- **Personaje DTOs**: DTOs para personajes
- **Misión DTOs**: DTOs para misiones
