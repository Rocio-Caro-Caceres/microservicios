from flask import jsonify, Blueprint, request

from app.mapping import CarritoSchema, ProductoSchema
from app.services import CommerceService
from app import limiter
import logging

home = Blueprint('home', __name__)
carrito_schema = CarritoSchema()
producto_schema = ProductoSchema()

@home.route('/commerce/comprar', methods=['POST'])
@limiter.limit("3 per minute")  
def index():
    commerce = CommerceService()
    carrito = carrito_schema.load(request.get_json())
    try:
        resultado = commerce.comprar(carrito)  # Capturar el resultado del orquestador
        logging.info(f"Resultado del orquestador: {resultado}")  # Depuración
        
        if resultado["success"]:
            return jsonify({
                "status": "success",
                "message": "¡Compra realizada exitosamente! Gracias por su compra."
            }), 200
        else:
            # Manejo de errores específicos
            if resultado.get("error") == "stock_insufficient":
                return jsonify({
                    "status": "error",
                    "message": "No hay suficiente stock disponible para completar la compra.",
                    "details": resultado.get("details")
                }), 409  # Conflict
            elif resultado.get("error") == "saga_error":
                return jsonify({
                    "status": "error",
                    "message": "Ocurrió un error al procesar su compra. Por favor, intente nuevamente más tarde.",
                    "details": resultado.get("details")
                }), 400  # Bad Request
            else:
                # Manejo de otros errores
                return jsonify({
                    "status": "error",
                    "message": "Ocurrió un error inesperado. Por favor, contacte al soporte técnico.",
                    "details": resultado.get("details")
                }), 500  # Internal Server Error

    except Exception as e:
        # Manejo de errores inesperados
        logging.error(f"Error inesperado: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Ocurrió un error inesperado. Por favor, contacte al soporte técnico."
        }), 500
@home.route('/commerce/consultar/catalogo/<int:id>', methods=['GET'])
def consultar_catalogo(id:int):
    commerce = CommerceService()
    producto = commerce.consultar_catalogo(id)
    result = {"message": "No se encontró el producto"}
    status_code = 404
    if producto:
        result = producto_schema.dump(producto)
        status_code = 200
    return result, status_code
