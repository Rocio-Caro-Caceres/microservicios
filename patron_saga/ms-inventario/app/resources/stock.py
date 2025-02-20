from flask import Blueprint, request
from app.mapping import StockSchema
from app.services import StockService

stock_bp = Blueprint('stock', __name__)
stock_schema = StockSchema()
stock_service = StockService()



@stock_bp.route('/inventarios/retirar', methods=['POST'])
def retirar_producto():
    try:
        stock = stock_schema.load(request.json)
        stock = stock_service.retirar(stock)
        if stock and stock.id:
            return stock_schema.dump(stock), 200
        return {'error': 'Error al procesar el retiro'}, 500
    except ValueError as e:
        return {'error': str(e)}, 400
    except Exception as e:
        return {'error': 'Error interno del servidor'}, 500
    
@stock_bp.route('/inventarios/ingresar', methods=['POST'])
def ingresar_producto():
    stock = stock_schema.load(request.json)
    stock = stock_service.ingresar(stock)
    
    if stock.id:
        status_code = 200 
    else:
        status_code = 500

    return stock_schema.dump(stock), status_code


@stock_bp.route('/inventarios/stock/<int:producto_id>', methods=['GET'])
def consultar_stock(producto_id: int):
    print(f"Consultando stock para producto {producto_id}")  # Agregar este print
    stock_disponible = stock_service.consultar_stock_disponible(producto_id)
    if stock_disponible is not None:
        return {
            'producto_id': producto_id,
            'stock_disponible': stock_disponible
        }, 200
    return {'error': 'No se encontró el producto'}, 404


