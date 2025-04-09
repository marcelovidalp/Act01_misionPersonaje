from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

DATABASE_URL = 'sqlite:///RPG.db'

# Crear el engine de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una clase Session configurada
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base para los modelos declarativos
Base = declarative_base()

def get_db(): #-> Session
    """Dependencia para proporcionar una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def session_scope():
    """Contexto para manejar sesiones de base de datos"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def init_db():
    """Inicializa la base de datos creando todas las tablas definidas"""
    # Importamos los modelos aquí para asegurar que estén registrados
    from models.Personaje import Personaje
    from models.Mision import Mision
    from models.MisionPersonaje import MisionPersonaje
    
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada")