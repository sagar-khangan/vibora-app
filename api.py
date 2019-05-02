from vibora import Request
from vibora.blueprints import Blueprint
from vibora.responses import JsonResponse, StreamingResponse, Response
from vibora.cache import CacheEngine
import asyncio
from schema import UserSchema

api = Blueprint()


class AppCacheEngine(CacheEngine):
    async def get(self, request: Request):
        return self.cache.get(request.url)

    async def store(self, request: Request, response):
        self.cache[request.url] = response
        

@api.route('/home', methods=['GET','POST','PUT'])
async def home(request:Request):
    if request.method == b'GET':
        resp = {'hello': 'world'}
    else:
        resp = await  UserSchema.load_json(request)
    return JsonResponse(resp,headers={'x-my-custom-header':'hello'})


@api.route('/product/<product_id>',cache=AppCacheEngine(skip_hooks=True))
async def show_product(product_id: str):
    return Response(f'Chosen product: {product_id}'.encode())


@api.route('/stream')
async def home():
    async def stream_builder():
        for x in range(0, 5):
            yield str(x).encode()
            await asyncio.sleep(1)

    return StreamingResponse(
           stream_builder, chunk_timeout=10, complete_timeout=30
    )


@api.route('/file')
async def show_product():
    title = "Vibora App"
    users = [{'name':'A'},{'name':'B'},{'name':'C'}]
    return await api.render('index.html',title=title,users=users)
