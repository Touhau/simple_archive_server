import os
import json

from aiohttp import web

from save_archive import storage_change
from auth import auth

async def delete_archive(request) -> web.Response:
    task_id = int(request.match_info.get('id'))
    operation_ascess = await auth()
    if type(operation_ascess) == str:
        with open('json/storage.json', 'r') as data_file:
                data = json.load(data_file)
        try:
            if data[task_id]['status'] == 'deleted':
                return web.Response(text = 'archive already deleted')
            else:
                os.remove(data[task_id]['path'])
                await storage_change(task_id, 'status', 'deleted')
                return web.Response(text = 'deleted')
        except Exception:
            web.Response(text = 'something wrong')
    else:
        return web.Response(text = 'Auth error')