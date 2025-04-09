from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import init_db
from routers.mision_router import router as mision_router
from routers.personaje_router import router as personaje_router

# Inicializar FastAPI
app = FastAPI(
    title="Sistema de Misiones RPG",
    description="API para gestionar personajes y misiones de un juego RPG con sistema FIFO",
    version="1.0.0",
    openapi_tags=[
        {"name": "Root", "description": "Endpoint principal"},
        {"name": "Personajes", "description": "Operaciones con personajes"},
        {"name": "Misiones", "description": "Operaciones con misiones"}
    ]
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(personaje_router)
app.include_router(mision_router)

# Evento de inicio
@app.on_event("startup")
def startup_event():
    init_db()
    print("Base de datos inicializada correctamente.")

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Bienvenido al Sistema de Misiones RPG",
        "endpoints": {
            "Personajes": [
                {"POST /personajes": "Crear nuevo personaje"},
                {"GET /personajes/{id}/misiones": "Listar misiones en orden FIFO"},
                {"POST /personajes/{id}/misiones/{id}": "Aceptar misión (encolar)"},
                {"POST /personajes/{id}/completar": "Completar misión (desencolar + sumar XP)"}
            ],
            "Misiones": [
                {"POST /misiones": "Crear nueva misión"}
            ]
        },
        "documentación": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
