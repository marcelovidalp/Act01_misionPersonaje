# Guía de Instalación y Uso

Esta guía explica cómo instalar y ejecutar la aplicación de Sistema de Misiones RPG.

## Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## Instalación

### 1. Clonar el repositorio (opcional)

```bash
git clone https://github.com/username/Act01_misionPersonaje.git
cd Act01_misionPersonaje
```

### 2. Crear un entorno virtual (recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración

La aplicación utiliza una base de datos SQLite que se crea automáticamente en el directorio raíz del proyecto. No es necesaria ninguna configuración adicional para empezar a usar la aplicación.

## Ejecución

### Iniciar la aplicación

```bash
# En Windows
python main.py

# En macOS/Linux
python3 main.py
```

La API estará disponible en `http://localhost:8000`

### Acceder a la documentación Swagger

Abre un navegador y visita:

```
http://localhost:8000/docs
```

Aquí encontrarás una interfaz interactiva que te permite probar todos los endpoints de la API.

## Uso básico

### Flujo de trabajo típico

1. **Crear personajes y misiones**:
   - Crea varios personajes usando el endpoint `POST /personajes`
   - Crea varias misiones usando el endpoint `POST /misiones`

2. **Asignar misiones a personajes**:
   - Asigna misiones a personajes usando el endpoint `POST /personajes/{id}/misiones/{id}`

3. **Completar misiones**:
   - Completa misiones para ganar experiencia usando el endpoint `POST /personajes/{id}/completar`

4. **Consultar progreso**:
   - Verifica las misiones pendientes con el endpoint `GET /personajes/{id}/misiones`
   - Verifica el nivel y experiencia de los personajes con el endpoint `GET /personajes/{id}`

### Ejemplo de flujo de trabajo con la API

#### 1. Crear un personaje

```bash
curl -X POST "http://localhost:8000/personajes" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Gandalf", "clase": "Mago"}'
```

Respuesta:
```json
{
  "id": 1,
  "nombre": "Gandalf",
  "clase": "Mago",
  "nivel": 1,
  "experiencia": 0
}
```

#### 2. Crear una misión

```bash
curl -X POST "http://localhost:8000/misiones" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Derrotar al dragón", "descripcion": "Debes vencer al dragón que habita en la montaña", "experiencia": 200}'
```

Respuesta:
```json
{
  "id": 1,
  "nombre": "Derrotar al dragón",
  "descripcion": "Debes vencer al dragón que habita en la montaña",
  "experiencia": 200,
  "estado": "pendiente",
  "fecha_inicio": "2023-09-25T12:30:45.123456"
}
```

#### 3. Aceptar la misión

```bash
curl -X POST "http://localhost:8000/personajes/1/misiones/1"
```

Respuesta:
```json
{
  "message": "Misión aceptada exitosamente"
}
```

#### 4. Verificar las misiones del personaje

```bash
curl -X GET "http://localhost:8000/personajes/1/misiones"
```

Respuesta:
```json
[
  {
    "id": 1,
    "nombre": "Derrotar al dragón",
    "descripcion": "Debes vencer al dragón que habita en la montaña",
    "experiencia": 200,
    "estado": "en_progreso",
    "fecha_inicio": "2023-09-25T12:30:45.123456"
  }
]
```

#### 5. Completar la misión

```bash
curl -X POST "http://localhost:8000/personajes/1/completar"
```

Respuesta:
```json
{
  "id": 1,
  "nombre": "Derrotar al dragón",
  "descripcion": "Debes vencer al dragón que habita en la montaña",
  "experiencia": 200,
  "estado": "completada",
  "fecha_inicio": "2023-09-25T12:30:45.123456"
}
```

#### 6. Verificar el estado del personaje

```bash
curl -X GET "http://localhost:8000/personajes/1"
```

Respuesta:
```json
{
  "id": 1,
  "nombre": "Gandalf",
  "clase": "Mago",
  "nivel": 3,
  "experiencia": 200
}
```

## Solución de problemas comunes

### Error: Address already in use

Si al ejecutar la aplicación obtienes un error indicando que el puerto 8000 ya está en uso, puedes modificar el puerto en el archivo `main.py`:

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Cambia 8000 por otro puerto
```

### Error: No module named 'fastapi'

Este error indica que las dependencias no se han instalado correctamente. Asegúrate de haber activado el entorno virtual y ejecutado:

```bash
pip install -r requirements.txt
```

### Error: Database is locked

Este error puede ocurrir cuando múltiples procesos intentan acceder a la base de datos SQLite simultáneamente. Asegúrate de que solo tienes una instancia de la aplicación ejecutándose.
