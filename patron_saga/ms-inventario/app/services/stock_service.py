from app import db
from app.models import Stock
from app.repositories import StockRepository
from datetime import datetime
from app import cache
import logging

repository = StockRepository()
class StockService:

    def validar_stock_disponible(self, producto_id: int, cantidad_requerida: int) -> bool:
        # Intentamos obtener el stock de cache primero
        stock_cache = cache.get(f'stock_disponible_{producto_id}')
        
        if stock_cache is not None:
            return stock_cache >= cantidad_requerida
            
        # Si no está en cache, consultamos la BD
        stock_disponible = repository.get_stock_disponible(producto_id)
        
        # Guardamos en cache por 60 segundos
        cache.set(f'stock_disponible_{producto_id}', stock_disponible, timeout=60)
        
        return stock_disponible >= cantidad_requerida


    def retirar(self, stock: Stock) -> Stock:
        if stock is not None:
            # Validamos stock disponible
            stock_disponible = repository.get_stock_disponible(stock.producto)
            if stock_disponible < stock.cantidad:
                logging.error(f"Stock insuficiente para el producto {stock.producto}. Disponible: {stock_disponible}, Solicitado: {stock.cantidad}")
                raise ValueError(f"Stock insuficiente. Disponible: {stock_disponible}, Solicitado: {stock.cantidad}")
                # "return None  # Mantenemos el comportamiento original de retornar None"
                
            stock.fecha_transaccion = stock.fecha_transaccion if stock.fecha_transaccion is not None else datetime.now()
            stock.entrada_salida = 2  # Salida de Producto
            result = repository.save(stock)
            
            # Verificamos que el objeto tenga un id después de guardarlo (agregado)
            if not hasattr(result, 'id') or result.id is None:
                logging.error("El objeto Stock no tiene un atributo 'id' después de guardarlo")
                raise ValueError("Error al guardar el Stock: no se asignó un ID")

            # Actualizamos cache
            cache.set(f'stock_{stock.id}', result, timeout=60)
            cache.set(f'stock_disponible_{stock.producto}', stock_disponible - stock.cantidad, timeout=60)
        
        return result
    def ingresar(self, stock: Stock) -> Stock:
        result = None
        if stock is not None:
            stock.fecha_transaccion = stock.fecha_transaccion if stock.fecha_transaccion is not None else datetime.now()
            stock.entrada_salida = 1  # Entrada de Producto
            result = repository.save(stock)
            
            # Actualizamos cache
            stock_disponible = repository.get_stock_disponible(stock.producto)
            cache.set(f'stock_{stock.id}', result, timeout=60)
            cache.set(f'stock_disponible_{stock.producto}', stock_disponible, timeout=60)
        
        return result
    
    def consultar_stock_disponible(self, producto_id: int):
        # Intentamos obtener el stock de cache primero
        stock_cache = cache.get(f'stock_disponible_{producto_id}')
        
        if stock_cache is not None:
            return stock_cache
            
        # Si no está en cache, consultamos la BD
        stock_disponible = repository.get_stock_disponible(producto_id)
        
        # Guardamos en cache por 60 segundos
        cache.set(f'stock_disponible_{producto_id}', stock_disponible, timeout=60)
        
        return stock_disponible
    