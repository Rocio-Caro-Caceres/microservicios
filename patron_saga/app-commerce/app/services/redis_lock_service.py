import logging
from app import cache

class RedisLockService:
    """
    Servicio que implementa un lock distribuido usando Redis
    """
    def __init__(self):
        self.redis_client = cache
        self.lock_timeout = 60  # segundos para evitar deadlocks

    def acquire_lock(self, product_id: int) -> bool:
        """
        Intenta adquirir un lock para un producto específico
        """
        lock_key = f"stock_lock_{product_id}"
        return self.redis_client.add(lock_key, "locked", timeout=self.lock_timeout)

    def release_lock(self, product_id: int) -> None:
        """
        Libera el lock de un producto específico
        """
        lock_key = f"stock_lock_{product_id}"
        self.redis_client.delete(lock_key)