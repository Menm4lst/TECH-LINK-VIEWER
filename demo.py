"""
Script de demostración para TECH LINK VIEWER.
Muestra las capacidades de búsqueda y funcionalidades principales.
"""
import sys
from pathlib import Path
from app.models.repository import RepositorioEnlaces
from app.models.search import buscar_enlaces, calcular_score_fuzzy
from app.utils.validators import normalizar


def mostrar_banner():
    """Muestra el banner de la aplicación."""
    print("🔗" + "=" * 60)
    print("    🔗 TECH LINK VIEWER - DEMOSTRACIÓN v4.0.1")
    print("    Buscador Global de Enlaces con Tema Oscuro")
    print("=" * 62)
    print()


def mostrar_estadisticas(repo):
    """Muestra estadísticas de la base de datos."""
    stats = repo.obtener_estadisticas()
    enlaces = repo.obtener_enlaces()
    
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("-" * 40)
    print(f"📎 Total de enlaces: {stats['total_enlaces']}")
    print(f"📁 Categorías: {stats['total_categorias']}")
    print(f"🏷️  Tags únicos: {stats['total_tags_unicos']}")
    print()
    
    print("📁 DISTRIBUCIÓN POR CATEGORÍAS:")
    for categoria, count in stats['enlaces_por_categoria'].items():
        print(f"   • {categoria}: {count} enlaces")
    print()


def demo_busqueda_basica(repo):
    """Demuestra búsqueda básica."""
    print("🔍 DEMOSTRACIÓN DE BÚSQUEDA BÁSICA")
    print("-" * 40)
    
    enlaces = repo.obtener_enlaces()
    terminos = ["github", "python", "desarrollo", "cloud"]
    
    for termino in terminos:
        resultados = buscar_enlaces(enlaces, termino)
        print(f"Término: '{termino}' → {len(resultados)} resultado(s)")
        
        for enlace, score in resultados[:2]:  # Mostrar solo los primeros 2
            print(f"   • {enlace['titulo']} (score: {score:.2f})")
        
        if len(resultados) > 2:
            print(f"   ... y {len(resultados) - 2} más")
        print()


def demo_busqueda_fuzzy(repo):
    """Demuestra búsqueda fuzzy."""
    print("🤖 DEMOSTRACIÓN DE BÚSQUEDA FUZZY")
    print("-" * 40)
    
    enlaces = repo.obtener_enlaces()
    
    # Búsquedas con errores de tipeo
    busquedas_fuzzy = [
        ("githb", "github con error de tipeo"),
        ("pythn", "python con letras faltantes"),
        ("tecnologia", "búsqueda con acentos"),
    ]
    
    for termino_error, descripcion in busquedas_fuzzy:
        resultados = buscar_enlaces(enlaces, termino_error)
        print(f"Búsqueda fuzzy: '{termino_error}' ({descripcion})")
        
        if resultados:
            mejor = resultados[0]
            print(f"   ✅ Mejor resultado: {mejor[0]['titulo']} (score: {mejor[1]:.2f})")
        else:
            print("   ❌ Sin resultados")
        print()


def demo_filtros(repo):
    """Demuestra filtros por categoría y tags."""
    print("🏷️  DEMOSTRACIÓN DE FILTROS")
    print("-" * 40)
    
    enlaces = repo.obtener_enlaces()
    
    # Filtro por categoría
    categorias = ["Desarrollo", "Cloud", "Noticias"]
    
    for categoria in categorias:
        if categoria in [enlace.get('categoria') for enlace in enlaces]:
            resultados = buscar_enlaces(enlaces, categoria_filtro=categoria)
            print(f"Categoría '{categoria}': {len(resultados)} enlaces")
    
    print()
    
    # Filtro por tags
    tags_ejemplo = ["python", "aws", "docker"]
    
    for tag in tags_ejemplo:
        resultados = buscar_enlaces(enlaces, tag_filtro=tag)
        if resultados:
            print(f"Tag '{tag}': {len(resultados)} enlaces")
    
    print()


def demo_normalizacion():
    """Demuestra la normalización de texto."""
    print("🔤 DEMOSTRACIÓN DE NORMALIZACIÓN")
    print("-" * 40)
    
    textos_ejemplo = [
        "Programación en Python",
        "  GITHUB   REPOSITORIO  ",
        "Configuración de AWS",
        "Documentación Técnica"
    ]
    
    for texto in textos_ejemplo:
        normalizado = normalizar(texto)
        print(f"'{texto}' → '{normalizado}'")
    
    print()


def main():
    """Función principal de demostración."""
    mostrar_banner()
    
    # Cargar repositorio
    ruta_datos = Path("data/links.json")
    if not ruta_datos.exists():
        print("❌ Archivo de datos no encontrado.")
        print("💡 Ejecuta 'python generar_demo.py' para crear datos de prueba.")
        return
    
    repo = RepositorioEnlaces(ruta_datos)
    
    # Ejecutar demostraciones
    mostrar_estadisticas(repo)
    demo_busqueda_basica(repo)
    demo_busqueda_fuzzy(repo)
    demo_filtros(repo)
    demo_normalizacion()
    
    print("🎯 PRÓXIMOS PASOS:")
    print("-" * 40)
    print("1. Ejecuta 'python -m app.main' para abrir la interfaz gráfica")
    print("2. Prueba la búsqueda en tiempo real")
    print("3. Agrega tus propios enlaces")
    print("4. Explora los filtros por categoría y tags")
    print("5. Usa los atajos de teclado (Ctrl+N, Ctrl+F, etc.)")
    print()
    print("🔗 ¡Disfruta usando TECH LINK VIEWER!")


if __name__ == "__main__":
    main()