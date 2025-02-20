import logging
from saga import SagaBuilder, SagaError
from .mscatalogo_service import ClienteCatalogoService
from .mscompras_service import ClienteComprasService
from .msinventario_service import ClienteInventarioService
from .mspagos_service import ClientePagosService
from .redis_lock_service import RedisLockService
from app.models import Carrito, Producto
from app import cache

clienteCompras = ClienteComprasService()
clientePagos = ClientePagosService()
clienteInventario = ClienteInventarioService()
clienteCatalogo = ClienteCatalogoService()

class CommerceService:
    """
    Clase que implementa la funcionalidad de Orquestador en el patron SAGA de microservicios
    """
    def __init__(self):
        self.lock_service = RedisLockService()
 
    def comprar(self, carrito: Carrito) -> dict:
        
        if not self.lock_service.acquire_lock(carrito.producto.id):
            logging.warning(f"No se pudo adquirir el lock para el producto {carrito.producto.id}")
            return {"error": "El producto está siendo procesado, intente nuevamente"}
        
        try:
            SagaBuilder.create()\
                .action(lambda: clienteCompras.comprar(carrito.producto, carrito.direccion_envio), lambda: clienteCompras.cancelar_compra()) \
                .action(lambda: clientePagos.registrar_pago(carrito.producto, carrito.medio_pago), lambda: clientePagos.cancelar_pago()) \
                .action(lambda: clienteInventario.retirar_producto(carrito), lambda: clienteInventario.ingresar_producto()) \
                .build().execute()
            return {"success": True, "message": "Compra realizada exitosamente"}
        
        except ValueError as e:
            # Este error vendrá del microservicio de inventario cuando no hay stock suficiente
            logging.error(f"Error de validación: {str(e)}")
            return {"success": False, "error": "stock_insufficient", "details": str(e)}
        
        except SagaError as e:
            # Este error vendrá de los microservicios de compras o pagos
            logging.error(f"Error en la saga: {str(e)}")
            return {"success": False, "error": "saga_error", "details": str(e)}
        
        except Exception as e:
            # Error inesperado
            logging.error(f"Error inesperado: {str(e)}")
            return {"success": False, "error": "internal_error", "details": "Ocurrió un error inesperado."}
        
        finally:
            # Siempre liberar el lock al terminar
            self.lock_service.release_lock(carrito.producto.id)

    def consultar_catalogo(self, id: int) -> Producto:
        result = cache.get(f"producto_{id}")
        logging.info(f'datos en cache {result}')
        if result is None:
            result = clienteCatalogo.obtener_producto(id)
            cache.set(f"producto_{id}", result, timeout=60)
        return result
