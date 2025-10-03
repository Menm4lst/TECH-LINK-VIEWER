"""
Utilidades de entrada/salida para la aplicación.
"""
import json
import logging
import webbrowser
from pathlib import Path
from typing import Dict, Any, Optional
import portalocker


logger = logging.getLogger(__name__)


def abrir_url(url: str) -> bool:
    """
    Abre una URL en el navegador por defecto.
    
    Args:
        url: URL a abrir
        
    Returns:
        True si se abrió correctamente, False en caso contrario
    """
    try:
        webbrowser.open(url)
        logger.info(f"URL abierta correctamente: {url}")
        return True
    except Exception as e:
        logger.error(f"Error al abrir URL {url}: {e}")
        return False


def cargar_json(ruta_archivo: Path) -> Optional[Dict[str, Any]]:
    """
    Carga datos desde un archivo JSON con bloqueo seguro.
    
    Args:
        ruta_archivo: Ruta al archivo JSON
        
    Returns:
        Diccionario con los datos o None si hay error
    """
    try:
        if not ruta_archivo.exists():
            logger.warning(f"Archivo no existe: {ruta_archivo}")
            return None
            
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            # Bloqueo compartido para lectura
            portalocker.lock(f, portalocker.LOCK_SH)
            try:
                datos = json.load(f)
                logger.info(f"JSON cargado correctamente desde: {ruta_archivo}")
                return datos
            finally:
                portalocker.unlock(f)
                
    except json.JSONDecodeError as e:
        logger.error(f"Error de formato JSON en {ruta_archivo}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error al cargar JSON desde {ruta_archivo}: {e}")
        return None


def guardar_json(datos: Dict[str, Any], ruta_archivo: Path) -> bool:
    """
    Guarda datos en un archivo JSON con bloqueo seguro.
    
    Args:
        datos: Diccionario con los datos a guardar
        ruta_archivo: Ruta al archivo JSON
        
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    try:
        # Crear directorio padre si no existe
        ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            # Bloqueo exclusivo para escritura
            portalocker.lock(f, portalocker.LOCK_EX)
            try:
                json.dump(datos, f, ensure_ascii=False, indent=2)
                logger.info(f"JSON guardado correctamente en: {ruta_archivo}")
                return True
            finally:
                portalocker.unlock(f)
                
    except Exception as e:
        logger.error(f"Error al guardar JSON en {ruta_archivo}: {e}")
        return False


def validar_estructura_json(datos: Dict[str, Any]) -> bool:
    """
    Valida que un diccionario tenga la estructura esperada para links.json.
    
    Args:
        datos: Diccionario a validar
        
    Returns:
        True si la estructura es válida, False en caso contrario
    """
    try:
        # Verificar claves principales
        if not isinstance(datos, dict):
            return False
            
        if 'version' not in datos or 'categorias' not in datos or 'links' not in datos:
            return False
            
        # Verificar tipos
        if not isinstance(datos['version'], int):
            return False
            
        if not isinstance(datos['categorias'], list):
            return False
            
        if not isinstance(datos['links'], list):
            return False
            
        # Verificar cada enlace
        for link in datos['links']:
            if not isinstance(link, dict):
                return False
                
            campos_requeridos = ['id', 'titulo', 'url', 'categoria', 'tags', 'creado_en', 'actualizado_en']
            for campo in campos_requeridos:
                if campo not in link:
                    return False
                    
            # Verificar tipos específicos
            if not isinstance(link['tags'], list):
                return False
                
        logger.info("Estructura JSON válida")
        return True
        
    except Exception as e:
        logger.error(f"Error al validar estructura JSON: {e}")
        return False


def crear_backup(ruta_archivo: Path) -> bool:
    """
    Crea una copia de seguridad de un archivo.
    
    Args:
        ruta_archivo: Ruta al archivo original
        
    Returns:
        True si se creó el backup correctamente, False en caso contrario
    """
    try:
        if not ruta_archivo.exists():
            return False
            
        backup_path = ruta_archivo.with_suffix(f'{ruta_archivo.suffix}.backup')
        
        with open(ruta_archivo, 'r', encoding='utf-8') as origen:
            with open(backup_path, 'w', encoding='utf-8') as destino:
                destino.write(origen.read())
                
        logger.info(f"Backup creado: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error al crear backup: {e}")
        return False