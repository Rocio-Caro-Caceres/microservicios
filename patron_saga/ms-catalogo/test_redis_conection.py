import redis
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def probar_conexion_redis():
    try:
        # Configuración de conexión desde variables de entorno
        r = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            password=os.getenv('REDIS_PASSWORD')
        )

        # Probar conexión con PING
        print("Intentando conectar a Redis...")
        r.ping()
        print("✅ Conexión exitosa!")

        # Prueba de escritura y lectura
        print("\nProbando escritura y lectura:")
        clave_prueba = 'test_conexion'
        valor_prueba = 'Conexión Redis funcionando correctamente'
        
        # Guardar valor
        r.set(clave_prueba, valor_prueba)
        print(f"Guardado: {clave_prueba} = {valor_prueba}")

        # Recuperar valor
        valor_recuperado = r.get(clave_prueba)
        print(f"Recuperado: {valor_recuperado.decode('utf-8')}")

        # Eliminar clave de prueba
        r.delete(clave_prueba)
        print("Clave de prueba eliminada")

    except redis.exceptions.ConnectionError as e:
        print(f"❌ Error de conexión: {e}")
    except redis.exceptions.AuthenticationError as e:
        print(f"❌ Error de autenticación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

# Ejecutar el script
if __name__ == '__main__':
    probar_conexion_redis()