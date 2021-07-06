import json

from aiohttp import web

from auth import auth

async def get_status(request) -> web.Response:
    task_id = int(request.match_info.get('id'))
    
    operation_ascess = await auth()
    if type(operation_ascess) == str:
        with open('json/storage.json', 'r') as data_file:
            data = json.load(data_file)
        try:
            if data[task_id]['status'] != 'ok':
                return web.Response(text = data[task_id]['status'])
            else:
                data = {
                    "status": "ok",
                    "files": data[task_id]['files']
                }
                return web.json_response(data)
        except Exception:
            web.Response(text = 'something wrong')
    else:
        return web.Response(text = 'Auth error')