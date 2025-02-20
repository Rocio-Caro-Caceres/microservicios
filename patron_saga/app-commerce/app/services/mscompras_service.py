import os
import logging
import requests

from app.mapping import CompraSchema
from app.models import Compra, Producto

class ClienteComprasService:
    
    def __init__(self):
        self.compra = Compra()
        self.URL = os.getenv('MSCOMPRAS_URL', 'http://localhost:5002/api/v1/')
    
    def comprar(self, producto: Producto, direccion_envio: str) -> None:
        self.compra.producto = producto.id
        self.compra.direccion_envio = direccion_envio
        compra_schema = CompraSchema()

        # Serializar y loggear en una sola línea
        logging.info(f"[CLIENTE_COMPRAS] Enviando datos al MS compras: {compra_schema.dump(self.compra)}")
        
        # Enviar la solicitud al microservicio de compras
        r = requests.post(f'{self.URL}compras', json=compra_schema.dump(self.compra))   

        logging.info(f"[CLIENTE_COMPRAS] Respuesta del microservicio compras: {r.status_code} - {r.text}")

        if r.status_code == 200:
            logging.info(f"Compra <- {r.json()}")
       
            # Deserializar la respuesta y actualizar self.compra
            compra_data = r.json()
            self.compra = compra_schema.load(compra_data)
            logging.info(f"[CLIENTE_COMPRAS] Compra deserializada con ID: {self.compra.id}")

            # Verificar que el id esté asignado
            if not self.compra.id:
                logging.error("[CLIENTE_COMPRAS] ERROR: La compra no tiene un ID válido")
                raise BaseException("La compra no tiene un id válido")
        
            logging.info(f"Compra realizada id: {self.compra.id}")
        else:
            logging.error("[CLIENTE_COMPRAS] ERROR en el microservicio compras")
            raise BaseException("Error en el microservicio compras")
        
    def cancelar_compra(self) -> None:
        
        if not self.compra.id:
            logging.error("No se puede cancelar una compra sin id")
            raise BaseException("No se puede cancelar una compra sin id")
        
        r = requests.delete(f'{self.URL}compras/{self.compra.id}')
        if r.status_code == 200:
            logging.warning(f"Compra eliminada id: {self.compra.id}")
        else:
            logging.error("Error tratando de compensar Compras")
            raise BaseException("Error tratando de compensar Compras")