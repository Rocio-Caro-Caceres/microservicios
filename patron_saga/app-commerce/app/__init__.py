from flask import Flask
from flask_caching import Cache
from flask_marshmallow import Marshmallow
import os
from app.config import config
from app.config.cache_config import cache_config

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

ma = Marshmallow()
cache = Cache()

limiter = Limiter(key_func=get_remote_address)

def create_app() -> Flask:
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)
    print(f"Running in {cache_config} mode")
    ma.init_app(app)
    cache.init_app(app, config=cache_config)

    limiter.init_app(app)

    from app.resources import home
    app.register_blueprint(home, url_prefix='/api/v1')
    

    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app

