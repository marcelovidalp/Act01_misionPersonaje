# Estructura de la Aplicación

La aplicación sigue una arquitectura por capas, separando claramente las responsabilidades y facilitando el mantenimiento y la escalabilidad del código.

## Diagrama de Capas

```
┌─────────────────────────────┐
│          Controladores      │  Routers FastAPI
├─────────────────────────────┤
│           Servicios         │  Lógica de negocio
├─────────────────────────────┤
│         Repositorios        │  Acceso a datos
├─────────────────────────────┤
│           Modelos           │  Entidades de dominio
└─────────────────────────────┘
```

## Descripción de las Capas

### Modelos (Capa de Dominio)

Los modelos representan las entidades principales del sistema:

- `Personaje`: Representa a un personaje del juego con atributos como nombre, nivel, clase y experiencia.
- `Mision`: Representa una misión con atributos como nombre, descripción, experiencia otorgada y estado.
- `MisionPersonaje`: Relación muchos a muchos entre personajes y misiones.

### Repositorios (Capa de Acceso a Datos)

Los repositorios encapsulan la lógica de acceso y manipulación de datos:

- `PersonajeRepository`: Operaciones CRUD para personajes.
- `MisionRepository`: Operaciones CRUD para misiones.

### Servicios (Capa de Lógica de Negocio)

Los servicios implementan la lógica de negocio del sistema:

- `PersonajeService`: Lógica relacionada con personajes.
- `MisionService`: Lógica relacionada con misiones.

### Controladores (Capa de Presentación)

Los controladores (routers en FastAPI) definen los endpoints de la API:

- `personaje_router`: Endpoints para operaciones con personajes.
- `mision_router`: Endpoints para operaciones con misiones.

## Componentes Adicionales

### DTOs (Data Transfer Objects)

Los DTOs facilitan la transferencia de datos entre capas y la validación de entrada/salida:

- `personaje_dto`: DTOs para operaciones con personajes.
- `mision_dto`: DTOs para operaciones con misiones.

### Colas FIFO

Implementan el sistema de gestión de misiones por personaje:

- `personaje_mision_queue`: Cola FIFO para misiones por personaje.
- `misionFIFO`: Cola FIFO general para misiones.

## Estructura de Directorios

```
│   database.py          # Configuración de base de datos
│   main.py              # Punto de entrada de la aplicación
│
├───dto                  # Objetos de transferencia de datos
│       mision_dto.py
│       personaje_dto.py
│
├───models               # Modelos de datos
│       Base.py
│       Mision.py
│       MisionPersonaje.py
│       Personaje.py
│
├───queue                # Implementación de colas FIFO
│       misionFIFO.py
│       personaje_mision_queue.py
│
├───repositories         # Repositorios para acceso a datos
│       mision_repository.py
│       personaje_repository.py
│
├───routers              # Controladores de API
│       mision_router.py
│       personaje_router.py
│
└───services             # Servicios con lógica de negocio
        mision_service.py
        personaje_service.py
```
