from app import db
from app.models import Stock

class StockRepository:
    def get_stock_disponible(self, producto_id: int) -> int:
        # Calculamos entradas (1) y salidas (2)
        entradas = db.session.query(db.func.sum(Stock.cantidad))\
            .filter(Stock.producto == producto_id)\
            .filter(Stock.entrada_salida == 1)\
            .scalar() or 0
            
        salidas = db.session.query(db.func.sum(Stock.cantidad))\
            .filter(Stock.producto == producto_id)\
            .filter(Stock.entrada_salida == 2)\
            .scalar() or 0
            
        return entradas - salidas
    
    def save(self, stock: Stock) -> Stock:
        db.session.add(stock)
        db.session.commit()
        return stock
    