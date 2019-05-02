from vibora.router import RouterStrategy
import json
from vibora.static import StaticHandler
from vibora import Vibora
from api import api
from config import Config
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = f'{BASE_DIR}/template'
STATIC_DIR = f'{BASE_DIR}/template'

if __name__ == '__main__':
    app = Vibora(router_strategy=RouterStrategy.STRICT,static=StaticHandler(
        paths=[STATIC_DIR],
        host="*",
        max_cache_size=1 * 1024 * 1024
        ),
        template_dirs=[TEMPLATE_DIR]
    )
    app.add_blueprint(api, prefixes={'v1': '/v1'})
    with open('config.json') as f:

        config = Config(json.load(f))
        app.components.add(config)
        app.run(host=config.host, port=config.port)


