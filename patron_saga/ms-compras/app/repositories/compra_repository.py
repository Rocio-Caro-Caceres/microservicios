from app import db
from app.models import Compra
import logging

class CompraRepository:

    def save(self, compra: Compra) -> Compra:
          
        logging.info(f"[COMPRA_REPOSITORY] Guardando compra en la BD: {compra}")
        db.session.add(compra)
        db.session.commit()
        logging.info(f"[COMPRA_REPOSITORY] Compra guardada con ID: {compra.id}") # Log del id generado
        return compra
        
    def delete(self, id: int) -> Compra:
        compra = Compra.query.get(id)
        compra.deleted_at = db.func.now()
        db.session.commit()
        return compra