"""
Script de pruebas para verificar funcionalidades de TLV 4.0.
"""
from pathlib import Path
from app.models.repository import RepositorioEnlaces
from app.models.search import buscar_enlaces, calcular_score_fuzzy
from app.utils.validators import normalizar, validar_url
from app.utils.io import abrir_url


def test_repositorio():
    """Prueba básica del repositorio."""
    print("=== Prueba del Repositorio ===")
    
    # Usar archivo de prueba
    ruta_test = Path("data/links_test.json")
    repo = RepositorioEnlaces(ruta_test)
    
    # Verificar enlaces iniciales
    enlaces = repo.obtener_enlaces()
    print(f"Enlaces cargados: {len(enlaces)}")
    
    for enlace in enlaces:
        print(f"- {enlace['titulo']}: {enlace['url']} [{enlace['categoria']}]")
    
    # Estadísticas
    stats = repo.obtener_estadisticas()
    print(f"Estadísticas: {stats}")
    
    print()


def test_busqueda():
    """Prueba del motor de búsqueda."""
    print("=== Prueba de Búsqueda ===")
    
    repo = RepositorioEnlaces(Path("data/links.json"))
    enlaces = repo.obtener_enlaces()
    
    # Prueba búsqueda simple
    resultados = buscar_enlaces(enlaces, "google")
    print(f"Búsqueda 'google': {len(resultados)} resultados")
    
    for enlace, score in resultados:
        print(f"- {enlace['titulo']} (score: {score:.2f})")
    
    # Prueba búsqueda fuzzy
    resultados = buscar_enlaces(enlaces, "gogle")  # Error intencional
    print(f"Búsqueda fuzzy 'gogle': {len(resultados)} resultados")
    
    for enlace, score in resultados:
        print(f"- {enlace['titulo']} (score: {score:.2f})")
    
    print()


def test_validaciones():
    """Prueba las validaciones."""
    print("=== Prueba de Validaciones ===")
    
    # Prueba normalización
    textos = [
        "Categoría de Trabajo",
        "  TEXTO   CON   ESPACIOS  ",
        "Acentuación y ñoño"
    ]
    
    for texto in textos:
        print(f"'{texto}' -> '{normalizar(texto)}'")
    
    # Prueba validación URLs
    urls = [
        "https://www.google.com",
        "http://ejemplo.com",
        "www.google.com",
        "ftp://servidor.com",
        "no-es-url"
    ]
    
    for url in urls:
        valida = validar_url(url)
        print(f"'{url}' -> {valida}")
    
    print()


def test_score_fuzzy():
    """Prueba el algoritmo de scoring fuzzy."""
    print("=== Prueba Score Fuzzy ===")
    
    termino = "google"
    textos = [
        "Google",
        "google",
        "Gogle",  # Error de tipeo
        "Motor de búsqueda Google",
        "Yahoo",
        "Facebook"
    ]
    
    for texto in textos:
        score = calcular_score_fuzzy(termino, texto)
        print(f"'{termino}' vs '{texto}' -> {score:.3f}")
    
    print()


def main():
    """Ejecuta todas las pruebas."""
    print("🧪 Ejecutando pruebas de TLV 4.0")
    print("=" * 40)
    
    test_repositorio()
    test_busqueda()
    test_validaciones()
    test_score_fuzzy()
    
    print("✅ Todas las pruebas completadas")


if __name__ == "__main__":
    main()