"""
Motor de búsqueda con soporte para búsqueda fuzzy y normalización de texto.
"""
import re
from typing import List, Dict, Any, Tuple
from ..utils.validators import normalizar


def calcular_distancia_levenshtein(s1: str, s2: str) -> int:
    """
    Calcula la distancia de Levenshtein entre dos strings.
    
    Args:
        s1: Primera cadena
        s2: Segunda cadena
        
    Returns:
        Distancia de Levenshtein (número de operaciones de edición)
    """
    if len(s1) < len(s2):
        return calcular_distancia_levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    fila_anterior = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        fila_actual = [i + 1]
        for j, c2 in enumerate(s2):
            # Costo de inserción, eliminación o sustitución
            insercion = fila_anterior[j + 1] + 1
            eliminacion = fila_actual[j] + 1
            sustitucion = fila_anterior[j] + (c1 != c2)
            fila_actual.append(min(insercion, eliminacion, sustitucion))
        fila_anterior = fila_actual
    
    return fila_anterior[-1]


def calcular_score_fuzzy(termino_busqueda: str, texto_objetivo: str) -> float:
    """
    Calcula un score de similitud fuzzy entre un término de búsqueda y un texto.
    
    Args:
        termino_busqueda: Término que se está buscando
        texto_objetivo: Texto en el que buscar
        
    Returns:
        Score de 0.0 a 1.0 (1.0 = coincidencia exacta)
    """
    if not termino_busqueda or not texto_objetivo:
        return 0.0
    
    # Normalizar ambos textos
    termino_norm = normalizar(termino_busqueda)
    texto_norm = normalizar(texto_objetivo)
    
    # Coincidencia exacta
    if termino_norm == texto_norm:
        return 1.0
    
    # Contiene el término completo
    if termino_norm in texto_norm:
        return 0.9
    
    # Coincidencia por palabras
    palabras_termino = termino_norm.split()
    palabras_texto = texto_norm.split()
    
    coincidencias_palabra = 0
    for palabra_termino in palabras_termino:
        for palabra_texto in palabras_texto:
            if palabra_termino == palabra_texto:
                coincidencias_palabra += 1
            elif palabra_termino in palabra_texto or palabra_texto in palabra_termino:
                coincidencias_palabra += 0.7
    
    if coincidencias_palabra > 0:
        score_palabras = coincidencias_palabra / len(palabras_termino)
        return min(0.8, score_palabras)
    
    # Búsqueda fuzzy usando Levenshtein
    longitud_maxima = max(len(termino_norm), len(texto_norm))
    if longitud_maxima == 0:
        return 0.0
    
    distancia = calcular_distancia_levenshtein(termino_norm, texto_norm)
    score_levenshtein = 1.0 - (distancia / longitud_maxima)
    
    # Solo considerar scores fuzzy si son relativamente altos
    if score_levenshtein > 0.6:
        return score_levenshtein * 0.6
    
    return 0.0


def buscar_en_link(termino_busqueda: str, link: Dict[str, Any]) -> float:
    """
    Busca un término en todos los campos de un enlace y devuelve el mejor score.
    
    Args:
        termino_busqueda: Término a buscar
        link: Diccionario con los datos del enlace
        
    Returns:
        Score máximo encontrado (0.0 a 1.0)
    """
    if not termino_busqueda:
        return 1.0  # Sin término de búsqueda, mostrar todo
    
    scores = []
    
    # Buscar en título (peso alto)
    if 'titulo' in link:
        score_titulo = calcular_score_fuzzy(termino_busqueda, link['titulo'])
        scores.append(score_titulo * 1.2)  # Peso extra para título
    
    # Buscar en URL (peso medio)
    if 'url' in link:
        score_url = calcular_score_fuzzy(termino_busqueda, link['url'])
        scores.append(score_url)
    
    # Buscar en categoría (peso medio)
    if 'categoria' in link:
        score_categoria = calcular_score_fuzzy(termino_busqueda, link['categoria'])
        scores.append(score_categoria)
    
    # Buscar en tags (peso alto)
    if 'tags' in link and isinstance(link['tags'], list):
        for tag in link['tags']:
            score_tag = calcular_score_fuzzy(termino_busqueda, tag)
            scores.append(score_tag * 1.1)  # Peso extra para tags
    
    return min(1.0, max(scores) if scores else 0.0)


def filtrar_por_categoria(links: List[Dict[str, Any]], categoria: str) -> List[Dict[str, Any]]:
    """
    Filtra enlaces por categoría.
    
    Args:
        links: Lista de enlaces
        categoria: Categoría a filtrar (None o "Todas" para mostrar todas)
        
    Returns:
        Lista de enlaces filtrados
    """
    if not categoria or categoria == "Todas":
        return links
    
    return [link for link in links if link.get('categoria') == categoria]


def filtrar_por_tag(links: List[Dict[str, Any]], tag: str) -> List[Dict[str, Any]]:
    """
    Filtra enlaces por tag.
    
    Args:
        links: Lista de enlaces
        tag: Tag a filtrar
        
    Returns:
        Lista de enlaces filtrados
    """
    if not tag:
        return links
    
    tag_normalizado = normalizar(tag)
    resultado = []
    
    for link in links:
        if 'tags' in link and isinstance(link['tags'], list):
            for link_tag in link['tags']:
                if normalizar(link_tag) == tag_normalizado:
                    resultado.append(link)
                    break
    
    return resultado


def buscar_enlaces(links: List[Dict[str, Any]], 
                  termino_busqueda: str = "",
                  categoria_filtro: str = "",
                  tag_filtro: str = "",
                  umbral_score: float = 0.1) -> List[Tuple[Dict[str, Any], float]]:
    """
    Realiza búsqueda completa de enlaces con filtros y scoring.
    
    Args:
        links: Lista de enlaces a buscar
        termino_busqueda: Término de búsqueda libre
        categoria_filtro: Categoría por la que filtrar
        tag_filtro: Tag por el que filtrar
        umbral_score: Score mínimo para incluir resultado
        
    Returns:
        Lista de tuplas (enlace, score) ordenadas por relevancia
    """
    # Aplicar filtros de categoría y tag
    links_filtrados = filtrar_por_categoria(links, categoria_filtro)
    
    if tag_filtro:
        links_filtrados = filtrar_por_tag(links_filtrados, tag_filtro)
    
    # Si no hay término de búsqueda, devolver todos los filtrados
    if not termino_busqueda:
        return [(link, 1.0) for link in links_filtrados]
    
    # Buscar y calcular scores
    resultados = []
    for link in links_filtrados:
        score = buscar_en_link(termino_busqueda, link)
        if score >= umbral_score:
            resultados.append((link, score))
    
    # Ordenar por score descendente, luego por fecha de actualización
    resultados.sort(key=lambda x: (x[1], x[0].get('actualizado_en', '')), reverse=True)
    
    return resultados


def extraer_todas_las_categorias(links: List[Dict[str, Any]]) -> List[str]:
    """
    Extrae todas las categorías únicas de una lista de enlaces.
    
    Args:
        links: Lista de enlaces
        
    Returns:
        Lista de categorías únicas ordenadas
    """
    categorias = set()
    for link in links:
        if 'categoria' in link and link['categoria']:
            categorias.add(link['categoria'])
    
    return sorted(list(categorias))


def extraer_todos_los_tags(links: List[Dict[str, Any]]) -> List[str]:
    """
    Extrae todos los tags únicos de una lista de enlaces.
    
    Args:
        links: Lista de enlaces
        
    Returns:
        Lista de tags únicos ordenados
    """
    tags = set()
    for link in links:
        if 'tags' in link and isinstance(link['tags'], list):
            for tag in link['tags']:
                if tag:
                    tags.add(tag.lower())
    
    return sorted(list(tags))