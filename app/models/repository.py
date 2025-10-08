"""
Repositorio para gestión de datos de enlaces en formato JSON.
"""
import json
import logging
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from ..utils.io import cargar_json, guardar_json, validar_estructura_json, crear_backup
from ..utils.time import obtener_timestamp_actual
from ..utils.validators import (
    validar_url, validar_titulo, validar_categoria, 
    limpiar_url, limpiar_tags, normalizar
)


logger = logging.getLogger(__name__)


class RepositorioEnlaces:
    """
    Repositorio para gestionar la persistencia de enlaces en JSON.
    """
    
    def __init__(self, ruta_archivo: Path):
        """
        Inicializa el repositorio.
        
        Args:
            ruta_archivo: Ruta al archivo JSON de datos
        """
        self.ruta_archivo = ruta_archivo
        self._datos = self._cargar_o_crear_datos()
        
        # ⭐ Migrar enlaces existentes para soporte de favoritos
        self.migrar_favoritos()
    
    def _cargar_o_crear_datos(self) -> Dict[str, Any]:
        """
        Carga los datos desde el archivo o crea datos por defecto.
        
        Returns:
            Diccionario con los datos
        """
        datos = cargar_json(self.ruta_archivo)
        
        if datos is None or not validar_estructura_json(datos):
            logger.warning("Datos no válidos o no existen, creando datos por defecto")
            datos = self._crear_datos_por_defecto()
            # Guardar los datos por defecto directamente sin usar self.guardar()
            guardar_json(datos, self.ruta_archivo)
        
        return datos
    
    def cargar(self) -> bool:
        """
        Recarga los datos desde el archivo.
        
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        try:
            self._datos = self._cargar_o_crear_datos()
            logger.info("Datos recargados desde archivo")
            return True
        except Exception as e:
            logger.error(f"Error al recargar datos: {e}")
            return False
    
    def _crear_datos_por_defecto(self) -> Dict[str, Any]:
        """
        Crea los datos por defecto con enlaces de ejemplo.
        
        Returns:
            Diccionario con datos por defecto
        """
        timestamp_actual = obtener_timestamp_actual()
        
        return {
            "version": 1,
            "categorias": ["Personal", "Trabajo"],
            "links": [
                {
                    "id": str(uuid.uuid4()),
                    "titulo": "Google",
                    "url": "https://www.google.com",
                    "categoria": "Personal",
                    "tags": ["google", "buscador"],
                    "es_favorito": True,  # ⭐ Nuevo campo favorito
                    "creado_en": timestamp_actual,
                    "actualizado_en": timestamp_actual
                },
                {
                    "id": str(uuid.uuid4()),
                    "titulo": "Trabajo",
                    "url": "https://www.trabajo.com",
                    "categoria": "Trabajo",
                    "tags": ["trabajo"],
                    "es_favorito": False,  # ⭐ Nuevo campo favorito
                    "creado_en": timestamp_actual,
                    "actualizado_en": timestamp_actual
                }
            ]
        }
    
    def guardar(self) -> bool:
        """
        Guarda los datos actuales en el archivo.
        
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        return guardar_json(self._datos, self.ruta_archivo)
    
    def crear_backup(self) -> bool:
        """
        Crea una copia de seguridad del archivo actual.
        
        Returns:
            True si se creó el backup correctamente, False en caso contrario
        """
        return crear_backup(self.ruta_archivo)
    
    def obtener_enlaces(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los enlaces.
        
        Returns:
            Lista de enlaces
        """
        return self._datos.get('links', [])
    
    def obtener_categorias(self) -> List[str]:
        """
        Obtiene todas las categorías.
        
        Returns:
            Lista de categorías
        """
        return self._datos.get('categorias', [])
    
    def obtener_enlace_por_id(self, enlace_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un enlace por su ID.
        
        Args:
            enlace_id: ID del enlace
            
        Returns:
            Diccionario con el enlace o None si no existe
        """
        for enlace in self._datos.get('links', []):
            if enlace.get('id') == enlace_id:
                return enlace
        return None
    
    def url_existe(self, url: str, excluir_id: Optional[str] = None) -> bool:
        """
        Verifica si una URL ya existe en los enlaces.
        
        Args:
            url: URL a verificar
            excluir_id: ID de enlace a excluir de la verificación
            
        Returns:
            True si la URL ya existe, False en caso contrario
        """
        url_normalizada = normalizar(url)
        
        for enlace in self._datos.get('links', []):
            if excluir_id and enlace.get('id') == excluir_id:
                continue
                
            url_enlace = normalizar(enlace.get('url', ''))
            if url_enlace == url_normalizada:
                return True
        
        return False
    
    def agregar_enlace(self, titulo: str, url: str, categoria: str, tags: List[str], es_favorito: bool = False) -> Optional[str]:
        """
        Agrega un nuevo enlace.
        
        Args:
            titulo: Título del enlace
            url: URL del enlace
            categoria: Categoría del enlace
            tags: Lista de tags
            es_favorito: Si el enlace es favorito (por defecto False)
            
        Returns:
            ID del enlace creado o None si hay error
        """
        # Validaciones
        if not validar_titulo(titulo):
            logger.error("Título inválido")
            return None
            
        url_limpia = limpiar_url(url)
        if not validar_url(url_limpia):
            logger.error(f"URL inválida: {url}")
            return None
            
        if not validar_categoria(categoria):
            logger.error("Categoría inválida")
            return None
            
        if self.url_existe(url_limpia):
            logger.error(f"URL ya existe: {url_limpia}")
            return None
        
        # Limpiar y preparar datos
        tags_limpios = limpiar_tags(tags)
        timestamp_actual = obtener_timestamp_actual()
        enlace_id = str(uuid.uuid4())
        
        # Crear enlace
        nuevo_enlace = {
            "id": enlace_id,
            "titulo": titulo.strip(),
            "url": url_limpia,
            "categoria": categoria.strip(),
            "tags": tags_limpios,
            "es_favorito": es_favorito,  # ⭐ Nuevo campo favorito
            "creado_en": timestamp_actual,
            "actualizado_en": timestamp_actual
        }
        
        # Agregar a los datos
        self._datos.setdefault('links', []).append(nuevo_enlace)
        
        # Agregar categoría si no existe
        if categoria not in self._datos.setdefault('categorias', []):
            self._datos['categorias'].append(categoria)
            self._datos['categorias'].sort()
        
        logger.info(f"Enlace agregado: {titulo} -> {url_limpia}")
        return enlace_id
    
    def actualizar_enlace(self, enlace_id: str, titulo: str, url: str, 
                         categoria: str, tags: List[str], es_favorito: bool = None) -> bool:
        """
        Actualiza un enlace existente.
        
        Args:
            enlace_id: ID del enlace a actualizar
            titulo: Nuevo título
            url: Nueva URL
            categoria: Nueva categoría
            tags: Nuevos tags
            es_favorito: Estado de favorito (None para mantener el actual)
            
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        # Validaciones
        if not validar_titulo(titulo):
            logger.error("Título inválido")
            return False
            
        url_limpia = limpiar_url(url)
        if not validar_url(url_limpia):
            logger.error(f"URL inválida: {url}")
            return False
            
        if not validar_categoria(categoria):
            logger.error("Categoría inválida")
            return False
            
        if self.url_existe(url_limpia, excluir_id=enlace_id):
            logger.error(f"URL ya existe: {url_limpia}")
            return False
        
        # Buscar y actualizar enlace
        for enlace in self._datos.get('links', []):
            if enlace.get('id') == enlace_id:
                tags_limpios = limpiar_tags(tags)
                
                # Preparar datos de actualización
                datos_actualizacion = {
                    "titulo": titulo.strip(),
                    "url": url_limpia,
                    "categoria": categoria.strip(),
                    "tags": tags_limpios,
                    "actualizado_en": obtener_timestamp_actual()
                }
                
                # Solo actualizar favorito si se especifica
                if es_favorito is not None:
                    datos_actualizacion["es_favorito"] = es_favorito
                
                enlace.update(datos_actualizacion)
                
                # Agregar categoría si no existe
                if categoria not in self._datos.setdefault('categorias', []):
                    self._datos['categorias'].append(categoria)
                    self._datos['categorias'].sort()
                
                logger.info(f"Enlace actualizado: {enlace_id}")
                return True
        
        logger.error(f"Enlace no encontrado: {enlace_id}")
        return False
    
    def eliminar_enlace(self, enlace_id: str) -> bool:
        """
        Elimina un enlace.
        
        Args:
            enlace_id: ID del enlace a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        enlaces_originales = len(self._datos.get('links', []))
        self._datos['links'] = [
            enlace for enlace in self._datos.get('links', [])
            if enlace.get('id') != enlace_id
        ]
        
        eliminado = len(self._datos['links']) < enlaces_originales
        if eliminado:
            logger.info(f"Enlace eliminado: {enlace_id}")
        else:
            logger.error(f"Enlace no encontrado para eliminar: {enlace_id}")
        
        return eliminado
    
    def agregar_categoria(self, categoria: str) -> bool:
        """
        Agrega una nueva categoría.
        
        Args:
            categoria: Nombre de la categoría
            
        Returns:
            True si se agregó correctamente, False en caso contrario
        """
        if not validar_categoria(categoria):
            return False
        
        categoria = categoria.strip()
        categorias = self._datos.setdefault('categorias', [])
        
        if categoria not in categorias:
            categorias.append(categoria)
            categorias.sort()
            logger.info(f"Categoría agregada: {categoria}")
            return True
        
        return False
    
    def renombrar_categoria(self, categoria_antigua: str, categoria_nueva: str) -> bool:
        """
        Renombra una categoría existente.
        
        Args:
            categoria_antigua: Nombre actual de la categoría
            categoria_nueva: Nuevo nombre de la categoría
            
        Returns:
            True si se renombró correctamente, False en caso contrario
        """
        if not validar_categoria(categoria_nueva):
            return False
        
        categoria_nueva = categoria_nueva.strip()
        categorias = self._datos.setdefault('categorias', [])
        
        # Verificar que la categoría antigua existe y la nueva no
        if categoria_antigua not in categorias or categoria_nueva in categorias:
            return False
        
        # Renombrar en lista de categorías
        categorias[categorias.index(categoria_antigua)] = categoria_nueva
        categorias.sort()
        
        # Actualizar enlaces que usan esta categoría
        for enlace in self._datos.get('links', []):
            if enlace.get('categoria') == categoria_antigua:
                enlace['categoria'] = categoria_nueva
                enlace['actualizado_en'] = obtener_timestamp_actual()
        
        logger.info(f"Categoría renombrada: {categoria_antigua} -> {categoria_nueva}")
        return True
    
    def eliminar_categoria(self, categoria: str, mover_a: Optional[str] = None) -> bool:
        """
        Elimina una categoría.
        
        Args:
            categoria: Categoría a eliminar
            mover_a: Categoría destino para mover los enlaces (None para eliminar enlaces)
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        categorias = self._datos.setdefault('categorias', [])
        
        if categoria not in categorias:
            return False
        
        # Remover de lista de categorías
        categorias.remove(categoria)
        
        # Procesar enlaces de esta categoría
        enlaces_a_eliminar = []
        for i, enlace in enumerate(self._datos.get('links', [])):
            if enlace.get('categoria') == categoria:
                if mover_a and validar_categoria(mover_a):
                    # Mover a nueva categoría
                    enlace['categoria'] = mover_a
                    enlace['actualizado_en'] = obtener_timestamp_actual()
                    
                    # Agregar categoría destino si no existe
                    if mover_a not in categorias:
                        categorias.append(mover_a)
                        categorias.sort()
                else:
                    # Marcar para eliminar
                    enlaces_a_eliminar.append(i)
        
        # Eliminar enlaces marcados (en orden inverso para mantener índices)
        for i in reversed(enlaces_a_eliminar):
            del self._datos['links'][i]
        
        logger.info(f"Categoría eliminada: {categoria}, enlaces afectados: {len(enlaces_a_eliminar)}")
        return True
    
    def importar_datos(self, datos_importados: Dict[str, Any]) -> bool:
        """
        Importa datos desde un diccionario externo.
        
        Args:
            datos_importados: Datos a importar
            
        Returns:
            True si se importó correctamente, False en caso contrario
        """
        if not validar_estructura_json(datos_importados):
            logger.error("Estructura de datos inválida para importar")
            return False
        
        # Crear backup antes de importar
        self.crear_backup()
        
        # Reemplazar datos actuales
        self._datos = datos_importados
        
        logger.info("Datos importados correctamente")
        return True
    
    def exportar_datos(self) -> Dict[str, Any]:
        """
        Exporta los datos actuales.
        
        Returns:
            Diccionario con todos los datos
        """
        return self._datos.copy()
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de los datos.
        
        Returns:
            Diccionario con estadísticas
        """
        enlaces = self._datos.get('links', [])
        categorias = self._datos.get('categorias', [])
        
        # Contar enlaces por categoría
        contador_categorias = {}
        for enlace in enlaces:
            categoria = enlace.get('categoria', 'Sin categoría')
            contador_categorias[categoria] = contador_categorias.get(categoria, 0) + 1
        
        # Contar tags únicos
        tags_unicos = set()
        for enlace in enlaces:
            for tag in enlace.get('tags', []):
                tags_unicos.add(tag.lower())
        
        return {
            'total_enlaces': len(enlaces),
            'total_categorias': len(categorias),
            'total_tags_unicos': len(tags_unicos),
            'enlaces_por_categoria': contador_categorias,
            'total_favoritos': self.contar_favoritos()  # ⭐ Nueva estadística
        }
    
    # ⭐ NUEVAS FUNCIONES PARA FAVORITOS
    
    def marcar_favorito(self, enlace_id: str) -> bool:
        """
        Marca un enlace como favorito.
        
        Args:
            enlace_id: ID del enlace a marcar como favorito
            
        Returns:
            True si se marcó correctamente, False en caso contrario
        """
        for enlace in self._datos.get('links', []):
            if enlace.get('id') == enlace_id:
                enlace['es_favorito'] = True
                enlace['actualizado_en'] = obtener_timestamp_actual()
                logger.info(f"Enlace marcado como favorito: {enlace.get('titulo')}")
                return True
        
        logger.error(f"Enlace no encontrado: {enlace_id}")
        return False
    
    def desmarcar_favorito(self, enlace_id: str) -> bool:
        """
        Desmarca un enlace como favorito.
        
        Args:
            enlace_id: ID del enlace a desmarcar como favorito
            
        Returns:
            True si se desmarcó correctamente, False en caso contrario
        """
        for enlace in self._datos.get('links', []):
            if enlace.get('id') == enlace_id:
                enlace['es_favorito'] = False
                enlace['actualizado_en'] = obtener_timestamp_actual()
                logger.info(f"Enlace desmarcado como favorito: {enlace.get('titulo')}")
                return True
        
        logger.error(f"Enlace no encontrado: {enlace_id}")
        return False
    
    def alternar_favorito(self, enlace_id: str) -> bool:
        """
        Alterna el estado de favorito de un enlace.
        
        Args:
            enlace_id: ID del enlace
            
        Returns:
            True si el enlace ahora es favorito, False si no es favorito, None si error
        """
        for enlace in self._datos.get('links', []):
            if enlace.get('id') == enlace_id:
                # Obtener estado actual (por defecto False para compatibilidad)
                es_favorito_actual = enlace.get('es_favorito', False)
                nuevo_estado = not es_favorito_actual
                
                enlace['es_favorito'] = nuevo_estado
                enlace['actualizado_en'] = obtener_timestamp_actual()
                
                accion = "marcado" if nuevo_estado else "desmarcado"
                logger.info(f"Enlace {accion} como favorito: {enlace.get('titulo')}")
                return nuevo_estado
        
        logger.error(f"Enlace no encontrado: {enlace_id}")
        return None
    
    def obtener_favoritos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los enlaces marcados como favoritos.
        
        Returns:
            Lista de enlaces favoritos
        """
        favoritos = []
        for enlace in self._datos.get('links', []):
            if enlace.get('es_favorito', False):
                favoritos.append(enlace.copy())
        
        # Ordenar por fecha de actualización (más recientes primero)
        favoritos.sort(key=lambda x: x.get('actualizado_en', ''), reverse=True)
        return favoritos
    
    def contar_favoritos(self) -> int:
        """
        Cuenta el número total de enlaces favoritos.
        
        Returns:
            Número de enlaces favoritos
        """
        count = 0
        for enlace in self._datos.get('links', []):
            if enlace.get('es_favorito', False):
                count += 1
        return count
    
    def es_favorito(self, enlace_id: str) -> bool:
        """
        Verifica si un enlace es favorito.
        
        Args:
            enlace_id: ID del enlace
            
        Returns:
            True si es favorito, False en caso contrario
        """
        for enlace in self._datos.get('links', []):
            if enlace.get('id') == enlace_id:
                return enlace.get('es_favorito', False)
        return False
    
    def migrar_favoritos(self) -> None:
        """
        Migra enlaces existentes para agregar el campo es_favorito si no existe.
        Esta función se ejecuta automáticamente en la carga.
        """
        migrados = 0
        for enlace in self._datos.get('links', []):
            if 'es_favorito' not in enlace:
                enlace['es_favorito'] = False
                migrados += 1
        
        if migrados > 0:
            logger.info(f"Migrados {migrados} enlaces para soporte de favoritos")
            # Guardar automáticamente después de la migración
            self.guardar()