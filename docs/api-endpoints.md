# API REST con FastAPI

Este documento describe los endpoints disponibles en la API del Sistema de Misiones RPG, implementada con FastAPI.

## Información General

- **URL Base**: `http://localhost:8000`
- **Documentación Swagger**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`

## Formato de Respuestas

Todas las respuestas se devuelven en formato JSON. Los códigos de estado HTTP estándar se utilizan para indicar el éxito o fracaso de las solicitudes:

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Solicitud exitosa sin contenido para devolver
- `400 Bad Request`: Error en la solicitud
- `404 Not Found`: Recurso no encontrado
- `422 Unprocessable Entity`: Validación fallida
- `500 Internal Server Error`: Error del servidor

## Autenticación

Actualmente, la API no requiere autenticación y es accesible públicamente.

## Endpoints

### Personajes

#### Obtener todos los personajes

```
GET /personajes
```

**Parámetros de consulta**:
- `skip` (opcional): Número de registros a omitir (defecto: 0)
- `limit` (opcional): Número máximo de registros a devolver (defecto: 100)

**Respuesta exitosa (200 OK)**:
```json
[
  {
    "id": 1,
    "nombre": "Aragorn",
    "clase": "Guerrero",
    "nivel": 5,
    "experiencia": 450
  },
  {
    "id": 2,
    "nombre": "Gandalf",
    "clase": "Mago",
    "nivel": 10,
    "experiencia": 980
  }
]
```

#### Obtener un personaje por ID

```
GET /personajes/{personaje_id}
```

**Parámetros de ruta**:
- `personaje_id`: ID del personaje

**Respuesta exitosa (200 OK)**:
```json
{
  "id": 1,
  "nombre": "Aragorn",
  "clase": "Guerrero",
  "nivel": 5,
  "experiencia": 450
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "Personaje no encontrado"
}
```

#### Crear un nuevo personaje

```
POST /personajes
```

**Cuerpo de la solicitud**:
```json
{
  "nombre": "Legolas",
  "clase": "Arquero"
}
```

**Respuesta exitosa (201 Created)**:
```json
{
  "id": 3,
  "nombre": "Legolas",
  "clase": "Arquero",
  "nivel": 1,
  "experiencia": 0
}
```

**Error de validación (422 Unprocessable Entity)**:
```json
{
  "detail": [
    {
      "loc": ["body", "nombre"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Actualizar un personaje

```
PUT /personajes/{personaje_id}
```

**Parámetros de ruta**:
- `personaje_id`: ID del personaje

**Cuerpo de la solicitud**:
```json
{
  "nombre": "Aragorn II",
  "clase": "Rey"
}
```

**Respuesta exitosa (200 OK)**:
```json
{
  "id": 1,
  "nombre": "Aragorn II",
  "clase": "Rey",
  "nivel": 5,
  "experiencia": 450
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "Personaje no encontrado"
}
```

#### Eliminar un personaje

```
DELETE /personajes/{personaje_id}
```

**Parámetros de ruta**:
- `personaje_id`: ID del personaje

**Respuesta exitosa (204 No Content)**:
Sin contenido

**Error (404 Not Found)**:
```json
{
  "detail": "Personaje no encontrado"
}
```

#### Aceptar una misión (encolar)

```
POST /personajes/{personaje_id}/misiones/{mision_id}
```

**Parámetros de ruta**:
- `personaje_id`: ID del personaje
- `mision_id`: ID de la misión

**Respuesta exitosa (200 OK)**:
```json
{
  "message": "Misión aceptada exitosamente",
  "personaje_id": 1,
  "mision_id": 2
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "No se pudo aceptar la misión. Verifica que el personaje y la misión existan y que la misión esté pendiente."
}
```

#### Completar una misión (desencolar + sumar XP)

```
POST /personajes/{personaje_id}/completar
```

**Parámetros de ruta**:
- `personaje_id`: ID del personaje

**Respuesta exitosa (200 OK)**:
```json
{
  "id": 2,
  "nombre": "Derrotar al dragón",
  "descripcion": "Debes matar al dragón que aterroriza la aldea",
  "experiencia": 200,
  "estado": "completada",
  "fecha_inicio": "2023-09-25T12:30:45.123456"
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "No hay misiones pendientes para completar o el personaje no existe."
}
```

#### Listar misiones de un personaje en orden FIFO

```
GET /personajes/{personaje_id}/misiones
```

**Parámetros de ruta**:
- `personaje_id`: ID del personaje

**Respuesta exitosa (200 OK)**:
```json
[
  {
    "id": 1,
    "nombre": "Rescatar al príncipe",
    "descripcion": "Debes rescatar al príncipe secuestrado",
    "experiencia": 150,
    "estado": "en_progreso",
    "fecha_inicio": "2023-09-25T10:30:45.123456"
  },
  {
    "id": 3,
    "nombre": "Robar el tesoro",
    "descripcion": "Infiltrarse en la cueva del dragón y robar su tesoro",
    "experiencia": 300,
    "estado": "en_progreso",
    "fecha_inicio": "2023-09-25T14:30:45.123456"
  }
]
```

**Error (404 Not Found)**:
```json
{
  "detail": "Personaje no encontrado"
}
```

### Misiones

#### Obtener todas las misiones

```
GET /misiones
```

**Parámetros de consulta**:
- `skip` (opcional): Número de registros a omitir (defecto: 0)
- `limit` (opcional): Número máximo de registros a devolver (defecto: 100)

**Respuesta exitosa (200 OK)**:
```json
[
  {
    "id": 1,
    "nombre": "Rescatar al príncipe",
    "descripcion": "Debes rescatar al príncipe secuestrado",
    "experiencia": 150,
    "estado": "en_progreso",
    "fecha_inicio": "2023-09-25T10:30:45.123456"
  },
  {
    "id": 2,
    "nombre": "Derrotar al dragón",
    "descripcion": "Debes matar al dragón que aterroriza la aldea",
    "experiencia": 200,
    "estado": "pendiente",
    "fecha_inicio": "2023-09-25T12:30:45.123456"
  }
]
```

#### Obtener una misión por ID

```
GET /misiones/{mision_id}
```

**Parámetros de ruta**:
- `mision_id`: ID de la misión

**Respuesta exitosa (200 OK)**:
```json
{
  "id": 1,
  "nombre": "Rescatar al príncipe",
  "descripcion": "Debes rescatar al príncipe secuestrado",
  "experiencia": 150,
  "estado": "en_progreso",
  "fecha_inicio": "2023-09-25T10:30:45.123456"
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "Misión no encontrada"
}
```

#### Crear una nueva misión

```
POST /misiones
```

**Cuerpo de la solicitud**:
```json
{
  "nombre": "Recuperar el anillo",
  "descripcion": "Debes viajar a Mordor y destruir el anillo en el Monte del Destino",
  "experiencia": 500
}
```

**Respuesta exitosa (201 Created)**:
```json
{
  "id": 4,
  "nombre": "Recuperar el anillo",
  "descripcion": "Debes viajar a Mordor y destruir el anillo en el Monte del Destino",
  "experiencia": 500,
  "estado": "pendiente",
  "fecha_inicio": "2023-09-25T16:30:45.123456"
}
```

#### Actualizar una misión

```
PUT /misiones/{mision_id}
```

**Parámetros de ruta**:
- `mision_id`: ID de la misión

**Cuerpo de la solicitud**:
```json
{
  "nombre": "Recuperar el anillo mágico",
  "experiencia": 600
}
```

**Respuesta exitosa (200 OK)**:
```json
{
  "id": 4,
  "nombre": "Recuperar el anillo mágico",
  "descripcion": "Debes viajar a Mordor y destruir el anillo en el Monte del Destino",
  "experiencia": 600,
  "estado": "pendiente",
  "fecha_inicio": "2023-09-25T16:30:45.123456"
}
```

#### Eliminar una misión

```
DELETE /misiones/{mision_id}
```

**Parámetros de ruta**:
- `mision_id`: ID de la misión

**Respuesta exitosa (204 No Content)**:
Sin contenido

**Error (404 Not Found)**:
```json
{
  "detail": "Misión no encontrada"
}
```

#### Asignar un personaje a una misión

```
POST /misiones/{mision_id}/asignar/{personaje_id}
```

**Parámetros de ruta**:
- `mision_id`: ID de la misión
- `personaje_id`: ID del personaje

**Respuesta exitosa (200 OK)**:
```json
{
  "message": "Personaje asignado correctamente a la misión"
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "No se pudo realizar la asignación"
}
```

#### Obtener la siguiente misión pendiente

```
GET /misiones/next-mission
```

**Respuesta exitosa (200 OK)**:
```json
{
  "id": 2,
  "nombre": "Derrotar al dragón",
  "descripcion": "Debes matar al dragón que aterroriza la aldea",
  "experiencia": 200,
  "estado": "pendiente",
  "fecha_inicio": "2023-09-25T12:30:45.123456"
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "No hay misiones pendientes en la cola"
}
```

## Uso con cURL

### Crear un personaje
```bash
curl -X POST "http://localhost:8000/personajes/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Frodo", "clase": "Halfling"}'
```

### Crear una misión
```bash
curl -X POST "http://localhost:8000/misiones/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Destruir el anillo", "descripcion": "Viaja a Mordor y destruye el anillo", "experiencia": 1000}'
```

### Aceptar una misión
```bash
curl -X POST "http://localhost:8000/personajes/1/misiones/1"
```

### Completar una misión
```bash
curl -X POST "http://localhost:8000/personajes/1/completar"
```

## Uso con Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Crear un personaje
personaje_data = {
    "nombre": "Legolas",
    "clase": "Elfo"
}
response = requests.post(f"{BASE_URL}/personajes/", json=personaje_data)
personaje = response.json()
print(f"Personaje creado: {personaje}")

# Crear una misión
mision_data = {
    "nombre": "Defender Helm's Deep",
    "descripcion": "Proteger la fortaleza de los orcos",
    "experiencia": 300
}
response = requests.post(f"{BASE_URL}/misiones/", json=mision_data)
mision = response.json()
print(f"Misión creada: {mision}")

# Aceptar la misión
personaje_id = personaje["id"]
mision_id = mision["id"]
response = requests.post(f"{BASE_URL}/personajes/{personaje_id}/misiones/{mision_id}")
print(f"Respuesta: {response.json()}")

# Completar la misión
response = requests.post(f"{BASE_URL}/personajes/{personaje_id}/completar")
print(f"Misión completada: {response.json()}")

# Verificar nivel y experiencia del personaje
response = requests.get(f"{BASE_URL}/personajes/{personaje_id}")
personaje_actualizado = response.json()
print(f"Estado actual del personaje: {personaje_actualizado}")
```

## Códigos de Estado y Errores Comunes

| Código | Descripción | Posible causa |
|--------|-------------|--------------|
| 200 | OK | Solicitud exitosa |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Operación exitosa sin contenido para devolver |
| 400 | Bad Request | Datos de solicitud malformados |
| 404 | Not Found | Recurso solicitado no existe |
| 422 | Unprocessable Entity | Datos de entrada no válidos |
| 500 | Internal Server Error | Error en el servidor |

### Errores Comunes:

1. **Personaje o Misión no encontrado**: Asegúrate de usar IDs válidos en las solicitudes.
2. **Validación de datos**: Verifica que los campos obligatorios están presentes y tienen el formato correcto.
3. **Estado de misión incorrecto**: Las misiones solo pueden ser aceptadas si están en estado "pendiente".
4. **Cola vacía**: No se puede completar una misión si el personaje no tiene misiones en su cola.
