"""
Script para agregar enlaces de demostración a TECH LINK VIEWER.
"""
import json
import uuid
from pathlib import Path
from datetime import datetime


def generar_enlaces_demo():
    """Genera enlaces de demostración para mostrar las capacidades de la aplicación."""
    timestamp = datetime.now().isoformat()
    
    enlaces_demo = [
        {
            "id": str(uuid.uuid4()),
            "titulo": "GitHub - Desarrollo de Software",
            "url": "https://github.com",
            "categoria": "Desarrollo",
            "tags": ["git", "código", "repositorio", "desarrollo"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "Stack Overflow - Programación",
            "url": "https://stackoverflow.com",
            "categoria": "Desarrollo",
            "tags": ["programación", "ayuda", "comunidad", "código"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "YouTube - Videos Técnicos",
            "url": "https://youtube.com",
            "categoria": "Educación",
            "tags": ["videos", "tutoriales", "educación", "tecnología"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "LinkedIn - Red Profesional",
            "url": "https://linkedin.com",
            "categoria": "Trabajo",
            "tags": ["networking", "profesional", "empleo", "conexiones"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "Python.org - Documentación",
            "url": "https://python.org",
            "categoria": "Desarrollo",
            "tags": ["python", "documentación", "programación", "lenguaje"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "MDN Web Docs - HTML/CSS/JS",
            "url": "https://developer.mozilla.org",
            "categoria": "Desarrollo",
            "tags": ["web", "html", "css", "javascript", "documentación"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "AWS Console - Cloud Computing",
            "url": "https://aws.amazon.com/console",
            "categoria": "Cloud",
            "tags": ["aws", "cloud", "servidor", "infraestructura"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "Docker Hub - Contenedores",
            "url": "https://hub.docker.com",
            "categoria": "DevOps",
            "tags": ["docker", "contenedores", "devops", "deployment"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "Reddit - Tecnología",
            "url": "https://reddit.com/r/technology",
            "categoria": "Noticias",
            "tags": ["noticias", "tecnología", "comunidad", "discusión"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        },
        {
            "id": str(uuid.uuid4()),
            "titulo": "Hacker News - Tech News",
            "url": "https://news.ycombinator.com",
            "categoria": "Noticias",
            "tags": ["noticias", "startup", "tecnología", "emprendimiento"],
            "creado_en": timestamp,
            "actualizado_en": timestamp
        }
    ]
    
    # Cargar datos existentes
    ruta_datos = Path("data/links.json")
    
    try:
        with open(ruta_datos, 'r', encoding='utf-8') as f:
            datos_existentes = json.load(f)
    except FileNotFoundError:
        datos_existentes = {
            "version": 1,
            "categorias": [],
            "links": []
        }
    
    # Agregar nuevos enlaces
    datos_existentes["links"].extend(enlaces_demo)
    
    # Actualizar categorías
    nuevas_categorias = ["Desarrollo", "Educación", "Cloud", "DevOps", "Noticias"]
    for categoria in nuevas_categorias:
        if categoria not in datos_existentes["categorias"]:
            datos_existentes["categorias"].append(categoria)
    
    datos_existentes["categorias"].sort()
    
    # Guardar datos actualizados
    with open(ruta_datos, 'w', encoding='utf-8') as f:
        json.dump(datos_existentes, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Se agregaron {len(enlaces_demo)} enlaces de demostración")
    print(f"📁 Categorías disponibles: {', '.join(datos_existentes['categorias'])}")
    print(f"🔗 Total de enlaces: {len(datos_existentes['links'])}")


if __name__ == "__main__":
    generar_enlaces_demo()