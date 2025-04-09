"""
Ejemplo de uso del sistema de misiones RPG
Este script crea datos de ejemplo y demuestra el flujo de trabajo de la API
"""
import requests
import json
import time

# URL base de la API
BASE_URL = "http://localhost:8000"

def print_response(response):
    """Formatea y muestra la respuesta de la API"""
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("-" * 50)

def run_example():
    """Ejecuta un flujo de trabajo completo de ejemplo"""
    print("=== SISTEMA DE MISIONES RPG - FLUJO DE TRABAJO DE EJEMPLO ===")
    
    # 1. Crear dos personajes
    print("\n1. Creando personajes...")
    
    personaje1_data = {
        "nombre": "Aragorn",
        "clase": "Guerrero"
    }
    response = requests.post(f"{BASE_URL}/personajes/", json=personaje1_data)
    print_response(response)
    personaje1 = response.json()
    
    personaje2_data = {
        "nombre": "Gandalf",
        "clase": "Mago"
    }
    response = requests.post(f"{BASE_URL}/personajes/", json=personaje2_data)
    print_response(response)
    personaje2 = response.json()
    
    # 2. Crear varias misiones
    print("\n2. Creando misiones...")
    
    mision1_data = {
        "nombre": "Derrotar al dragón",
        "descripcion": "Debes enfrentarte al temible dragón Smaug y derrotarlo",
        "experiencia": 150
    }
    response = requests.post(f"{BASE_URL}/misiones/", json=mision1_data)
    print_response(response)
    mision1 = response.json()
    
    mision2_data = {
        "nombre": "Rescatar al príncipe",
        "descripcion": "El príncipe ha sido secuestrado. ¡Debes rescatarlo!",
        "experiencia": 100
    }
    response = requests.post(f"{BASE_URL}/misiones/", json=mision2_data)
    print_response(response)
    mision2 = response.json()
    
    mision3_data = {
        "nombre": "Recuperar el anillo",
        "descripcion": "Debes recuperar el anillo mágico que fue robado del reino",
        "experiencia": 200
    }
    response = requests.post(f"{BASE_URL}/misiones/", json=mision3_data)
    print_response(response)
    mision3 = response.json()
    
    # 3. Asignar misiones a personajes
    print("\n3. Asignando misiones a personajes...")
    
    # Aragorn acepta dos misiones
    response = requests.post(f"{BASE_URL}/personajes/{personaje1['id']}/misiones/{mision1['id']}")
    print_response(response)
    
    response = requests.post(f"{BASE_URL}/personajes/{personaje1['id']}/misiones/{mision2['id']}")
    print_response(response)
    
    # Gandalf acepta una misión
    response = requests.post(f"{BASE_URL}/personajes/{personaje2['id']}/misiones/{mision3['id']}")
    print_response(response)
    
    # 4. Verificar las misiones de los personajes
    print("\n4. Verificando misiones asignadas (orden FIFO)...")
    
    response = requests.get(f"{BASE_URL}/personajes/{personaje1['id']}/misiones")
    print(f"Misiones de {personaje1['nombre']}:")
    print_response(response)
    
    response = requests.get(f"{BASE_URL}/personajes/{personaje2['id']}/misiones")
    print(f"Misiones de {personaje2['nombre']}:")
    print_response(response)
    
    # 5. Completar misiones
    print("\n5. Completando misiones...")
    
    # Aragorn completa su primera misión
    response = requests.post(f"{BASE_URL}/personajes/{personaje1['id']}/completar")
    print(f"{personaje1['nombre']} completa la misión:")
    print_response(response)
    
    # Gandalf completa su misión
    response = requests.post(f"{BASE_URL}/personajes/{personaje2['id']}/completar")
    print(f"{personaje2['nombre']} completa la misión:")
    print_response(response)
    
    # 6. Verificar estado final (personajes con experiencia y misiones restantes)
    print("\n6. Verificando estado final...")
    
    # Verificar estado de personajes (nivel y experiencia)
    response = requests.get(f"{BASE_URL}/personajes/{personaje1['id']}")
    print(f"Estado final de {personaje1['nombre']}:")
    print_response(response)
    
    response = requests.get(f"{BASE_URL}/personajes/{personaje2['id']}")
    print(f"Estado final de {personaje2['nombre']}:")
    print_response(response)
    
    # Verificar misiones restantes
    response = requests.get(f"{BASE_URL}/personajes/{personaje1['id']}/misiones")
    print(f"Misiones restantes de {personaje1['nombre']}:")
    print_response(response)
    
    print("\n=== FIN DEL EJEMPLO ===")

if __name__ == "__main__":
    print("Asegúrate de que la API está en ejecución en http://localhost:8000")
    print("Esperando 3 segundos antes de comenzar...")
    time.sleep(3)
    run_example()
