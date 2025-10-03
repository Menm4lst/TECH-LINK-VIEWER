"""
Utilidades para manejo de tiempo y fechas.
"""
from datetime import datetime
from typing import Optional


def obtener_timestamp_actual() -> str:
    """
    Obtiene el timestamp actual en formato ISO.
    
    Returns:
        Timestamp en formato ISO string
    """
    return datetime.now().isoformat()


def formatear_fecha(timestamp: str) -> str:
    """
    Formatea un timestamp ISO para mostrar en la UI.
    
    Args:
        timestamp: Timestamp en formato ISO
        
    Returns:
        Fecha formateada para mostrar
    """
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return "Fecha inválida"


def parsear_timestamp(timestamp: Optional[str]) -> Optional[datetime]:
    """
    Convierte un timestamp string a datetime object.
    
    Args:
        timestamp: Timestamp en formato ISO o None
        
    Returns:
        Objeto datetime o None si no se puede parsear
    """
    if not timestamp:
        return None
    
    try:
        return datetime.fromisoformat(timestamp)
    except (ValueError, TypeError):
        return None


def comparar_fechas(timestamp1: str, timestamp2: str) -> int:
    """
    Compara dos timestamps.
    
    Args:
        timestamp1: Primer timestamp
        timestamp2: Segundo timestamp
        
    Returns:
        -1 si timestamp1 < timestamp2
         0 si son iguales
         1 si timestamp1 > timestamp2
    """
    dt1 = parsear_timestamp(timestamp1)
    dt2 = parsear_timestamp(timestamp2)
    
    if dt1 is None and dt2 is None:
        return 0
    elif dt1 is None:
        return -1
    elif dt2 is None:
        return 1
    elif dt1 < dt2:
        return -1
    elif dt1 > dt2:
        return 1
    else:
        return 0