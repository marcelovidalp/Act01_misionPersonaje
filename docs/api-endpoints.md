# API REST con FastAPI

La aplicación expone una API REST utilizando FastAPI, un moderno marco de desarrollo web para Python. FastAPI integra automáticamente la documentación de la API utilizando Swagger UI, lo que facilita la exploración y prueba de los endpoints.

## Endpoints Principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/personajes` | Crear nuevo personaje |
| POST | `/misiones` | Crear nueva misión |
| POST | `/personajes/{id}/misiones/{id}` | Aceptar misión (encolar) |
| POST | `/personajes/{id}/completar` | Completar misión (desencolar + sumar XP) |
| GET | `/personajes/{id}/misiones` | Listar misiones en orden FIFO |

## API de Personajes

### Crear un nuevo personaje

```
POST /personajes
```

**Payload**:
```json
{
  "nombre": "Aragorn",
  "clase": "Guerrero"
}
```

**Respuesta**: El personaje creado con su ID, nivel y experiencia iniciales.

### Obtener todos los personajes

```
GET /personajes
```

**Respuesta**: Lista de todos los personajes.

### Obtener un personaje por ID

```
GET /personajes/{personaje_id}
```

**Respuesta**: Detalles del personaje solicitado.

### Actualizar un personaje

```
PUT /personajes/{personaje_id}
```

**Payload**:
```json
{
  "nombre": "Aragorn Hijo de Arathorn",
  "nivel": 5
}
```

**Respuesta**: El personaje actualizado.

### Eliminar un personaje

```
DELETE /personajes/{personaje_id}
```

**Respuesta**: 204 No Content

### Aceptar una misión

```
POST /personajes/{personaje_id}/misiones/{mision_id}
```

**Respuesta**: Mensaje de confirmación.

### Completar una misión

```
POST /personajes/{personaje_id}/completar
```

**Respuesta**: La misión completada y la experiencia ganada.

### Listar misiones del personaje

```
GET /personajes/{personaje_id}/misiones
```

**Respuesta**: Lista de misiones asignadas al personaje en orden FIFO.

## API de Misiones

### Crear una nueva misión

```
POST /misiones
```

**Payload**:
```json
{
  "nombre": "Rescatar al príncipe",
  "descripcion": "El príncipe ha sido capturado por orcos. Debes rescatarlo.",
  "experiencia": 100
}
```

**Respuesta**: La misión creada con su ID y estado inicial.

### Obtener todas las misiones

```
GET /misiones
```

**Respuesta**: Lista de todas las misiones.

### Obtener una misión por ID

```
GET /misiones/{mision_id}
```

**Respuesta**: Detalles de la misión solicitada.

### Actualizar una misión

```
PUT /misiones/{mision_id}
```

**Payload**:
```json
{
  "nombre": "Rescatar al príncipe heredero",
  "experiencia": 150
}
```

**Respuesta**: La misión actualizada.

### Eliminar una misión

```
DELETE /misiones/{mision_id}
```

**Respuesta**: 204 No Content

## Documentación Swagger

La API está documentada automáticamente con Swagger UI, accesible en la ruta `/docs` de la aplicación. Aquí puedes:

1. Ver todos los endpoints disponibles
2. Leer la documentación de cada endpoint
3. Probar los endpoints directamente desde el navegador
4. Ver los esquemas de datos utilizados por la API

## Ejemplos de uso con cURL

### Crear un personaje

```bash
curl -X POST "http://localhost:8000/personajes" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Legolas", "clase": "Arquero"}'
```

### Crear una misión

```bash
curl -X POST "http://localhost:8000/misiones" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Caza de trolls", "descripcion": "Elimina a los trolls que amenazan la aldea", "experiencia": 75}'
```

### Aceptar una misión

```bash
curl -X POST "http://localhost:8000/personajes/1/misiones/1"
```

### Completar una misión

```bash
curl -X POST "http://localhost:8000/personajes/1/completar"
```

### Listar misiones del personaje

```bash
curl -X GET "http://localhost:8000/personajes/1/misiones"
```
