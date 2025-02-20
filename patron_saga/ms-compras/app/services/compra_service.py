from datetime import datetime
from app.models import Compra
from app.repositories import CompraRepository
from app import cache
import logging

repository = CompraRepository()
class CompraService:

   def save(self, compra: Compra) -> Compra:
      compra.fecha_compra = datetime.now()
      result = repository.save(compra)

      if result:
         logging.info(f"[COMPRA_SERVICE] Compra guardada con ID: {result.id}")
         cache.set(f"compra_{result.id}", result, timeout=60)
         logging.info(f"[COMPRA_SERVICE] Compra almacenada en caché con ID: {result.id}")
      else:
        logging.error("[COMPRA_SERVICE] ERROR: No se pudo guardar la compra en la BD")
           
      return result
   
   def delete(self, id: int) -> Compra:
      if id:
         cache.delete(f"compra_{id}")
      
      result = repository.delete(id)
      return result