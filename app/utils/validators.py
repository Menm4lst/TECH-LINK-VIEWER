"""
Utilidades de validación para la aplicación.
"""
import re
import unicodedata
from urllib.parse import urlparse
from typing import List


def normalizar(texto: str) -> str:
    """
    Normaliza texto removiendo acentos, convirtiendo a minúsculas
    y limpiando espacios duplicados.
    
    Args:
        texto: Texto a normalizar
        
    Returns:
        Texto normalizado
        
    Examples:
        >>> normalizar("Categoría de Trabajo")
        'categoria de trabajo'
        >>> normalizar("  TEXTO   CON   ESPACIOS  ")
        'texto con espacios'
    """
    if not texto:
        return ""
    
    # Convertir a minúsculas
    texto = texto.lower()
    
    # Remover acentos usando unicodedata
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    
    # Limpiar espacios duplicados
    texto = re.sub(r'\s+', ' ', texto.strip())
    
    return texto


def validar_url(url: str) -> bool:
    """
    Valida que una URL tenga formato correcto y use http/https.
    
    Args:
        url: URL a validar
        
    Returns:
        True si la URL es válida, False en caso contrario
        
    Examples:
        >>> validar_url("https://www.google.com")
        True
        >>> validar_url("http://ejemplo.com")
        True
        >>> validar_url("ftp://servidor.com")
        False
        >>> validar_url("no-es-url")
        False
    """
    if not url:
        return False
        
    try:
        resultado = urlparse(url)
        return all([
            resultado.scheme in ('http', 'https'),
            resultado.netloc
        ])
    except Exception:
        return False


def validar_titulo(titulo: str) -> bool:
    """
    Valida que el título no esté vacío.
    
    Args:
        titulo: Título a validar
        
    Returns:
        True si el título es válido, False en caso contrario
    """
    return bool(titulo and titulo.strip())


def validar_categoria(categoria: str) -> bool:
    """
    Valida que la categoría no esté vacía.
    
    Args:
        categoria: Categoría a validar
        
    Returns:
        True si la categoría es válida, False en caso contrario
    """
    return bool(categoria and categoria.strip())


def validar_tags(tags: List[str]) -> bool:
    """
    Valida que la lista de tags sea válida.
    
    Args:
        tags: Lista de tags a validar
        
    Returns:
        True si los tags son válidos, False en caso contrario
    """
    if not isinstance(tags, list):
        return False
    
    # Todos los tags deben ser strings no vacíos
    for tag in tags:
        if not isinstance(tag, str) or not tag.strip():
            return False
    
    return True


def limpiar_url(url: str) -> str:
    """
    Limpia y normaliza una URL agregando protocolo si es necesario.
    
    Args:
        url: URL a limpiar
        
    Returns:
        URL limpia
        
    Examples:
        >>> limpiar_url("www.google.com")
        'https://www.google.com'
        >>> limpiar_url("  https://ejemplo.com  ")
        'https://ejemplo.com'
    """
    if not url:
        return ""
    
    url = url.strip()
    
    # Si no tiene protocolo, agregar https://
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
    
    return url


def limpiar_tags(tags: List[str]) -> List[str]:
    """
    Limpia y normaliza una lista de tags.
    
    Args:
        tags: Lista de tags a limpiar
        
    Returns:
        Lista de tags limpia sin duplicados
    """
    if not tags:
        return []
    
    tags_limpios = []
    tags_vistos = set()
    
    for tag in tags:
        if isinstance(tag, str):
            tag_limpio = tag.strip().lower()
            if tag_limpio and tag_limpio not in tags_vistos:
                tags_limpios.append(tag_limpio)
                tags_vistos.add(tag_limpio)
    
    return tags_limpios


if __name__ == "__main__":
    import doctest
    doctest.testmod()